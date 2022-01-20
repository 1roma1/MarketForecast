import numpy as np
import pandas as pd 


def rolling_mean(series, window):
    return series.rolling(window).mean()

def ewma(series, span, min_periods):
    return series.ewm(span=span, min_periods=min_periods).mean()

def moving_average(df, n):
    ma = pd.Series(rolling_mean(df['Close'], n), name = 'MA_' + str(n))
    return ma

def exp_moving_average(df, n):
    ema = pd.Series(ewma(df['Close'], span=n, min_periods=n-1), name='EMA_' + str(n))
    return ema

def vol_moving_average(df, n):
    vma = pd.Series(rolling_mean(df['Volume'], n), name = 'VMA_' + str(n))
    return vma

def upper_shadow(df): 
    return df['High'] - np.maximum(df['Close'], df['Open'])

def lower_shadow(df): 
    return np.minimum(df['Close'], df['Open']) - df['Low']

def realized_vol(df, n):
    returns = np.log(df['Close']/df['Close'].shift(1))
    volatility = returns.rolling(window=n).std(ddof=0)*np.sqrt(252)
    return volatility

def get_feats(df):
    df['MA_3'] = moving_average(df, 3)
    df['MA_9'] = moving_average(df, 9)

    df['EMA_3'] = exp_moving_average(df, 3)
    df['EMA_9'] = exp_moving_average(df, 9)

    df['VMA_3'] = vol_moving_average(df, 3)
    df['VMA_9'] = vol_moving_average(df, 9)

    df['Upper_shadow'] = upper_shadow(df)
    df['Lower_shadow'] = lower_shadow(df)

    df['High_div_low'] = df['High'] / df['Low']
    df['Open_sub_close'] = df['Open'] - df['Close']

    df['Realized_vol'] = realized_vol(df, 30)

    return df.dropna()