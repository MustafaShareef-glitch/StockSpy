from flask import Flask, request
import yfinance as yf

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    price_info = ""
    if request.method == 'POST':
        symbol = request.form.get('symbol').upper()
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d")
            price = round(data['Close'][0], 2)
            price_info = f"{symbol} Stock Price: ${price}"
        except:
            price_info = "Error fetching data. Please try again."

    return f"""
        <h1>StockSpy</h1>
        <form method="POST">
            <input name="symbol" placeholder="Enter stock symbol (e.g., AAPL)" required>
            <button type="submit">Check</button>
        </form>
        <h2>{price_info}</h2>
    """

if __name__ == '__main__':
    app.run(debug=True)

