import joblib
import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

from financial_data.models import DailyStock
from financial_data.utils import update_stock_with_predictions


class Command(BaseCommand):
    help = "Train the future stock prices prediction model and update predictions in the database"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Training model..."))
        df = self.load_data()
        if df is None:
            return

        model, score = self.train_model(df)
        self.stdout.write(
            self.style.SUCCESS(
                f"Model trained and saved successfully with score: {score:.4f}"
            )
        )

        self.stdout.write(self.style.WARNING("Predicting the old data..."))
        predictions = model.predict(df[["timestamp"]])

        update_stock_with_predictions(df, predictions)

        self.stdout.write(
            self.style.SUCCESS("Predicted prices updated successfully in the database.")
        )

    def load_data(self):
        df = pd.DataFrame(
            list(
                DailyStock.objects.filter(close_price__isnull=False)
                .order_by("date")
                .values("date", "close_price")
            )
        )

        if df.empty:
            self.stdout.write(self.style.ERROR("No data available for training."))
            return None

        df["date"] = pd.to_datetime(df["date"])
        df["timestamp"] = df["date"].map(pd.Timestamp.timestamp)
        return df

    def train_model(self, df):
        X = df[["timestamp"]]
        y = df["close_price"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        model = LinearRegression()
        model.fit(X_train, y_train)

        joblib.dump(model, settings.STOCK_PRICES_MODEL_PATH)

        return model, model.score(X_test, y_test)
