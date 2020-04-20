from abc import ABC, abstractmethod


class IAccount(ABC):
    @abstractmethod
    def get_account_value(self): pass

    @abstractmethod
    def get_buying_power(self): pass

    # value = price per stock
    @abstractmethod
    def buy_stock(self, ticker, num, value): pass

    @abstractmethod
    def sell_stock(self, ticker, num, value): pass

    @abstractmethod
    def owned_stock_info(self, ticker): pass

    @abstractmethod
    def print_summary(self): pass
