import json

import httpx

from .base import BaseProvider


class BinanceProvider(BaseProvider):
    BASE_URL = 'https://api.binance.com/api/v3'

    async def fetch_current_prices(self, provider_ids: list[str], vs_currency: str = 'usd') -> dict:
        """
        The Binance provider gets the prices.
        Note: On Binance, prices are usually given relative to USDT.
        We assume vs_currency = 'usd', meaning we should use 'USDT'.
        """
        symbols = [pid.upper() + 'USDT' for pid in provider_ids]
        url = f"{self.BASE_URL}/ticker/price"
        params = {'symbols': json.dumps(symbols)}
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()  # List of dictionaries

        # Convert the output to a CoinGecko-like format (dict with provider_id key)
        result = {}
        for item in data:
            symbol = item['symbol']  # Like BTCUSDT
            price_str = item['price']
            # provider_id: remove 'USDT' from the end
            if symbol.endswith('USDT'):
                pid = symbol[:-4].lower()
                try:
                    price = float(price_str)
                    result[pid] = {'usd': price}
                except Exception:
                    # If the price doesn't convert, reject it.
                    continue
        return result
