import logging
from datetime import date

from django.utils import timezone

from .models import DailyStock
from .serializers import DailyStockSerializer

logger = logging.getLogger()


def bulk_create_or_update_stock(stock_entries, updated_fields):
    dates_to_check = [entry["date"] for entry in stock_entries]

    existing_data = DailyStock.objects.filter(date__in=dates_to_check).values_list(
        "id", "date"
    )

    existing_data_map = {date.strftime("%Y-%m-%d"): id for id, date in existing_data}

    records_to_create = []
    records_to_update = []

    for entry in stock_entries:
        record = DailyStock(**entry)

        if entry["date"] in existing_data_map:
            record.id = existing_data_map[entry["date"]]
            record.updated_at = timezone.now()
            records_to_update.append(record)
        else:
            records_to_create.append(record)

    if records_to_create:
        DailyStock.objects.bulk_create(records_to_create, ignore_conflicts=True)

    if records_to_update:
        DailyStock.objects.bulk_update(records_to_update, updated_fields)


def store_fetched_data(fetched_data):
    stock_entries = [
        {
            "open_price": float(price_data["1. open"]),
            "high_price": float(price_data["2. high"]),
            "low_price": float(price_data["3. low"]),
            "close_price": float(price_data["4. close"]),
            "volume": int(price_data["5. volume"]),
            "date": date,
        }
        for date, price_data in fetched_data
    ]

    try:
        bulk_create_or_update_stock(
            stock_entries,
            [
                "open_price",
                "high_price",
                "low_price",
                "close_price",
                "volume",
                "updated_at",
            ],
        )
        return stock_entries
    except Exception as e:
        logger.error(f"Failed to create or update stock models: {str(e)}")
        raise ValueError("Failed to store fetched data")


def store_predicted_data(predicted_data):
    payloads = [
        {
            "predicted_close_price": item["predicted_close_price"],
            "date": item["date"],
        }
        for item in predicted_data
    ]

    stock_entries = [
        {
            "predicted_close_price": item["predicted_close_price"],
            "date": item["date"],
        }
        for item in predicted_data
    ]

    try:
        bulk_create_or_update_stock(
            stock_entries, ["predicted_close_price", "updated_at"]
        )
        return predicted_data
    except Exception as e:
        logger.error(f"Failed to create or update predicted stock models: {str(e)}")
        raise ValueError("Failed to store predicted data")


def update_stock_with_predictions(df, predictions):
    for index, predicted_price in enumerate(predictions):
        daily_stock_entry = DailyStock.objects.get(date=df.iloc[index]["date"])
        daily_stock_entry.predicted_close_price = round(predicted_price, 2)
        daily_stock_entry.save()

    return predictions
