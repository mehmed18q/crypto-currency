from celery import shared_task

from .services.fetcher import fetch_and_store_prices


@shared_task(bind=True)
def fetch_prices_task(self):
    return fetch_and_store_prices()
