from abc import ABC, abstractmethod



class OrderAdapter(ABC):
    @abstractmethod
    def send_order(self):
        pass

    @abstractmethod
    def get_order(self):
        pass

    @abstractmethod
    def cancel_order(self):
        pass