from datetime import datetime, timezone, timedelta
from decimal import Decimal

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from prices.models import Currency, PriceHistory


@pytest.mark.django_db
class TestPricesAPI:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        # Create sample currency
        self.currency = Currency.objects.create(code='BTC', name='Bitcoin', provider_id='bitcoin', active=True)
        # Create multiple price records
        now = datetime.now(timezone.utc)
        PriceHistory.objects.create(currency=self.currency, price=Decimal('30000.12345678'),
                                    timestamp=now - timedelta(minutes=10), provider='coingecko')
        PriceHistory.objects.create(currency=self.currency, price=Decimal('30500.87654321'), timestamp=now,
                                    provider='coingecko')

    def test_latest_prices(self):
        url = reverse('latest_prices')
        response = self.client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert 'BTC' in [item['code'] for item in data['data']]
        # Check that the latest price matches the latest timestamp
        btc_data = next(filter(lambda x: x['code'] == 'BTC', data['data']))
        assert btc_data['price'] == '30500.87654321'

    def test_price_history_default_limit(self):
        url = reverse('price_history', kwargs={'code': 'BTC'})
        response = self.client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        # The default limit value is 50; we only have 2 records
        assert len(data['data']) == 2

    def test_price_history_with_limit(self):
        url = reverse('price_history', kwargs={'code': 'BTC'})
        response = self.client.get(url + '?limit=1')
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert len(data['data']) == 1

    def test_price_history_not_found(self):
        url = reverse('price_history', kwargs={'code': 'NONEXISTENT'})
        response = self.client.get(url)
        assert response.status_code == 404
        data = response.json()
        assert data['success'] is False
        assert data['message'] == 'Currency not found'
