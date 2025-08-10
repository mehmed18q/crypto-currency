from django.core.management.base import BaseCommand

from prices.services.fetcher import fetch_and_store_prices


class Command(BaseCommand):
    help = 'Fetch current prices once (used by entrypoint or manually)'

    def handle(self, *args, **options):
        result = fetch_and_store_prices()
        self.stdout.write(str(result))
