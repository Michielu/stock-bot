import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def basic_graph(data):
    print("data: ", data)
    pd.DataFrame({
        "CLOSE": data['Close'],
        "OPEN": data['Open']
    }).plot(title="Basic Graph title")
    plt.show()


def volume_graph(data):
    # DataFrame and series's index already has dates as index
    pd.DataFrame({
        "CLOSE": data['Close'],
        "Volume": data['Volume']
    }).plot(title="Volume Graph title")


def graph(data_dic):
    # Data_dic example:
    # {
    #     "SPY": data_dic["SPY"],
    #     "Account": data_dic["Account"]
    # }
    # keys = data_dic.keys()
    # for k in keys:
    #     print(k, ": ", type(data_dic[k]), data_dic[k])

    df = pd.DataFrame(data_dic)
    df.plot(title="Graph title")
    plt.show()


def scatter_plot_with_line(scatter_data, line_data):
    df = pd.DataFrame(scatter_data, columns=['col', 'index'])

    plt.scatter(y=df.col, x=df.index, c='green')
    plt.plot(df.index, line_data, c="red", marker='.', linestyle=':')

    plt.show()


Graph = {
    "basic_graph": basic_graph,
    "volume_graph": volume_graph,
    "graph": graph,
    "scatter_plot_with_line": scatter_plot_with_line


}
