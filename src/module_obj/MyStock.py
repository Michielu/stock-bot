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
    sma_window = 16
    roc_length = 14  # has to be a positive number
    history_roc = []
    history_parabolic_trend = []
    history_hl2 = []

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

        # hl2 = self.gen_hl2(high_price, low_price)
        # if hl2 != None:
        #     self.history_hl2.append(hl2)

        pc = self.gen_roc(closing_price)
        if pc != None:
            self.history_roc.append(pc)

        self.history_parabolic_trend.append(
            self.ParabolicTrend.next(high_price, low_price))

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

    # def gen_hl2(self, high, low):
    #     return TOMMICH_HELPER["get_hl2"](high, low)

    def gen_roc(self, closing_price):

        roc = TOMMICH_HELPER["get_roc"](
            closing_price, self.history_price_close, self.roc_length)
        # print("Past rate of change :", roc)

        return roc

    def get_roc(self):
        if len(self.history_roc) > 0:
            return self.history_roc[-1]
        return None

    def get_previous_roc(self):
        if len(self.history_roc) > 1:
            return self.history_roc[-2]
        return None

    def get_parabolic_trend(self):
        if len(self.history_parabolic_trend) > 0:
            return self.history_parabolic_trend[-1]
        return None

    # def get_exp_average(self):
    #     return TOMMICH_HELPER["get_triple_exp_average"]()

# Test
