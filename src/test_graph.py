# pylint: disable=import-error, no-name-in-module

from data_source.history import History
from util.graph import Graph
import matplotlib.pyplot as plt


day_data_df = History["get_week_data"]("SPY")
print(type(day_data_df))
print(day_data_df[["Close"]])
Graph["volume_graph"](day_data_df)
plt.show()
