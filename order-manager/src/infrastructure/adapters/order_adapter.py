from abc import ABC, abstractmethod



class OrderAdapter(ABC):
    @abstractmethod
    def send_order(self, order_data: dict):
        """ This method should send orders to Exchange """
        pass