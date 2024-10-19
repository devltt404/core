from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    root_mean_squared_error,
)


def calculate_predictions_metrics(actual_prices, predicted_prices):
    filtered_actual_prices = []
    filtered_predicted_prices = []

    print(actual_prices, predicted_prices)

    for actual, predicted in zip(actual_prices, predicted_prices):
        if actual is not None and predicted is not None:
            filtered_actual_prices.append(actual)
            filtered_predicted_prices.append(predicted)

    return {
        "mean_squared_error": round(
            mean_squared_error(filtered_actual_prices, filtered_predicted_prices), 2
        ),
        "root_mean_squared_error": round(
            root_mean_squared_error(filtered_actual_prices, filtered_predicted_prices),
            2,
        ),
        "mean_absolute_error": round(
            mean_absolute_error(filtered_actual_prices, filtered_predicted_prices), 2
        ),
        "r_squared": round(
            r2_score(filtered_actual_prices, filtered_predicted_prices), 2
        ),
    }
