import matplotlib
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

matplotlib.use("Agg")


def generate_visualization(path, dates, actual_prices, predicted_prices):
    plt.figure(figsize=(10, 5))

    plt.plot(dates, actual_prices, label="Actual Prices", color="blue")
    plt.plot(dates, predicted_prices, label="Predicted Prices", color="red")

    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title("Stock Prices Prediction by Linear Regression")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(path)
    plt.close()


def draw_text(c, y, text, x=100):
    c.drawString(x, y, text)
    return y - 20


def report_backtest(c, y, backtest_result):
    c.setFont("Helvetica-Bold", 15)
    y = draw_text(c, y, "Backtest Results:")
    c.setFont("Helvetica", 12)

    y = draw_text(c, y, f"Investment Amount: {backtest_result['investment_amount']}")
    y = draw_text(c, y, f"Final Money: {backtest_result['final_money']}")
    y = draw_text(c, y, f"Profit: {backtest_result['profit']}")
    y = draw_text(c, y, f"Total Return: {backtest_result['total_return']}%")
    y = draw_text(c, y, f"Number of Trades: {backtest_result['num_trades']}")
    y = draw_text(c, y, f"Max Drawdown: {backtest_result['max_drawdown']}%")
    return y


def report_ml(c, y, metrics, plot_path):
    c.setFont("Helvetica-Bold", 15)
    y = draw_text(c, y, "Machine Learning Prediction:")
    c.setFont("Helvetica", 12)
    for key, value in metrics.items():
        y = draw_text(
            c, y, f"{key.replace('-', ' ').replace('_', ' ').title()}: {value}"
        )

    c.drawImage(
        plot_path,
        50,
        y - 300,
        width=500,
        height=300,
    )

    y -= 320

    return y


def create_performance_pdf(
    pdf_path, plot_path, actual_prices, predicted_prices, backtest_result, metrics
):
    c = canvas.Canvas(pdf_path, pagesize=letter)

    y = 750

    c.setFont("Helvetica", 20)
    y = draw_text(c, y, "Performance Report")
    y -= 10

    y = report_backtest(c, y, backtest_result)
    y -= 10
    y = report_ml(c, y, metrics, plot_path)

    c.showPage()
    c.save()
