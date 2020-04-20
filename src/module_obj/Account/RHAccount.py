# pylint: disable=import-error

import numpy as np
import pandas as pd
from module_obj.Account.IAccount import IAccount

# TODO change this to get RH account

# Keep the same function names. Same as MyAccount


class RHAccount(IAccount):
    # {ticker: [num, average_price]}
    stock_own = {}

    def __init__(self, account_value):
        self.buying_power = account_value

    def get_account_value(self):
        # Iterate through stock
        invested_stocks = 0
        for s in self.stock_own:
            num_price = self.stock_own[s]
            invested_stocks += num_price[0]*num_price[1]

        print("Invested : ", invested_stocks,
              "Buying power: ", self.buying_power)
        return invested_stocks + self.buying_power

    def get_buying_power(self):
        return self.buying_power

    # value = price per stock
    def buy_stock(self, ticker, num, value):
        # Check if enough buying power

        if ticker in self.stock_own:
            stock_revenue = self.stock_own[ticker]
            total_investment = stock_revenue[0] * \
                stock_revenue[1] + (num*value)
            total_num = stock_revenue[0] + num
            average = total_investment / total_num
            self.stock_own[ticker] = [total_num, average]
        else:
            self.stock_own[ticker] = [num, value]

        self.buying_power -= num*value

        print("Buying ", num, " of ", ticker, " for ", value, "/each")
        return self.stock_own

    # value = price selling each stock
    def sell_stock(self, ticker, num, value):
        # Check if ticker isn't owned

        # Don't calculate new average
        # owned_after = self.stock_own[ticker][0] - num
        # # calculate new average
        # before_sell_amount_invested = self.stock_own[ticker][0] * \
        #     self.stock_own[ticker][1]
        # after_sell_amount_invested = before_sell_amount_invested - \
        #     (num * value)
        # print(before_sell_amount_invested, " ", after_sell_amount_invested)
        # new_average = after_sell_amount_invested / owned_after

        if(self.stock_own[ticker][0] == num):
            del self.stock_own[ticker]
            print("Sold all (", num, ") ", ticker, " for ", num*value)
        else:
            self.stock_own[ticker][0] -= num
            print("Sold ", num, " ", ticker, " for ", num*value)

        self.buying_power += num*value

    def owned_stock_info(self, ticker):
        for stock_log in self.stocks_log_list:
            if stock_log.get_ticker() == ticker:
                return stock_log.get_data()

    def print_summary(self):
        print("")
        print("========================================")
        print("Account Value: ", self.get_account_value())
        print("Buying power: ", self.buying_power)
        if self.stock_own:
            stock_df = pd.DataFrame(self.stock_own)
            print(stock_df)
        print("========================================")
        print("")
