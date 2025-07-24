import logging
import json

from src.infrastructure.adapters.crypto.binance import BinanceSimpleOrderAdapter, BinanceFuturesOrderAdapter
from src.infrastructure.adapters.stocks.flowa.flowa_simple_order import FlowaSimpleOrderAdapter
from src.infrastructure.adapters.logger_adapter import LoggerAdapter
from src.infrastructure.adapters.order_adapter import OrderAdapter

from src.domain.orders.order_creation_manager import OrderCreationManager



class OrderService:
    def __init__(self, logger: logging.Logger = LoggerAdapter().get_logger()):
        self.logger = logger
        self.order_creation_manager = OrderCreationManager(logger=self.logger)
        self.order_adapter_dict = {
            "binance": {
                "simple-order": BinanceSimpleOrderAdapter(logger=self.logger),
                "futures": BinanceFuturesOrderAdapter(logger=self.logger)
            },
            "flowa": {
                "simple-order": FlowaSimpleOrderAdapter(logger=self.logger)
            }
        }

    def get_order_adapter(self, exchange_name: str, strategy: str) -> OrderAdapter:
        try:
            return self.order_adapter_dict[exchange_name][strategy]
        except KeyError as err:
            self.logger.error(f"Exchange requested is not valid: {exchange_name}")
            raise ValueError("Unsupported exchange")
    
    def send_order(self, exchange_name: str, strategy: str, order_data: dict):
        try:
            order = self.order_creation_manager.create_order(strategy, json.loads(order_data))
            order_adapter = self.get_order_adapter(exchange_name, strategy)
            response = order_adapter.send_order(order.to_dict())
            return response
        except Exception as err:
            self.logger.error(err)
            raise
    
    def get_order(self, exchange_name: str, strategy: str, order_id: str, **kwargs) -> dict:
        try:
            order_adapter = self.get_order_adapter(exchange_name, strategy)
            order = order_adapter.get_order(order_id, **kwargs)
            return order
        except Exception as err:
            self.logger.error(f"Could not send order, reason: {err}")
            raise

    def update_order(self, exchange_name: str, strategy: str, order_id: str, **kwargs) -> dict:
        try:
            order_adapter = self.get_order_adapter(exchange_name, strategy)
            order = order_adapter.update_order(order_id, **kwargs)
            return order
        except Exception as err:
            self.logger.error(f"Could not update order, reason: {err}")
            raise

    def cancel_order(self, exchange_name: str, strategy: str, order_id: str, **kwargs) -> bool:
        try:
            order_adapter = self.get_order_adapter(exchange_name, strategy)
            return order_adapter.cancel_order(order_id, **kwargs)
        except Exception as err:
            self.logger.error(f"Could not cancel order, reason: {err}")
            raise
