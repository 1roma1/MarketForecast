import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from flask import (
    Blueprint, render_template, request, jsonify
)
from .forecaster import Forecaster

bp = Blueprint('', __name__)
forecaster = Forecaster()


def get_hist_prices(ticker):
    tickers_map = {'BTC': 'BTC-USD', 'ETH': 'ETH-USD', 'S&P500': '^GSPC', 'AAPL': 'AAPL', 
                   'MSFT': 'MSFT', 'AMZN': 'AMZN', 'GOOG': 'GOOG', 'TSLA': 'TSLA'}
    yf_ticker = yf.Ticker(tickers_map[ticker])
    prices = yf_ticker.history(start=datetime.now()-timedelta(100), end=datetime.now()-timedelta(1))
    prices = prices.reset_index()
    prices['Date'] = pd.to_datetime(prices['Date'], format='%Y-%m-%d')
    prices = prices.set_index('Date')
    prices = prices.interpolate()

    return prices[['Open', 'High', 'Low', 'Close', 'Volume']]

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/get_ticker_data', methods=['GET', 'POST'])
def get_ticker_data():
    if request.method == 'GET':
        ticker = request.args.get('ticker', 0, type=str)
        model = request.args.get('model', 1, type=str)

        prices = get_hist_prices(ticker)

        forecast_price = forecaster.forecast(prices, ticker, model)
        prices['Predicted'] = None
        prices.iloc[-1, prices.columns.get_loc('Predicted')] = prices.iloc[-1, prices.columns.get_loc('Close')]

        prices = pd.concat([prices[['Close', 'Predicted']], pd.DataFrame([[None, forecast_price]], columns=['Close', 'Predicted'], index=[datetime.now()])], ignore_index=False)

        prices = prices.reset_index()
        prices['Date'] = prices['index'].map(pd.Timestamp.date).map(str)

        prices = prices[['Date', 'Close', 'Predicted']].values.tolist()
        prices[-1][1] = None

    return jsonify({'prices': prices})
