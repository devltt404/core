import logging
from datetime import datetime, timedelta

import joblib
import numpy as np
from django.conf import settings
from django.shortcuts import render
from financial_data.utils import store_predicted_data
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger()


class Predictions(APIView):
    def get(self, request):
        """
        Use pre-trained model to predict stock prices
        for the next 30 days
        """
        model = joblib.load(settings.STOCK_PRICES_MODEL_PATH)

        if not model:
            logger.error("Stock prices model not found.")
            return Response({"error": "Internal server error."}, status=500)

        today = datetime.now()
        next_30_days = [today + timedelta(days=i) for i in range(1, 31)]
        next_30_days_timestamps = np.array(
            [dt.timestamp() for dt in next_30_days]
        ).reshape(-1, 1)
        predictions = model.predict(next_30_days_timestamps)
        predicted_prices = [
            {
                "date": dt.strftime("%Y-%m-%d"),
                "predicted_close_price": round(price.item(), 2),
            }
            for dt, price in zip(next_30_days, predictions)
        ]

        try:
            store_predicted_data(predicted_prices)
        except Exception as e:
            logger.error(f"Failed to store predicted data: {e}")
            return Response(
                {"error": "Internal server error. Please try again later."}, status=500
            )

        return Response(data=predicted_prices, status=200)
