# Test Strat
# Sells all when stock goes down
# Buys when stock goes up
# Current: just one ticker.
import math


class PracticeStrat:
    last_price = -1
    __percentage_of_buying_power = .50
    __holding_stock = False

    def __init__(self, account, ticker):
        self.account = account
        self.ticker = ticker

    def next_data_point(self, ticker, row):
        price = math.ceil(row["Close"]*100)/100

        if self.last_price == -1:
            self.last_price = price
            return self.account.get_account_value()

        if price > self.last_price:
            if self.__holding_stock == False:
                self.__buy(ticker, price)
                self.__holding_stock = True
        else:
            if self.__holding_stock == True:
                self.__sell(ticker, price)
                self.__holding_stock = False

        self.last_price = price
        return self.account.get_account_value()

    def __buy(self, ticker, price):
        buying_power = self.account.get_buying_power()
        # Calculate how much to spend
        num_buy = round(
            (buying_power * self.__percentage_of_buying_power)/price, 0)
        self.account.buy_stock(ticker, num_buy, price)

    def __sell(self, ticker, price):
        num_owned = self.account.owned_stock_info(ticker)['num']
        self.account.sell_stock(ticker, num_owned, price)
        # print("Sold, new account balance: ", self.account.get_buying_power())
