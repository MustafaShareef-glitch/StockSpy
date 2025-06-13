from flask import Flask, render_template, request
import yfinance as yf
import plotly.graph_objs as go
import plotly.offline as pyo

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    chart_html = None
    if request.method == 'POST':
        symbol = request.form['symbol'].upper()
        data = yf.download(symbol, period='7d', interval='1d')
        
        if not data.empty:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines+markers', name='Close Price'))
            fig.update_layout(title=f'{symbol} Price - Last 7 Days', xaxis_title='Date', yaxis_title='Price')
            chart_html = pyo.plot(fig, output_type='div')

    return render_template('index.html', chart_html=chart_html)

if __name__ == '__main__':
    app.run(debug=True)

