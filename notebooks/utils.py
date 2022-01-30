import numpy as np
import pandas as pd 
import yfinance as yf 

from sklearn.model_selection import TimeSeriesSplit
from sklearn.model_selection import cross_val_score 


def get_ticker_prices(ticker, start, end):
    yf_ticker = yf.Ticker(ticker)
    prices = yf_ticker.history(start=start, end=end)
    prices = prices.reset_index()
    prices['Date'] = pd.to_datetime(prices['Date'])
    prices = prices.set_index('Date')
    prices = prices.interpolate()
    prices = prices.drop(['Dividends', 'Stock Splits'], axis=1)
    return prices

def timeseries_train_test_split(X, y, test_size):
    test_index = int(len(X) * (1 - test_size))

    X_train = X.iloc[:test_index]
    y_train = y.iloc[:test_index]
    X_test = X.iloc[test_index:]
    y_test = y.iloc[test_index:]

    return X_train, X_test, y_train, y_test

def timeseries_cross_val(estimator, X_train, y_train, n_splits=5):
    tsvc = TimeSeriesSplit(n_splits=n_splits)
    scores = cross_val_score(estimator, X_train, y_train, cv=tsvc, scoring='neg_mean_squared_error')
    return np.sqrt(-scores.mean())