# pylint: disable=import-error, no-name-in-module
# https://towardsdatascience.com/stock-analysis-in-python-a0054e2c1a4c
# Issue with Catalina OS https://github.com/tensorflow/tensorflow/issues/33183
# Another solution: https://apple.stackexchange.com/questions/237430/how-to-install-specific-version-of-python-on-os-x/319675#319675
# yfinance limit: 2000 calls/hour
# Robinhood: https://github.com/JGrauPirozzi/robinhood
from util.graph import Graph
from test.test_account import test_account
from strategy.practice import PracticeStrat
from strategy.tommich import Tommich
from strategy.stop_loss import Strategy
from data_source.current import Current
from data_source.history import History
from module_obj.MyStock import MyStock
from module_obj.Account.RHAccount import RHAccount
from module_obj.Account.MyAccount import MyAccount
import pandas as pd
import numpy as np
import yfinance as yf
import time


real_brokerage = False
real_time = False

time_frame = "5d"

############### Choose Account ###############
account = MyAccount(2500)
if real_brokerage:
    account = RHAccount(20000)  # TODO won't be inputting value

############### Choose Strategy ###############
# strat = PracticeStrat(account, "SPY")
strat = Tommich(account, "SPY")

if real_time:
    print("Do real time stuff")
    graph_data = {}
    graph_data["SPY"] = []  # data_df["Close"]
    graph_data["Account"] = []

    # TODO make it only run during market hours
    while True:
        current_price = Current["get_current_price"]("SPY")
        account_balance = strat.next_data_point(
            "SPY", current_price, pd.datetime.now())
        graph_data["Account"].append(account_balance)
        graph_data["SPY"].append(current_price)
        print("Graph_data: ", graph_data)
        time.sleep(60)

else:
    # Execute Strategy
    # data_df = History["get_data"]("SPY", time_frame)
    data_df = History["tommich_test_data"]("SPY")
    graph_data = {}
    graph_data["Account"] = []
    for index, row in data_df.iterrows():
        account_balance = strat.next_data_point("SPY", row, index)
        graph_data["Account"].append(account_balance)


print("FINISHED!")
print(account.print_summary())
# print("Graph data", graph_data)
Graph["graph"](graph_data)


# day_data_df = History["get_week_data"]("SPY")
# print(type(day_data_df))
# print(day_data_df[["Close"]])
# Graph["volume_graph"](day_data_df)
