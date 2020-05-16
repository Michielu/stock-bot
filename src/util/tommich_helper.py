import numpy as np
import pandas as pd

data_set = [1, 5, 7, 8, 2, 4, 12, 6, 92, 2, 0]
data_set2 = [1, 2, 3]
data_set3 = [1, 1, 1, 1, 11, 22, 33, 444, 55]


def simple_moving_avg(values, window):
    # window = len(values)
    weights = np.repeat(1.0, window)/window
    # if window is 3: weights = [.33,.33,.33]
    smas = np.convolve(values, weights, 'valid')
    return smas


def get_sma_balance(values, window=-1):
    new_window = window if window > len(values) else len(values)
    weight = 1/new_window
    return sum(values[new_window:])*weight


def get_weighted_moving_avg(values, length):
    num_avalable = len(values) if len(values) < length else length
    weights = list(range(1, num_avalable+1))
    wmas = np.average(values[-num_avalable:], weights=weights)
    return wmas


def get_roc(history_closing, roc_length):
    # ThinkorSwim "2"(roc_length) gets [...,6,7] Our history currently has [...,6,7,8]
    new_length = roc_length + 1
    # print("PC: ", closing_price,  history_roc)
    if roc_length < 0:
        return None

    if new_length > len(history_closing):
        return 0
    else:
        return ((history_closing[-1]/history_closing[-new_length]) - 1) * 100


def get_hl2(high, low):
    if low == 0:
        return None
    return round((high+low)/2, 2)


def get_triple_exp_average(data, window):
    # data: array
    # 3 * ema1 - 3 * ema2 + ema3;
    ea1 = calc_exp_average(data, window)
    ea2 = calc_exp_average(ea1, window)
    ea3 = calc_exp_average(ea2, window)

    for i in range(len(data)):
        ea3[i] = 3*ea1[i] - 3*ea2[i] + ea3[i]

    return ea3


def calc_exp_average(data, window):
    d = {'col1': data}
    df = pd.DataFrame(data=d)
    df["expAvg"] = df['col1'].ewm(span=window, adjust=True).mean()

    return df['expAvg'].values


def calc_trend_quality():
    # ThinkOrSwim's TrendQuality
    # Don't change
    trend_length = 4
    correction_factor = 2

    smf = 2 / (1 + trend_length)
    # TODO store reversal in myStock and pass them in
    # reversal = TrendPeriods(fast_length, slow_length)
    # cpc = if isNaN(reversal[1]) then 0 else if reversal[1] != reversal then 0 else cpc[1] + close - close[1]
    # trend = if isNaN(reversal[1]) then 0 else if reversal[1] != reversal then 0 else trend[1] * (1 - smf) + cpc * smf

    # diff = AbsValue(cpc - trend)
    # noise = correctionFactor * Average(diff, noiseLength)


def calc_trend_period(close, fast_length, slow_length):
    # Sign: Returns the algebraic sign of a number: 1 if the number is positive, 0 if zero and -1 if negative.
    # sign(ExpAverage(close, fastLength) - ExpAverage(close, slowLength))
    fast_tp = calc_exp_average(close[-fast_length:], fast_length)
    slow_tp = calc_exp_average(close[-slow_length:], slow_length)
    period = fast_tp[-1]-slow_tp[-1]
    if period >= 0:
        return 1
    else:
        return -1


def find_last_valid(data, invalid=0):
    if len(data) == 0:
        return 0
    return data[-1] if data[-1] != invalid else find_last_valid(data[:-1])


TOMMICH_HELPER = {
    "get_sma_balance": get_sma_balance,
    "get_weighted_moving_avg": get_weighted_moving_avg,
    "get_roc": get_roc,
    "get_hl2": get_hl2,
    "get_triple_exp_average": get_triple_exp_average,
    "calc_trend_period": calc_trend_period,
    "find_last_valid": find_last_valid
}
