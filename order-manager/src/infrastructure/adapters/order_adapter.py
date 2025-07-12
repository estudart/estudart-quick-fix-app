from abc import ABC, abstractmethod



class OrderAdapter(ABC):
    @abstractmethod
    def send_order(self):
        pass