# pylint: disable=import-error

import certifi
import ssl
import urllib.request as urlrq
import pandas as pd
from module_obj.MyStock import MyStock


def getSP500():
    resp = urlrq.urlopen('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies',
                         context=ssl.create_default_context(cafile=certifi.where()))
    html = resp.read()
    data = pd.read_html(html)
    table = data[0]
    sliced_table = table[1:]
    header = table.iloc[0]
    corrected_table = sliced_table.rename(columns=header)
    values = corrected_table.values
    sp500 = []
    for x in values:
        if x[0].find(".") == -1:
            sp500.append(MyStock(x[0]))

    print(len(values), "to",  len(sp500))
    return sp500


SP500 = {
    "getSP500": getSP500
}
