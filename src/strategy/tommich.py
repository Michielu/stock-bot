# pylint: disable=import-error
# Test Strat
# Sells all when stock goes down
# Buys when stock goes up
# Initial: just one ticker.
# Later, multiple tickers
import math
from strategy.IStrategy import IStrategy
from enum import Enum
from module_obj.MyStock import MyStock


class ParabolicState(Enum):
    CAN_BUY_ONLY = 1
    CAN_SELL_ONLY = 2
    CANNOT_BUY_OR_SELL = 3


class Tommich(IStrategy):
    __last_closing_price = -1
    __percentage_of_buying_power = .80

    def __init__(self, account, ticker):
        self.account = account
        self.ticker = ticker
        self.__buying_state = ParabolicState.CAN_BUY_ONLY
        self.my_stock = MyStock(ticker, "Full name", "industry")

    def next_data_point(self, ticker, row):
        # Future enhancement: store in appropriate one
        closing_price = math.ceil(row["Close"]*100)/100
        high_price = math.ceil(row["High"]*100)/100
        low_price = math.ceil(row["Low"]*100)/100

        self.my_stock.add_stock_price(closing_price, high_price, low_price)

        simple_moving_avg_long = self.my_stock.get_sma()  # SMALong
        last_simple_moving_avg = self.my_stock.get_previous_sma()  # SMALong[1]
        price_change = self.my_stock.get_price_change()
        last_price_change = self.my_stock.get_previous_price_change()
        parabolic_trend = self.my_stock.get_parabolic_trend()

        if simple_moving_avg_long == None or last_simple_moving_avg == None or price_change == None or parabolic_trend == None:
            print("n", end="", flush=True)
            return None

        if self.__buying_state == ParabolicState.CAN_BUY_ONLY:
            print("b", end="", flush=True)
            if closing_price > simple_moving_avg_long and self.__last_closing_price < last_simple_moving_avg:
                print("BOUGHT!!")
                self.__buying_state = ParabolicState.CAN_SELL_ONLY
        elif self.__buying_state == ParabolicState.CAN_SELL_ONLY:
            print("s", end="", flush=True)
            if price_change < last_price_change and (closing_price < simple_moving_avg_long):
                print("SOLD")
                self.__buying_state = ParabolicState.CAN_BUY_ONLY
        else:
            print("buy or sell")

        self.__last_closing_price = closing_price

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
