


from flask import Flask, request, render_template
import yfinance as yf
import plotly.graph_objs as go
import plotly.io as pio

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    price_info = ""
    chart_html = ""

    if request.method == 'POST':
        symbol = request.form.get('symbol').upper()
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="7d")
            if not data.empty:
                latest_price = round(data['Close'][-1], 2)
                price_info = f"{symbol} Stock Price: ${latest_price}"

                fig = go.Figure()
                fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name=symbol))
                fig.update_layout(title=f"{symbol} - Last 7 Days", xaxis_title='Date', yaxis_title='Price ($)')
                chart_html = pio.to_html(fig, full_html=False)
            else:
                price_info = "No data available for this symbol."
        except:
            price_info = "Error fetching data. Please try again."

    return render_template("home.html", price_info=price_info, chart_html=chart_html)

if __name__ == '__main__':
    app.run(debug=True)
