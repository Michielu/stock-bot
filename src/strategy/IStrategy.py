from abc import ABC, abstractmethod


class IStrategy(ABC):
    @abstractmethod
    def next_data_point(self, ticker, price): pass
