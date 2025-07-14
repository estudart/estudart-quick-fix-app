from abc import ABC, abstractmethod



class MDAdapter(ABC):
    @abstractmethod
    def fetch_price(self, ticker: str) -> float:
        pass
