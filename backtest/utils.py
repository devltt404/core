import numpy as np
import pandas as pd

from financial_data.models import DailyStock


def get_max_drawdown(values):
    rolling_max = np.maximum.accumulate(values)
    daily_drawdown = (values - rolling_max) / rolling_max
    max_drawdown = daily_drawdown.min()

    return max_drawdown


def get_moving_average(arr, period):
    return arr.rolling(window=period).mean()


def execute_backtest(investment_amount, short_term, long_term):
    stock_data = (
        DailyStock.objects.values("date", "close_price")
        .filter(close_price__isnull=False)
        .order_by("date")
    )
    df = pd.DataFrame(stock_data)

    df["short_ma"] = get_moving_average(df["close_price"], short_term)
    df["long_ma"] = get_moving_average(df["close_price"], long_term)

    cash = investment_amount
    num_trades = 0
    shares = 0
    portofolio_values = [investment_amount]

    # Execute trading strategy
    for i in range(1, len(df)):
        price = df["close_price"][i]
        short_ma = df["short_ma"][i]
        long_ma = df["long_ma"][i]

        # Buy: stock price dips below short-term moving average
        if price < short_ma and cash > 0:
            shares = cash / price
            cash = 0
            num_trades += 1

        # Sell: stock price rises above long-term moving average
        elif price > long_ma and shares > 0:
            cash = shares * price
            shares = 0
            num_trades += 1

        portofolio_values.append(cash + shares * price)

    final_money = cash + shares * df["close_price"].iloc[-1]
    profit = final_money - investment_amount

    return {
        "investment_amount": investment_amount,
        "short_term": short_term,
        "long_term": long_term,
        "final_money": round(final_money, 2),
        "profit": round(profit, 2),
        "total_return": round((profit) / investment_amount * 100, 2),
        "num_trades": num_trades,
        "max_drawdown": round(get_max_drawdown(portofolio_values) * 100, 2),
    }
