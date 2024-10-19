import datetime

from django.test import TestCase
from financial_data.models import DailyStock

from .utils import execute_backtest


class BacktestTestCase(TestCase):
    # ---------- HELPER METHODS ----------
    INITIAL_INVESTMENT = 1000

    def create_stock_data(self, prices):
        if len(prices) > 31:  # limit to generate 31 days of data
            raise ValueError("Too many prices")

        for i, price in enumerate(prices):
            DailyStock.objects.create(
                date=datetime.date(2024, 1, i + 1),
                close_price=price,
                # unused fields
                open_price=0,
                high_price=0,
                low_price=0,
                volume=0,
            )

    def call_backtest(self, prices):
        self.create_stock_data(prices)
        result = execute_backtest(
            investment_amount=self.INITIAL_INVESTMENT,
            short_term=2,
            long_term=3,
        )
        print(f"{prices}\n{result}\n")
        return result

    # ----------------------------------------

    def test_basic_case(self):
        result = self.call_backtest([100, 102, 101, 105, 100])

        self.assertIn("investment_amount", result)
        self.assertIn("final_money", result)
        self.assertIn("profit", result)
        self.assertIn("total_return", result)
        self.assertIn("num_trades", result)
        self.assertIn("max_drawdown", result)

        self.assertEqual(result["investment_amount"], self.INITIAL_INVESTMENT)
        self.assertGreaterEqual(result["num_trades"], 0)

    def test_same_prices(self):
        result = self.call_backtest([100, 100, 100, 100, 100])

        self.assertEqual(result["final_money"], 1000)
        self.assertEqual(result["profit"], 0)
        self.assertEqual(result["total_return"], 0)
        self.assertEqual(result["num_trades"], 0)

    def test_downward_trend(self):
        result = self.call_backtest([100, 102, 101, 95, 90, 85, 80])

        self.assertLess(result["final_money"], 1000)
        self.assertLess(result["profit"], 0)
        self.assertLess(result["total_return"], 0)
        self.assertGreater(result["num_trades"], 0)

    def test_upward_trend(self):
        result = self.call_backtest([100, 102, 101, 110, 112, 115, 130])

        self.assertGreater(result["final_money"], 1000)
        self.assertGreater(result["profit"], 0)
        self.assertGreater(result["total_return"], 0)
        self.assertGreater(result["num_trades"], 0)

    def test_small_data(self):
        result = self.call_backtest([100])

        self.assertIn("investment_amount", result)
        self.assertIn("final_money", result)
        self.assertEqual(result["num_trades"], 0)
