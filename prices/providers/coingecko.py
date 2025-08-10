import httpx

from .base import BaseProvider


class CoinGeckoProvider(BaseProvider):
    BASE_URL = 'https://api.coingecko.com/api/v3'

    async def fetch_current_prices(self, provider_ids: list, vs_currency: str = 'usd') -> dict:
        ids = ','.join(provider_ids)
        url = f"{self.BASE_URL}/simple/price"
        params = {'ids': ids, 'vs_currencies': vs_currency}
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            return resp.json()
