import os

from django.conf import settings
from django.http import FileResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from backtest.utils import execute_backtest
from financial_data.models import DailyStock
from predictions.utils import calculate_predictions_metrics

from .utils import create_performance_pdf, generate_visualization


class PerformanceReport(APIView):
    STOCK_PRICES_PREDICTION_PLOT_PATH = os.path.join(
        settings.REPORTS_DIR, "stock_prices_prediction.png"
    )
    PDF_FILE_PATH = os.path.join(settings.REPORTS_DIR, "performance_report.pdf")

    def get(self, request):
        stock_data = DailyStock.objects.all()

        dates = [item.date for item in stock_data]
        actual_prices = [item.close_price for item in stock_data]
        predicted_prices = [item.predicted_close_price for item in stock_data]

        generate_visualization(
            self.STOCK_PRICES_PREDICTION_PLOT_PATH,
            dates,
            actual_prices,
            predicted_prices,
        )

        metrics = calculate_predictions_metrics(actual_prices, predicted_prices)
        backtest_result = execute_backtest(10000, 50, 200)

        if request.GET.get("response") == "pdf":
            create_performance_pdf(
                self.PDF_FILE_PATH,
                self.STOCK_PRICES_PREDICTION_PLOT_PATH,
                actual_prices,
                predicted_prices,
                backtest_result,
                metrics,
            )

            response = FileResponse(
                open(self.PDF_FILE_PATH, "rb"),
                content_type='application/pdf; name="MyFile.pdf"',
            )
            if request.GET.get("download") == "true":
                response["Content-Disposition"] = (
                    'attachment; filename="performance_report.pdf"'
                )
            else:
                response["Content-Disposition"] = (
                    'inline; filename="performance_report.pdf"'
                )
            return response

        return Response(
            {
                "view_pdf": f"{request.build_absolute_uri()}?response=pdf",
                "download_pdf": f"{request.build_absolute_uri()}?response=pdf&download=true",
                "prediction_metrics": metrics,
                "backtest_result": backtest_result,
            }
        )

    def generate_visualization(self, dates, actual_prices, predicted_prices):
        plt.figure(figsize=(10, 5))
        plt.plot(dates, actual_prices, label="Actual Prices", color="blue")
        plt.plot(dates, predicted_prices, label="Predicted Prices", color="red")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.title("Stock Prices Prediction by Linear Regression")
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.savefig(self.STOCK_PRICES_PREDICTION_PLOT_PATH)
        plt.close()
