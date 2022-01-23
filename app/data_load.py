import pandas as pd
import yfinance as yf

from datetime import datetime, timedelta


def get_hist_prices(ticker):
    tickers_map = {'BTC': 'BTC-USD', 'ETH': 'ETH-USD', 'S&P500': '^GSPC', 'AAPL': 'AAPL', 
                   'MSFT': 'MSFT', 'AMZN': 'AMZN', 'GOOG': 'GOOG', 'TSLA': 'TSLA'}
    yf_ticker = yf.Ticker(tickers_map[ticker])
    prices = yf_ticker.history(start=datetime.now()-timedelta(100), end=datetime.now())
    prices = prices.reset_index()
    prices['Date'] = pd.to_datetime(prices['Date'], format='%Y-%m-%d')
    prices = prices.set_index('Date')
    prices = prices.interpolate()

    return prices[['Open', 'High', 'Low', 'Close', 'Volume']]