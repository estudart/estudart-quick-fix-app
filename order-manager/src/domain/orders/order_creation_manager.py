import logging

from src.infrastructure.adapters import OrderAdapter, BinanceAdapter, LoggerAdapter
from src.application.orders import Order



class OrderCreationManager:
    def __init__(self,
                 logger: logging.Logger = LoggerAdapter.get_logger()):
        self.logger = logger
        self.order_adapter_dict = {
            "binance": BinanceAdapter()
        }

    def get_order_adapter(self, exchange_name: str) -> OrderAdapter:
        try:
            return self.order_adapter_dict[exchange_name]
        except KeyError as err:
            self.logger.error("Exchange requested is not valid")
            raise
    
    def create_order(self, exchange_name: str, order_data: dict):
        try:
            order = Order(**order_data)
            order_adapter = self.get_order_adapter(exchange_name)
            order_adapter.send_order(order.to_dict())
        except Exception as err:
            self.logger.error(f"Could not create order, reason: {err}")
            raise OrderCreationError(f"Unable to create order, reason: {err}") from err


class OrderCreationError(Exception):
    pass
