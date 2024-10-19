import logging
from datetime import datetime, timedelta
from itertools import islice

import requests
from django.conf import settings
from django.shortcuts import render
from financial_data.utils import store_fetched_data
from rest_framework.views import APIView

from .exceptions import APIRateLimitExceeded

logger = logging.getLogger()


class DataFetcher(APIView):
    def get(self, request):
        """
        Fetches daily stock price data for AAPL symbol in the last 2 years using Alpha Vantage API.
        """

        try:
            response = requests.get(
                "https://www.alphavantage.co/query",
                params={
                    "function": "TIME_SERIES_DAILY",
                    "symbol": "AAPL",
                    "outputsize": "full",
                    "apikey": settings.ALPHA_VANTAGE_API_KEY,
                },
            )
            response.raise_for_status()

            data = response.json()

            # Handle invalid response that doesn't contain "Time Series (Daily)" key
            if "Time Series (Daily)" not in data:
                if "Information" in data and "API rate limit" in data["Information"]:
                    raise APIRateLimitExceeded()

                raise Exception(f"Invalid response from Alpha Vantage API: {data}")

            fetched_stock = data.get("Time Series (Daily)", {})
            # Extracted stock data for the last 2 years
            start_date = datetime.now() - timedelta(days=730)
            in_range_stock_end = len(fetched_stock)
            for index, (date, _) in enumerate(fetched_stock.items()):
                if datetime.strptime(date, "%Y-%m-%d") <= start_date:
                    in_range_stock_end = index
                    break

            filtered_fetched_stock = list(
                islice(fetched_stock.items(), in_range_stock_end)
            )
            stock_entries = store_fetched_data(filtered_fetched_stock)
            
            return render(
                request,
                "fetch_data.html",
                {"stock_entries": stock_entries},
            )

        except APIRateLimitExceeded as e:
            logger.error(e)
            return render(
                request,
                "error.html",
                {"error_message": e},
                status=429,
            )

        except Exception as e:
            logger.error(f"Unexpected error occurred when fetching data: {e}")
            return render(
                request,
                "error.html",
                {"error_message": "Internal server error. Please try again later."},
                status=500,
            )
