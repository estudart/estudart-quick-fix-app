import os

import ccxt
from dotenv import load_dotenv

from src.infrastructure.adapters.order_adapter import OrderAdapter
from src.infrastructure.adapters.logger_adapter import LoggerAdapter

load_dotenv()

ENV = os.environ.get("ENV", "DEV")

class BinanceFuturesAdapter(OrderAdapter):
    def __init__(self, logger = LoggerAdapter().get_logger()):
        self.endpoint = os.environ.get(f"BINANCE_FUTURES_ENDPOINT_{ENV}")
        self.api_key = os.environ.get(f"BINANCE_FUTURES_API_KEY_{ENV}")
        self.api_secret = os.environ.get(f"BINANCE_FUTURES_API_SECRET_{ENV}")
        self.logger = logger
        self.provider = "Binance"

        self.client = None

        self._start_client()

    def _start_client(self) -> None:
        self.client = ccxt.binance({
            'apiKey': self.api_key,
            'secret': self.api_secret,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'future',  # futures trading
            },
        })
        if ENV == "DEV":
            self.client.set_sandbox_mode(True)

    def transform_order(self, order_data: str):
        raise NotImplementedError
    
    def transform_get_order(self, order_data: str):
        raise NotImplementedError

    def send_order(self, order_data: dict) -> str:
        try:
            binance_order = self.transform_order(order_data)
            order = self.client.create_order(**binance_order)
            self.logger.info(f"Order was sent to {self.provider}: {order}")
            return order["info"]["orderId"]
        except Exception as err:
            self.logger.error(f"Could not send order to {self.provider}, reason: {err}")        
            raise

    def get_order(self, order_id: str, **kwargs) -> dict:
        try:
            symbol = kwargs.get("symbol")
            if not symbol:
                raise ValueError("Missing required argument: 'symbol'")
            order = self.client.fetch_order(orderId=order_id, symbol=symbol)
            self.logger.debug(f"Order retrieved from {self.provider}: {order}")
            processed_order = self.transform_get_order(order)
            self.logger.info(f"Order processed from {self.provider}: {order}")
            return processed_order
        except Exception as err:
            self.logger.error(f"Could not retrive order from {self.provider}, reason: {err}")
            raise

    def get_open_orders(self) -> list[dict]:
        try:
            open_orders = self.client.fetch_open_orders()
            self.logger.info(f"Open orders retrieved from Binance: {open_orders}")
            return open_orders
        except Exception as err:
            self.logger.error(f"Could not retrive open orders from {self.provider}, reason: {err}")
            raise
    
    def update_order(self, order_id, **kwargs):
        return super().update_order(order_id, **kwargs)

    def cancel_order(self, order_id: str, **kwargs) -> bool:
        try:
            symbol = kwargs.get("symbol")
            if not symbol:
                raise ValueError("Missing required argument: 'symbol'")
            self.client.cancel_order(orderId=order_id, symbol=kwargs.get("symbol"))
            self.logger.info(f"Order with id: {order_id} was successfully cancelled on {self.provider}")
            return True
        except Exception as err:
            self.logger.error(f"Could not cancel order from {self.provider}, reason: {err}")
            return False
