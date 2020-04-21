# pylint: disable=no-name-in-module

from util.graph import Graph
from data_source.history import History
from module_obj.ParabolicTrend import ParabolicTrend
import math

# To Test: check with ThinkOrSwim's script and compare graphs
# Also make sure that History is set to the same date/time frequency
parabolic_data = History["parabotic_test_data"]("SPY", "2020-04-15")
pt = ParabolicTrend(.05)

line_plot_data = []
scatter_plot_data = []

for index, row in parabolic_data.iterrows():
    high = math.ceil(row["High"]*100)/100
    low = math.ceil(row["Low"]*100)/100
    close = math.ceil(row["Close"]*100)/100
    line_plot_data.append(close)
    scatter_plot_data.append([pt.next(high, low), index])

# print(pt.get_sar())
Graph["scatter_plot_with_line"](scatter_plot_data, line_plot_data)
