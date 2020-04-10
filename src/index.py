
# https://towardsdatascience.com/stock-analysis-in-python-a0054e2c1a4c
# Issue with Catalina OS https://github.com/tensorflow/tensorflow/issues/33183
# Another solution: https://apple.stackexchange.com/questions/237430/how-to-install-specific-version-of-python-on-os-x/319675#319675
# import stocker
import pandas as pd
import certifi
import ssl
import urllib.request as urlrq
import numpy as np
from dataObj.MyStocks import MyStock
# from services.sp500 import SP500


resp = urlrq.urlopen('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies',
                     context=ssl.create_default_context(cafile=certifi.where()))

html = resp.read()  # table = data[0]
data = pd.read_html(html)

table = data[0]
sliced_table = table[1:]
header = table.iloc[0]
corrected_table = sliced_table.rename(columns=header)

print(corrected_table.values)

sp500 = []
for x in corrected_table.values:
    sp500.append(MyStock(x[0], x[1], x[3]))
    # print(stock1.getAll())

for company in sp500:
    print(company.getData())
# print(sp500)

# appl = stocker.predict.tomorrow('AAPL')
# print(appl)
# appl.plot_stock()

print("IN HERE :")
# SP500.getSp500()
