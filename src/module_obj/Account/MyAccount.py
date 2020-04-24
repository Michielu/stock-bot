# pylint: disable=import-error

import numpy as np
import pandas as pd
from module_obj.StockLog import StockLog
from module_obj.Account.IAccount import IAccount


class MyAccount(IAccount):
    # Array of StockLog objects
    stocks_log_list = []

    def __init__(self, account_value):
        self.buying_power = account_value

    def get_account_value(self):
        invested_in_stocks = 0
        for s in self.stocks_log_list:
            invested_in_stocks += s.get_total_invested()

        return round(invested_in_stocks, 2) + self.buying_power

    def get_buying_power(self):
        return round(self.buying_power, 2)

    # value = price per stock
    def buy_stock(self, ticker, num, value):
        # Check if enough buying power
        if self.buying_power < num*value:
            raise Exception("Error buying stock: Not enough buying power")

        # Check if previous own stock
        for stock_log in self.stocks_log_list:
            if stock_log.get_ticker() == ticker:
                stock_log.buy_stock(num, value)
                return "Bought more"

        self.stocks_log_list.append(StockLog(ticker, num, value))

        self.buying_power -= num*value

        return "Bought"

    def sell_stock(self, ticker, num, value):
        for stock_log in self.stocks_log_list:
            if stock_log.get_ticker() == ticker:
                status = stock_log.sell_stock(num)
                if stock_log.get_num_purchased() == 0:
                    self.stocks_log_list.remove(stock_log)
                # print(status)

        if status != "Successfully sold":
            raise Exception("Error Selling stock")

        self.buying_power += num*value
        return status

    def owned_stock_info(self, ticker):
        for stock_log in self.stocks_log_list:
            if stock_log.get_ticker() == ticker:
                return stock_log.get_data()

        raise Exception("Cannot sell unowned stock")

    def print_summary(self):
        print("")
        print("========================================")
        print("Account Value: ", self.get_account_value())
        print("Buying power: ", self.get_buying_power())

        # convert to dataframe

        if self.stocks_log_list:
            stock_df = pd.DataFrame.from_records(
                [stock_log.get_data() for stock_log in self.stocks_log_list])
            print(stock_df)
        print("========================================")
        print("")
