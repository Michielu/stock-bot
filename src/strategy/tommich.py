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


class FreezeState(Enum):
    SELL_ALL = 1
    WAIT = 2
    NO_FREEZE = 3


class Tommich(IStrategy):
    __last_closing_price = -1
    __percentage_of_buying_power = .9  # changing this causes some problems

    def __init__(self, account, ticker):
        self.account = account
        self.ticker = ticker
        self.__buying_state = ParabolicState.CAN_BUY_ONLY
        self.my_stock = MyStock(ticker, "Full name", "industry")

    def next_data_point(self, ticker, row, date_time):
        # Future enhancement: store in appropriate one
        closing_price = math.ceil(row["Close"]*100)/100
        high_price = math.ceil(row["High"]*100)/100
        low_price = math.ceil(row["Low"]*100)/100

        self.my_stock.add_stock_price(closing_price, high_price, low_price)

        in_freeze = self.in_freeze(date_time)

        if in_freeze == FreezeState.WAIT:
            print("in freeze")
        elif in_freeze == FreezeState.SELL_ALL:
            if self.__buying_state == ParabolicState.CAN_SELL_ONLY:
                self.__buying_state = ParabolicState.CAN_BUY_ONLY
                self.__sell(ticker, closing_price)
        else:
            simple_moving_avg_long = self.my_stock.get_sma()  # SMALong
            last_simple_moving_avg = self.my_stock.get_previous_sma()
            roc = self.my_stock.get_roc()
            last_roc = self.my_stock.get_previous_roc()
            parabolic_trend = self.my_stock.get_parabolic_trend()

            if simple_moving_avg_long == None or last_simple_moving_avg == None or roc == None or parabolic_trend == None:
                # print("n", end="", flush=True)
                return None

            if self.__buying_state == ParabolicState.CAN_BUY_ONLY:
                # print("b", end="", flush=True)
                if closing_price > simple_moving_avg_long and self.__last_closing_price < last_simple_moving_avg:
                    # print("BOUGHT!!")
                    self.__buying_state = ParabolicState.CAN_SELL_ONLY
                    self.__buy(ticker, closing_price)
            elif self.__buying_state == ParabolicState.CAN_SELL_ONLY:
                # print("s", end="", flush=True)
                # print("s", roc, last_roc,
                #       closing_price, simple_moving_avg_long)
                if roc < last_roc and (closing_price < simple_moving_avg_long):
                    # print("SOLD")
                    self.__buying_state = ParabolicState.CAN_BUY_ONLY
                    self.__sell(ticker, closing_price)

            else:
                print("buy or sell")

        self.__last_closing_price = closing_price
        return self.account.get_account_value()

    def __buy(self, ticker, price):
        buying_power = self.account.get_buying_power()
        # Calculate how much to spend
        num_buy = math.floor(
            (buying_power * self.__percentage_of_buying_power)/price)
        self.account.buy_stock(ticker, num_buy, price)

    def __sell(self, ticker, price):
        num_owned = self.account.owned_stock_info(ticker)['num']
        self.account.sell_stock(ticker, num_owned, price)

    def in_freeze(self, date):
        # print(date.hour, " ", date.minute)
        h = date.hour
        m = date.minute

        if h == 15 and m >= 50:
            return FreezeState.SELL_ALL

        if h == 9 and m < 40:
            # Between 9:30et -9:40et
            return FreezeState.WAIT

        return FreezeState.NO_FREEZE
