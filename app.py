from flask import Flask
import yfinance as yf

app = Flask(__name__)

@app.route("/")
def home():
    ticker = yf.Ticker("AAPL")  # Apple stock
    data = ticker.history(period="1d")
    price = round(data['Close'][0], 2)
    return f"Apple Stock Price: ${price}"

if __name__ == '__main__':
    app.run(debug=True)
