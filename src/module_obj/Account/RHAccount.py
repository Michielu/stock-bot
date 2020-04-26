# pylint: disable=import-error

import numpy as np
import pandas as pd
from module_obj.Account.IAccount import IAccount
from data_source.robinhood import Robinhood


class RHAccount(IAccount):
    def __init__(self, email):
        self.rh = Robinhood(email)

    def get_account_value(self):
        return self.rh.get_total_equity()

    def get_buying_power(self):
        return self.rh.get_buying_power()

    # value = price per stock
    def buy_stock(self, ticker, num, value=None):
        if value == None:
            # Build in 5 cents just in case RH increases it's price
            if num*(value+.05) > self.rh.get_buying_power():
                raise Exception("Buying error, not enough buying power")
            return self.rh.order_buy_market(ticker, num)

        else:
            return self.rh.order_buy_limit(ticker, num, value)

    def sell_stock(self, ticker, num=None, value=None):
        if value == None:
            if num == None:
                self.rh.order_sell_market_all(ticker)
            else:
                self.rh.order_sell_market(ticker, num)

        else:
            if num == None:
                self.rh.order_sell_limit(
                    ticker, self.rh.get_num_stock_own(ticker), value)
            else:
                self.rh.order_sell_limit(ticker, num, value)

    def owned_stock_info(self, ticker):
        return self.rh.get_stock_info(ticker)

    def print_summary(self):
        print("")
        print("========================================")
        print("Account Value: ", self.rh.get_total_equity())
        print("Buying power: ", self.rh.get_buying_power())
        print(self.rh.refresh_holdings())
        print("========================================")
        print("")
