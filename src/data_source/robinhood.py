
# Possible packages: https://github.com/robinhood-unofficial/pyrh or https://pyrh.readthedocs.io/en/latest/
# Another possible https://github.com/mstrum/robinhood-python
# Using https://github.com/jmfernandes/robin_stocks or http://www.robin-stocks.com/en/latest/functions.html
import robin_stocks as r
import json


class Robinhood:
    def __init__(self, email):
        f = open('./src/config/robinhood.json')
        # robinhood.json is not stored publically for security reasons
        # For personal use, create a robinhood file that looks like this:
        #       { "you_robinhood_email@email.com":"Your_robinhood_password"}
        robinhood_login_info = json.load(f)
        print(robinhood_login_info)

        r.login(email, robinhood_login_info[email])
        self.my_stocks = self.refresh_holdings()

    def refresh_holdings(self):
        return r.build_holdings()

    def get_buying_power(self):
        return r.load_account_profile()["buying_power"]

    def get_total_equity(self):
        return r.load_portfolio_profile()["equity"]

    def get_num_stock_own(self, ticker):
        try:
            return self.my_stocks[ticker]["quantity"]
        except:
            return 0

    def get_stock_info(self, ticker):
        return self.my_stocks[ticker]

    def get_all_stock_info(self):
        return self.my_stocks

    def cancel_all_orders(self):
        return r.cancel_all_stock_orders()

    def order_buy_limit(self, symbol, quantity, limitPrice):
        buy_status = r.order_buy_limit(symbol, quantity, limitPrice)
        # Test if stocks are updated immediately or nah
        self.my_stocks = self.refresh_holdings()
        return buy_status

    def order_buy_market(self, symbol, quantity):
        buy_status = r.order_buy_market(symbol, quantity)
        self.my_stocks = self.refresh_holdings()
        return buy_status

    def order_sell_limit(self, symbol, quantity, limitPrice):
        sell_status = r.order_sell_limit(symbol, quantity, limitPrice)
        # Test if stocks are updated immediately or nah
        self.my_stocks = self.refresh_holdings()
        return sell_status

    def order_sell_market(self, symbol, quantity):
        sell_status = r.order_sell_market(symbol, quantity)
        self.my_stocks = self.refresh_holdings()
        return sell_status

    def order_sell_market_all(self, symbol):
        return self.order_sell_market(symbol, self.get_num_stock_own(symbol))
