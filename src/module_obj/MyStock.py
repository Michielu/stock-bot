import numpy as np
from util.parabolic_helper import PARABOLIC_HELPER


class MyStock:
    prediction_price = -1
    prediction_error_chance = -1
    prediction_date = -1
    history_price = []
    history_sma = []
    sma_window = 3
    price_change_length = 14  # has to be a positive number
    history_price_change = []

    def __init__(self, ticker, name, industry):
        self.ticker = ticker
        self.name = name
        self.industry = industry

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

    def add_stock_price(self, price):
        self.history_price.append(price)

        sma = self.get_sma(self.sma_window)
        if sma != None:
            self.history_sma.append(sma)

        pc = self.get_price_change(high, low)
        if pc != None:
            self.history_price_change.append(pc)

    def get_sma(self, window):
        # TODO maybe store some placeholder values in sma
        if len(self.history_price) < window:
            return None

        print(window, self.history_price[-window:])
        return PARABOLIC_HELPER["get_sma_balance"](self.history_price[-window:])

    def get_price_change(self, high, low):
        # Test what happens when price_change_length gets an out of index value

        if self.price_change_length <= len(self.history_price_change):
            past_price_change = self.history_price_change[-self.price_change_length]
        else:
            past_price_change = None

        return PARABOLIC_HELPER["get_price_change"](high, low, past_price_change)


# Test
