import pandas as pd
import matplotlib.pyplot as plt


def basic_graph(data):
    print("data: ", data)
    pd.DataFrame({
        "CLOSE": data['Close'],
        "OPEN": data['Open']
    }).plot(title="Basic Graph title")
    plt.show()


def volume_graph(data):
    print("data: ", data)
    pd.DataFrame({
        "CLOSE": data['Close'],
        "Volume": data['Volume']
    }).plot(title="Volume Graph title")
    plt.show()


Graph = {
    "basic_graph": basic_graph,
    "volume_graph": volume_graph
}
