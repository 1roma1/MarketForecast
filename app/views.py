import pandas as pd
import numpy as np
import yfinance as yf

from flask import (
    Blueprint, render_template
)


bp = Blueprint('', __name__)


def get_hist_prices(ticker):
    yf_ticker = yf.Ticker(ticker)
    prices = yf_ticker.history(start='2020-01-01', end='2022-01-16')
    prices = prices.reset_index()
    prices['Date'] = pd.to_datetime(prices['Date'])
    prices = prices.set_index('Date')
    prices = prices.interpolate()
    prices = prices.drop(['Dividends', 'Stock Splits'], axis=1)

    return prices

@bp.route('/')
def index():
    prices = get_hist_prices('AAPL')

    data = np.c_[np.arange(1, prices.shape[0] + 1).reshape(-1, 1),
                             prices['Close'].values.reshape(-1, 1)].tolist()
    return render_template('index.html', data=data)
