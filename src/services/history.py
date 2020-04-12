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


def getHistoryData(ticker):
    ticker_df = yf.download(tickers=ticker, start='2020-01-01')
    plotTitle = ticker + " stock price"
    ticker_df.head()
    print(ticker_df['Close'])
    ticker_df['Close'].plot(title=plotTitle)
    plt.show()
    return "data"
    # return ticker_df
# stock_history = microsoft.stock
# stock_history.head()
