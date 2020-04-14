import numpy as np


class StockLog:
    def __init__(self, ticker, num, value):
        self.ticker = ticker
        self.num_purchased = num
        self.avg_price = value

    def get_ticker(self):
        return self.ticker

    def buy_stock(self, num, price):
        if self.num_purchased == 0:
            self.num_purchased = num
            self.avg_price = price
            return

        total_investment = self.avg_price*self.num_purchased + num * price
        self.num_purchased += num
        self.avg_price = total_investment/self.num_purchased
        return

    def sell_stock(self, num):
        if num > self.num_purchased:
            return "Not enough stocks to sell"

        self.num_purchased -= num
        return "Successfully sold"

    def get_num_purchased(self):
        return self.num_purchased

    def get_total_invested(self):
        return self.num_purchased * self.avg_price

    def get_data(self):
        return {"ticker": self.ticker,
                "num": self.num_purchased,
                "avg": self.avg_price}


# stock1 = MyStock("MMM", "3M Industry", "Manuafactorying")
# print(stock1.getData())
