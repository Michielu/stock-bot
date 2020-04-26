# pylint: disable=import-error, no-name-in-module

from util.graph import Graph
from strategy.tommich import Tommich
from data_source.current import Current
from data_source.history import History
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
    account = RHAccount("mich.menning@gmail.com")

############### Choose Strategy ###############
strat = Tommich(account, "SPY")

if real_time:
    print("Do real time stuff")
    graph_data = {}
    graph_data["SPY"] = []
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


print(account.print_summary())
Graph["graph"](graph_data)
