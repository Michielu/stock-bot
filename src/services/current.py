import pandas as pd
import matplotlib.pyplot as plt
from yahoo_fin import stock_info as si


def get_current_price(ticker):
    tickerLive = si.get_live_price(ticker)
    # ticker_df.head()
    print(tickerLive)
    return tickerLive


def get_current_price_list(tickers):
    prices = []
    for t in tickers:
        # print(t)
        # print("current: ", prices)
        prices.append(si.get_live_price(t))
    # print(prices)
    return prices


Current = {
    "get_current_price": get_current_price,
    "get_current_price_list": get_current_price_list
}
