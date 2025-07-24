from abc import ABC, abstractmethod



class OrderAdapter(ABC):
    @abstractmethod
    def send_order(self):
        pass

    @abstractmethod
    def get_order(self, order_id: str, **kwargs):
        pass

    @abstractmethod
    def update_order(self, order_id: str, **kwargs):
        pass

    @abstractmethod
    def cancel_order(self) -> bool:
        pass


class SendOrderError(Exception):
    pass

class GetOrderError(Exception):
    pass

class CancelOrderError(Exception):
    pass