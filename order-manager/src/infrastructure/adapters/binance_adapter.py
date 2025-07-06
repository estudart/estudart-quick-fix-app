import os

from binance.client import Client, BinanceRequestException, BinanceAPIException
from dotenv import load_dotenv

from src.infrastructure.adapters import OrderAdapter
from src.infrastructure.adapters import LoggerAdapter

load_dotenv()

ENV = os.environ.get("ENV", "DEV")

class BinanceAdapter(OrderAdapter):
    def __init__(self,
                 endpoint: str = os.environ.get(f"BINANCE_ENDPOINT_{ENV}"),
                 api_key: str = os.environ.get(f"BINANCE_API_KEY_{ENV}"), 
                 api_secret: str = os.environ.get(f"BINANCE_API_SECRET_{ENV}"),
                 logger = LoggerAdapter().get_logger()):
        
        self.endpoint = endpoint
        self.api_key = api_key
        self.api_secret = api_secret
        self.logger = logger

        self.client = None

        self._start_client()

    def _start_client(self) -> None:
        self.client = Client(self.api_key, self.api_secret)
        self.client.API_URL = self.endpoint

    def send_order(self, order_data: dict) -> dict:
        try:
            order = self.client.create_order(**order_data)
            self.logger.info(f"Order was sent to Binance: {order}")
            return order
        except Exception as err:
            self.logger.error(f"Could not send order to Binance, reason: {err}")        
            raise

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
            return True
        except BinanceRequestException as err:
            self.logger.error(f"Could not cancel order from Binance, reason: {err}")
            return False
