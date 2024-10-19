import logging

from data_fetcher.views import DataFetcher
from django.core.management.base import BaseCommand

logger = logging.getLogger()


class Command(BaseCommand):
    help = "Fetch daily stock price data for AAPL symbol using Alpha Vantage API."

    def handle(self, *args, **kwargs):
        data_fetcher = DataFetcher()

        try:
            response = data_fetcher.get(None)
            self.stdout.write(self.style.SUCCESS("Data fetched successfully."))
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
