
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
from services.sp500 import SP500

sp500Data = SP500["getSP500"]()
sp500 = []
for x in sp500Data:
    sp500.append(MyStock(x[0], x[1], x[3]))

for company in sp500:
    print(company.getData())
