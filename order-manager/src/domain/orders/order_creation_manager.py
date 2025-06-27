import logging

from src.infrastructure.adapters import OrderAdapter, LoggerAdapter
from src.application.orders import Order



class OrderCreationManager:
    def __init__(self, 
                 order_adapter: OrderAdapter,
                 logger: logging.Logger = LoggerAdapter.get_logger()):
        self.order_adapter = order_adapter
        self.logger = logger
    
    def create_order(self, order_data: dict):
        try:
            order = Order(**order_data)
            self.order_adapter.send_order(order.to_dict())
        except Exception as err:
            self.logger.error(f"Could not create order, reason: {err}")
            raise OrderCreationError(f"Unable to create order, reason: {err}") from err


class OrderCreationError(Exception):
    pass
