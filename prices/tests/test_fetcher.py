from decimal import Decimal
from unittest.mock import patch, AsyncMock

import pytest

from prices.models import Currency, PriceHistory
from prices.services.fetcher import fetch_and_store_prices


@pytest.mark.django_db
@patch('prices.services.fetcher.CoinGeckoProvider.fetch_current_prices', new_callable=AsyncMock)
def test_fetch_and_store_prices(mock_fetch):
    # Test data preparation: an active currency
    currency = Currency.objects.create(code='BTC', provider_id='bitcoin', active=True)

    # Define fake output from provider (async)
    mock_fetch.return_value = {
        'bitcoin': {'usd': 12345.67}
    }

    result = fetch_and_store_prices()

    # Output test
    assert result['success'] is True
    assert result['stored'] == 1

    # Test that the price record is saved
    price_entry = PriceHistory.objects.filter(currency=currency).first()
    assert price_entry is not None
    assert price_entry.price == Decimal('12345.67')
    assert price_entry.provider == 'coingecko'

    # Test when there is no active currency
    Currency.objects.all().delete()
    result_empty = fetch_and_store_prices()
    assert result_empty['success'] is True
    assert result_empty['stored'] == 0
    assert 'No active currencies' in result_empty['message']
