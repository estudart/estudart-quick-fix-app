import os

from binance.client import Client, BinanceRequestException, BinanceAPIException
from dotenv import load_dotenv

from src.infrastructure.adapters.order_adapter import OrderAdapter
from src.infrastructure.adapters.logger_adapter import LoggerAdapter

load_dotenv()

ENV = os.environ.get("ENV", "DEV")

class BinanceAdapter(OrderAdapter):
    def __init__(self, logger = LoggerAdapter().get_logger()):
        self.endpoint = os.environ.get(f"BINANCE_ENDPOINT_{ENV}")
        self.api_key = os.environ.get(f"BINANCE_API_KEY_{ENV}")
        self.api_secret = os.environ.get(f"BINANCE_API_SECRET_{ENV}")
        self.logger = logger
        self.provider = "Binance"

        self.client = None

        self._start_client()

    def _start_client(self) -> None:
        self.client = Client(self.api_key, self.api_secret)
        self.client.API_URL = self.endpoint

    def transform_order(self, order_data: str):
        raise NotImplementedError
    
    def transform_get_order(self, order_data: str):
        raise NotImplementedError

    def send_order(self, order_data: dict) -> str:
        try:
            binance_order = self.transform_order(order_data)
            order = self.client.create_order(**binance_order)
            self.logger.info(f"Order was sent to {self.provider}: {order}")
            return order["orderId"]
        except Exception as err:
            self.logger.error(f"Could not send order to {self.provider}, reason: {err}")        
            raise

    def get_order(self, order_id: str, **kwargs) -> dict:
        try:
            symbol = kwargs.get("symbol")
            if not symbol:
                raise ValueError("Missing required argument: 'symbol'")
            order = self.client.get_order(orderId=order_id, symbol=symbol)
            self.logger.debug(f"Order retrieved from {self.provider}: {order}")
            processed_order = self.transform_get_order(order)
            self.logger.info(f"Order processed from {self.provider}: {order}")
            return processed_order
        except BinanceRequestException as err:
            self.logger.error(f"Could not retrive order from {self.provider}, reason: {err}")
            raise

    def get_open_orders(self) -> list[dict]:
        try:
            open_orders = self.client.get_open_orders()
            self.logger.info(f"Open orders retrieved from Binance: {open_orders}")
            return open_orders
        except Exception as err:
            self.logger.error(f"Could not retrive open orders from {self.provider}, reason: {err}")
            raise

    def cancel_order(self, order_id: str, **kwargs) -> bool:
        try:
            symbol = kwargs.get("symbol")
            if not symbol:
                raise ValueError("Missing required argument: 'symbol'")
            self.client.cancel_order(orderId=order_id, symbol=kwargs.get("symbol"))
            self.logger.info(f"Order with id: {order_id} was successfully cancelled on {self.provider}")
            return True
        except BinanceRequestException as err:
            self.logger.error(f"Could not cancel order from {self.provider}, reason: {err}")
            return False
