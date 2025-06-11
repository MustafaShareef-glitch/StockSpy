from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import requests
import os

app = Flask(__name__)
API_KEY = '2VPCYBRE9XU740RE'

# SQLite Database Setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///watchlist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# DB model
class Watchlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), unique=True, nullable=False)

# Create DB if not exists
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    stock_data = None
    chart_data = None
    error = None

    if request.method == 'POST':
        symbol = request.form['symbol'].upper()
        action = request.form['action']

        if action == 'add':
            if not Watchlist.query.filter_by(symbol=symbol).first():
                new_stock = Watchlist(symbol=symbol)
                db.session.add(new_stock)
                db.session.commit()
        elif action == 'search':
            quote_url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}'
            quote_data = requests.get(quote_url).json()

            chart_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'
            chart_data_json = requests.get(chart_url).json()

            try:
                quote = quote_data['Global Quote']
                stock_data = {
                    'symbol': quote['01. symbol'],
                    'price': quote['05. price'],
                    'timestamp': quote['07. latest trading day']
                }

                time_series = chart_data_json['Time Series (Daily)']
                dates = list(time_series.keys())[:10][::-1]
                prices = [float(time_series[date]['4. close']) for date in dates]
                chart_data = {'dates': dates, 'prices': prices}
            except (KeyError, TypeError):
                error = f"Could not fetch data for symbol: {symbol}"

    # Fetch watchlist from DB
    saved_stocks = [s.symbol for s in Watchlist.query.all()]
    return render_template('home.html', stock_data=stock_data, chart_data=chart_data, error=error, watchlist=saved_stocks)

if __name__ == '__main__':
    app.run(debug=True)




