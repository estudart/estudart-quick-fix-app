import os

from binance.client import Client, BinanceRequestException, BinanceAPIException
from dotenv import load_dotenv

from src.infrastructure.adapters.order_adapter import OrderAdapter

load_dotenv()

ENV = os.environ.get("ENV", "DEV")

class BinanceAdapter(OrderAdapter):
    def __init__(self, logger):
        self.endpoint = os.environ.get(f"BINANCE_ENDPOINT_{ENV}")
        self.api_key = os.environ.get(f"BINANCE_API_KEY_{ENV}")
        self.api_secret = os.environ.get(f"BINANCE_API_SECRET_{ENV}")
        self.logger = logger

        self.client = None

        self._start_client()

    def _start_client(self) -> None:
        self.client = Client(self.api_key, self.api_secret)
        self.client.API_URL = self.endpoint

    def transform_order(self, order_data: str):
        raise NotImplementedError
    
    def send_order(self, order_data: dict) -> dict:
        raise NotImplementedError

    def get_order(self, symbol: str, order_id: str) -> dict:
        try:
            order = self.client.get_order(symbol=symbol, orderId=order_id)
            self.logger.info(f"Order retrieved from Binance: {order}")
            return order
        except BinanceRequestException as err:
            self.logger.error(f"Could not retrive order from Binance, reason: {err}")
            raise

    def get_open_orders(self) -> list[dict]:
        try:
            open_orders = self.client.get_open_orders()
            self.logger.info(f"Open orders retrieved from Binance: {open_orders}")
            return open_orders
        except Exception as err:
            self.logger.error(f"Could not retrive open orders from Binance, reason: {err}")
            raise

    def cancel_order(self, symbol: str, order_id: str) -> bool:
        try:
            self.client.cancel_order(symbol=symbol, orderId=order_id)
            self.logger.info(f"Order with id: {order_id} was successfully cancelled on Binance")
            return True
        except BinanceRequestException as err:
            self.logger.error(f"Could not cancel order from Binance, reason: {err}")
            return False
