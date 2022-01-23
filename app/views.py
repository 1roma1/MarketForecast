import pandas as pd
from datetime import datetime, timedelta

from flask import (
    Blueprint, render_template, request, jsonify
)
from .forecaster import Forecaster
from .data_load import get_hist_prices

bp = Blueprint('', __name__)
forecaster = Forecaster()


def prep_data(prices, predicted_price):
    prices['Predicted'] = None
    prices.iloc[-1, prices.columns.get_loc('Predicted')] = prices.iloc[-1, prices.columns.get_loc('Close')]
    prices = pd.concat([prices[['Close', 'Predicted']], 
                        pd.DataFrame([[None, predicted_price]], 
                                     columns=['Close', 'Predicted'], 
                                     index=[datetime.now()+timedelta(1)])], 
                        ignore_index=False)

    prices = prices.reset_index()
    prices['Date'] = prices['index'].map(pd.Timestamp.date).map(str)
    prices = prices[['Date', 'Close', 'Predicted']].values.tolist()
    prices[-1][1] = None

    return prices

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/get_ticker_data', methods=['GET', 'POST'])
def get_ticker_data():
    if request.method == 'GET':
        ticker = request.args.get('ticker', 0, type=str)
        model = request.args.get('model', 1, type=str)

        prices = get_hist_prices(ticker)
        predicted_price = forecaster.forecast(prices, ticker, model)
        prices = prep_data(prices, predicted_price)

    return jsonify({'prices': prices})
