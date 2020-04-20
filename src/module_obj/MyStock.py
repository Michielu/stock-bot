import numpy as np


class MyStock:
    prediction_price = -1
    prediction_error_chance = -1
    prediction_date = -1

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

    def get_data(self):
        return np.array([self.ticker, self.name, self.industry, self.prediction_price, self.prediction_error_chance, self.prediction_date])


# stock1 = MyStock("MMM", "3M Industry", "Manuafactorying")
# print(stock1.getData())
