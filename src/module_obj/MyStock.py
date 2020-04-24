# pylint disable=no-name-in-module
import numpy as np
from util.tommich_helper import TOMMICH_HELPER
from module_obj.ParabolicTrend import ParabolicTrend


class MyStock:
    prediction_price = -1
    prediction_error_chance = -1
    prediction_date = -1
    history_price = []
    history_sma = []
    sma_window = 16
    roc_length = 14  # has to be a positive number
    history_roc = []
    history_parabolic_trend = []
    history_hl2 = []

    def __init__(self, ticker, name, industry):
        self.ticker = ticker
        self.name = name
        self.industry = industry
        self.ParabolicTrend = ParabolicTrend(.05)

    def get_ticker(self):
        return self.ticker

    def get_name(self):
        return self.name

    def get_industry(self):
        return self.industry

    def set_predictions(self, p):
        self.predictionPrice = p[0]
        self.predictionErrorChance = p[1]
        self.predictionDate = p[2]

    def get_prediction_price(self):
        return self.predictionPrice

    def get_prediction_error_chance(self):
        return self.predictionErrorChance

    def get_prediction_date(self):
        return self.predictionDate

    def get_history_price(self):
        return self.history_price

    def get_history_sma(self):
        return self.history_sma

    def get_data(self):
        return np.array([self.ticker, self.name, self.industry, self.prediction_price, self.prediction_error_chance, self.prediction_date])

    def add_stock_price(self, price, high, low):
        # dataframe: "Open", "High", "Low", "Close", "Adj Close", "Volumn"
        self.history_price.append(price)

        sma = self.gen_sma(self.sma_window)
        if sma != None:
            self.history_sma.append(sma)

        # hl2 = self.gen_hl2(high, low)
        # if hl2 != None:
        #     self.history_hl2.append(hl2)

        pc = self.gen_roc(price)
        if pc != None:
            self.history_roc.append(pc)

        self.history_parabolic_trend.append(
            self.ParabolicTrend.next(high, low))

    def gen_sma(self, window):
        # TODO maybe store some placeholder values in sma
        if len(self.history_price) < window:
            return None

        return TOMMICH_HELPER["get_sma_balance"](self.history_price[-window:])

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
            closing_price, self.history_price, self.roc_length)
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

# Test
