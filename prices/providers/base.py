class BaseProvider:
    """Base interface for providers. Implement fetch_current_prices as async method.

    return value should be a dict keyed by provider_id with provider-specific data;
    for coin-gecko we expect something like: {'bitcoin': {'usd': 12345.0}}
    """

    async def fetch_current_prices(self, provider_ids: list, vs_currency: str = 'usd'):
        raise NotImplementedError
