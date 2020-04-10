import numpy as np


class MyStock:
    futurePrice = 0

    def __init__(self, ticker, name, industry):
        self.ticker = ticker
        self.name = name
        self.industry = industry

    def getTicker(self):
        return self.ticker

    def getName(self):
        return self.name

    def getIndustry(self):
        return self.industry

    def getData(self):
        return np.array([self.ticker, self.name, self.industry])


# stock1 = MyStock("MMM", "3M Industry", "Manuafactorying")
# print(stock1.getData())
