import joblib
from .features import get_feats


class Forecaster:
    TICKERS = ('BTC', 'ETH', 'S&P500', 'AAPL', 'MSFT', 'AMZN', 'GOOG', 'TSLA')

    def __init__(self):
        self.xgb_models = {}
        self.linreg_models = {}

        for ticker in self.TICKERS:
            self.xgb_models[ticker] = joblib.load(f"models/boost/{ticker}.pk")
            self.linreg_models[ticker] = joblib.load(f"models/linear/{ticker}.pk")

    def forecast(self, df, ticker, model):
        df = get_feats(df)

        if model == "linear":
            X = df[['MA_3','MA_9', 'Upper_shadow', 'Lower_shadow', 'High_div_low', 'Open_sub_close']]
            X = X.iloc[-1].values.reshape(1, -1)
            pred = self.linreg_models[ticker].predict(X)[0]
        elif model == "xgb":
            X = df.drop(['Open_sub_close'], axis=1)
            X_np = X.iloc[-1].values.reshape(1, -1)
            pred = self.xgb_models[ticker].predict(X_np)[0]
            close = X.iloc[-1, X.columns.get_loc('Close')]
            pred = close+(pred*close)

        return pred
