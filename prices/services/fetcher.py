import asyncio
import logging
from decimal import Decimal

from django.conf import settings
from django.db import transaction

from prices.models import Currency, PriceHistory
from prices.providers.base import BaseProvider
from prices.providers.coingecko import CoinGeckoProvider

logger = logging.getLogger(__name__)


def _get_provider() -> BaseProvider:
    provider_name = getattr(settings, 'CRYPTO_PRICE_PROVIDER', 'coingecko')
    if provider_name == 'coingecko':
        return CoinGeckoProvider()
    elif provider_name == 'binance':
        from prices.providers.binance import BinanceProvider
        return BinanceProvider()
    raise ValueError(f'Unknown provider: {provider_name}')


def fetch_and_store_prices():
    """
    Function sink: We execute the provider asynchronously with asyncio.run and store the results in the DB.
    Return: dict containing the execution summary or error
    """
    currencies = list(Currency.objects.filter(active=True))
    if not currencies:
        return {'success': True, 'message': 'No active currencies configured', 'stored': 0}

    provider = _get_provider()
    provider_ids = [c.provider_id or c.code.lower() for c in currencies]

    try:
        results = asyncio.run(provider.fetch_current_prices(provider_ids))
    except Exception as e:
        logger.exception('Provider fetch failed')
        return {'success': False, 'message': str(e), 'stored': 0}

    stored = 0
    with transaction.atomic():
        for c in currencies:
            pid = c.provider_id or c.code.lower()
            entry = results.get(pid)
            if not entry:
                logger.warning('No data from provider for %s', pid)
                continue
            # Let's assume vs_currency = usd
            price_val = entry.get('usd')
            if price_val is None:
                logger.warning('USD price not found for %s -> %s', pid, entry)
                continue
            try:
                price_dec = Decimal(str(price_val))
                PriceHistory.objects.create(currency=c, price=price_dec,
                                            provider=getattr(settings, 'CRYPTO_PRICE_PROVIDER', 'unknown'), raw=entry)
                stored += 1
            except Exception:
                logger.exception('Failed to store price for %s', c)

    return {'success': True, 'message': 'Fetch complete', 'stored': stored}
