# stock-bot

Grand purpose of this repo is simple. Capitilize on the stock market to grow personal capital.

This repo does two things:
1) Test and capitalize stock trading strategies
2) Predict which S&P 500 Stocks will show short term success. 

## Test Stock Trading Strategies
There are many places to test trading strategies with fancy graphs and charts. 
This script does multiple things to help you feel confident before hooking it up with your real Robinhood brokerage account(also does on this script).


You can decide whether to use real time stock data or use past data. Then choose to use a paper account (fake) or use your real account.  This gives you the flexibility to test strategies with past data quickly before putting real money on the line.


To run:
1) Install Python and appropriate dependencies
2) Run this command in terminal `python3 src/index`
a) If hook up with personal RH account, create a `/src/config/robinhood.json` file with content like this: 
```
{
    "your_email_address@gmail.com": "robinhood_password"
}
```
3) To add strategy: create strategy file in `strategy` directory and import and use that in `index.py`  

## Predict which S&P 500 Stocks will show short term success. 

Uses [Stocker API](https://github.com/WillKoehrsen/Data-Analysis/tree/master/stocker) as stock predicter tool. 

Exports s&p500 predictions to google sheet file, which is later updatable with actual closing prices and generates ratios of which stocks were the most successful. This can be analyzed to make investment decisions. 

This was created to help with investors with American investers with less than 25k that can only do 3 day trades with a five day period. By leveraging a stock predicting tool, I can avoid the PDT law by. 

This also allows me to be on certain sp500 stocks instead of the entirety of the index, which is heavily influenced by specific stocks.

 <i>**Disclaimer**This project is for educational purposes and not meant as investment advice or recommendation. Utilize this tool at your own risk. </i>

<b> Resources and tools </b>
 https://towardsdatascience.com/stock-analysis-in-python-a0054e2c1a4c
 Issue with Catalina OS https://github.com/tensorflow/tensorflow/issues/33183
 yfinance call limit: 2000 calls/hour