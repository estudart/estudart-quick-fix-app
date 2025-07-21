from abc import ABC, abstractmethod



class TradeReporter(ABC):
    @abstractmethod
    def start_reporting(self):
        pass