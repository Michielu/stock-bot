# pylint: disable=no-name-in-module, import-error

import numpy as np
import math
from util.tommich_helper import TOMMICH_HELPER
from module_obj.ParabolicTrend import ParabolicTrend


class MyStock:
    history_price_open = []
    history_price_high = []
    history_price_low = []
    history_price_close = []
    history_sma = []
    history_wma = []
    sma_window = 16
    wma_window = 10
    roc_length = 2  # has to be a positive number
    history_roc = []
    history_parabolic_trend = []
    history_hl2 = []
    history_ohlc4 = []
    tema_long = 7
    tema_short = 1
    tema_boundry = 1
    history_tema_short = []
    history_tema_long = []
    history_tema_boundry = []
    history_trend_quality = []
    fast_length = 7  # TrendQuality (1-50), first "fast_length"
    slow_length = 15
    history_reversal = []

    def __init__(self, ticker):
        self.ticker = ticker
        self.ParabolicTrend = ParabolicTrend(.05)

    def get_ticker(self):
        return self.ticker

    def get_history_sma(self):
        return self.history_sma

    def add_stock_price(self, price_row):
        # dataframe: "Open", "High", "Low", "Close", "Adj Close", "Volumn"
        # TODO store
        # self.history_price_open
        open_price = math.ceil(price_row["Open"]*100)/100
        high_price = math.ceil(price_row["High"]*100)/100
        low_price = math.ceil(price_row["Low"]*100)/100
        closing_price = math.ceil(price_row["Close"]*100)/100
        # print(open_price, high_price, low_price, closing_price, price_row)
        # self.history_price.append(price)
        self.history_price_open.append(open_price)
        self.history_price_high.append(high_price)
        self.history_price_low.append(low_price)
        self.history_price_close.append(closing_price)

        sma = self.gen_sma(self.sma_window)
        if sma != None:
            self.history_sma.append(sma)

        hl2 = self.gen_hl2(high_price, low_price)
        if hl2 != None:
            self.history_hl2.append(hl2)
            self.history_wma.append(self.gen_wma())

        self.history_ohlc4.append(self.gen_ohlc4(
            open_price, high_price, low_price, closing_price))

        pc = self.gen_roc()
        if pc != None:
            self.history_roc.append(pc)

        self.history_parabolic_trend.append(
            self.ParabolicTrend.next(high_price, low_price))

        self.history_tema_short.append(self.gen_exp_average(
            self.history_ohlc4, self.tema_short))
        self.history_tema_long.append(self.gen_exp_average(
            self.history_ohlc4, self.tema_long))
        self.history_tema_boundry.append(
            self.gen_exp_average(self.history_price_close, self.tema_boundry))

        self.history_reversal.append(self.gen_reversal())

    def gen_sma(self, window):
        # TODO maybe store some placeholder values in sma
        if len(self.history_price_close) < window:
            return None

        return TOMMICH_HELPER["get_sma_balance"](self.history_price_close[-window:])

    def get_sma(self):
        if len(self.history_sma) > 0:
            return self.history_sma[-1]
        return None

    def get_previous_sma(self):
        if len(self.history_sma) > 1:
            return self.history_sma[-2]
        return None

    def gen_wma(self):
        if len(self.history_hl2) > 0:
            return TOMMICH_HELPER["get_weighted_moving_avg"](self.history_hl2, self.wma_window)
        raise ValueError('self.history_hl2 can never be empty')

    def get_wma(self):
        return self.history_wma[-1]

    def gen_hl2(self, high, low):
        return TOMMICH_HELPER["get_hl2"](high, low)

    def gen_ohlc4(self, open, high, low, close):
        return (open+high+low+close)/4

    def get_ohlc4(self):
        return self.history_ohlc4[-1]

    def gen_roc(self):
        roc = TOMMICH_HELPER["get_roc"](
            self.history_price_close, self.roc_length)
        # print("Past rate of change :", roc)

        return roc

    def get_roc(self, previous=-1):
        if len(self.history_roc) >= abs(previous):
            return self.history_roc[previous]
        return None

    def get_difference_roc(self):
        if len(self.history_roc) > 2:
            return self.history_roc[-1] - self.history_roc[-2]
        return 0

    def get_previous_roc(self):
        if len(self.history_roc) > 1:
            return self.history_roc[-2]
        return None

    def get_parabolic_trend(self):
        if len(self.history_parabolic_trend) > 0:
            return self.history_parabolic_trend[-1]
        return 0  # We're using this value to subtract

    def gen_exp_average(self, data, window):
        return TOMMICH_HELPER["get_triple_exp_average"](data[-window:], window)[-1]

    def get_tema_long(self, previous=-1):
        if len(self.history_tema_long) >= abs(previous):
            return self.history_tema_long[previous]
        return None

    def get_tema_short(self, previous=-1):
        if len(self.history_tema_short) >= abs(previous):
            return self.history_tema_short[previous]
        return None

    def get_tema_boundry(self):
        return self.history_tema_boundry[-1]

    def gen_reversal(self):
        hist_length = len(self.history_price_close)
        fast_l = self.fast_length if hist_length >= self.fast_length else hist_length
        slow_l = self.slow_length if hist_length >= self.slow_length else hist_length
        return TOMMICH_HELPER["calc_trend_period"](self.history_price_close, fast_l, slow_l)

    def get_reversal(self):
        return self.history_reversal[-1]

    def reset_all(self):
        self.history_price_open = []
        self.history_price_high = []
        self.history_price_low = []
        self.history_price_close = []
        self.history_sma = []
        self.history_roc = []
        self.history_parabolic_trend = []
        self.history_hl2 = []
        self.history_ohlc4 = []
        self.history_tema_short = []
        self.history_tema_long = []
        self.history_tema_boundry = []
        self.history_trend_quality = []
        self.history_reversal = []
        self.history_wma = []

    # def gen_trend_quality(self):
    #     noise = self.correction_factor *

# Test
