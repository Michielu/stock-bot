import yfinance as yf
import stocker as Stocker
import pandas as pd
import matplotlib.pyplot as plt

# """Download yahoo tickers
#    :Parameters:
#        tickers : str, list
#            List of tickers to download
#        period : str
#            Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
#            Either Use period parameter or use start and end
#        interval : str
#            Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
#            Intraday data cannot extend last 60 days
#        start: str
#            Download start date string (YYYY-MM-DD) or _datetime.
#            Default is 1900-01-01
#        end: str
#            Download end date string (YYYY-MM-DD) or _datetime.
#            Default is now
#        group_by : str
#            Group by 'ticker' or 'column' (default)
#        prepost : bool
#        actions: bool
#            Download dividend + stock splits data. Default is False
#        rounding: bool
#            Optional. Round values to 2 decimal places?
#    """

valid_time_frames = {
    "1d": "1m",
    "5d": "5m",
    "1mo": "15m",
    "3mo": "30m",
    "6mo": "1h",
    "1y": "1h",
    "2y": "90m",
    "5y": "90m",
    "10y": "5d",
    "max": "5d"
}


def get_history_data(ticker):
    ticker_df = yf.download(tickers=ticker, start='2020-01-01')
    # ticker_df.head()
    print(ticker_df)
    return ticker_df


def get_day_data(ticker):
    ticker_df = yf.download(tickers=ticker, period="1d", interval="1m")
    # print(ticker_df)
    return ticker_df


def get_week_data(ticker):
    ticker_df = yf.download(tickers=ticker, period="5d", interval="5m")
    # print(ticker_df)
    return ticker_df


def get_data(ticker, time_frame):
    if time_frame not in valid_time_frames:
        return False
    ticker_df = yf.download(tickers=ticker, period=time_frame,
                            interval=valid_time_frames[time_frame])
    print(ticker_df)
    return ticker_df


History = {
    "get_history_data": get_history_data,
    "get_day_data": get_day_data,
    "get_week_data": get_week_data,
    "get_data": get_data
}
