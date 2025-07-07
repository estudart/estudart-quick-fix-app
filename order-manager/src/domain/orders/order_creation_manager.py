from src.infrastructure.adapters import LoggerAdapter
from src.domain.orders import Order



class OrderCreationManager:
    def __init__(self, logger = LoggerAdapter().get_logger()):
        self.logger = logger

    def create_order(self, order_data: dict):
        try:
            order = Order(**order_data)
            return order
        except Exception as err:
            raise OrderCreationError(f"Could not create order, reason: {err}")


class OrderCreationError(Exception):
    pass