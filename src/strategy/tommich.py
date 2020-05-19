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
    __roc_amplifier = 3
    __diff_roc_value_buy = .004
    # 5 is personal factor to offset difference in tq from thinkorswim
    __trend_quality_buy = 6 / 5
    __trend_quality_sell = 8 / 5

    def __init__(self, account, ticker):
        self.account = account
        self.ticker = ticker
        self.__buying_state = ParabolicState.CAN_BUY_ONLY
        self.my_stock = MyStock(ticker)

    def next_data_point(self, ticker, row, date_time):
        # Future enhancement: store in appropriate one
        closing_price = math.ceil(row["Close"]*100)/100
        self.my_stock.add_stock_price(row)

        in_freeze = self.in_freeze(date_time)
        if in_freeze == FreezeState.WAIT:
            print("in freeze")
        elif in_freeze == FreezeState.SELL_ALL:
            self.my_stock.reset_all()
            if self.__buying_state == ParabolicState.CAN_SELL_ONLY:
                self.__buying_state = ParabolicState.CAN_BUY_ONLY
                self.__sell(ticker, closing_price)
        else:
            TEMA_short = self.my_stock.get_tema_short()  # +1
            TEMA_long = self.my_stock.get_tema_long()  # +1
            TEMA_short_previous = self.my_stock.get_tema_short(-2)  # +0
            TEMA_long_previous = self.my_stock.get_tema_long(-2)  # +0
            TEMA_boundry = self.my_stock.get_tema_boundry()  # +1
            roc = self.my_stock.get_roc()  # +1
            difference_roc = self.my_stock.get_difference_roc()  # +1
            last_roc = self.my_stock.get_previous_roc()  # +1
            wma = self.my_stock.get_wma()  # +1
            trend_quality = self.my_stock.get_tq()

            # Old values
            # simple_moving_avg_long = self.my_stock.get_sma()  # SMALong
            # last_simple_moving_avg = self.my_stock.get_previous_sma()
            # parabolic_trend = self.my_stock.get_parabolic_trend()

            if self.__buying_state == ParabolicState.CAN_BUY_ONLY:
                # print("b", end="", flush=True)
                if TEMA_short > TEMA_long and TEMA_short_previous <= TEMA_long_previous \
                        and TEMA_short <= TEMA_boundry \
                        and (roc >= (last_roc * self.__roc_amplifier)) \
                        and (difference_roc >= self.__diff_roc_value_buy or difference_roc <= -self.__diff_roc_value_buy) \
                        and trend_quality > -self.__trend_quality_buy:
                    # print("BOUGHT!!")
                    self.__buying_state = ParabolicState.CAN_SELL_ONLY
                    self.__buy(ticker, closing_price)
            elif self.__buying_state == ParabolicState.CAN_SELL_ONLY:
                # print("s", end="", flush=True)
                if (TEMA_short < TEMA_long and wma) or \
                    ((difference_roc >= self.__diff_roc_value_buy or difference_roc <= -self.__diff_roc_value_buy
                      and roc < last_roc)) \
                        or trend_quality > self.__trend_quality_sell:
                    # print("SOLD")
                    self.__buying_state = ParabolicState.CAN_BUY_ONLY
                    self.__sell(ticker, closing_price)

            else:
                print("buy or sell")

        self.__last_closing_price = closing_price

        return self.account.get_account_value()
        # return self.my_stock.get_tq()

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
