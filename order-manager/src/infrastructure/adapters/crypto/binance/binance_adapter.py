import os
import requests

import ccxt
from dotenv import load_dotenv

from src.infrastructure.adapters.order_adapter import (
    OrderAdapter, 
    SendOrderError, 
    GetOrderError,
    CancelOrderError
)
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
        self.client = ccxt.binance({
            'apiKey': self.api_key,
            'secret': self.api_secret,
            'enableRateLimit': True
        })
        self.client.options["warnOnFetchOpenOrdersWithoutSymbol"] = False
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
        except (requests.RequestException, ValueError, KeyError) as err:
            msg = f"Could not send order to {self.provider}, reason: {err}"
            self.logger.exception(msg)
            raise SendOrderError(msg) from err
        except Exception as err:
            msg = f"Could not send order to {self.provider}, reason: {err}"
            self.logger.exception(msg)
            raise

    def get_order(self, order_id: str, **kwargs) -> dict:
        try:
            symbol = kwargs.get("symbol")
            if not symbol:
                raise ValueError("Missing required argument: 'symbol'")
            order = self.client.fetch_order(id=order_id, symbol=symbol)
            self.logger.debug(f"Order retrieved from {self.provider}: {order}")
            processed_order = self.transform_get_order(order["info"])
            self.logger.info(f"Order processed from {self.provider}: {order}")
            return processed_order
        except Exception as err:
            msg = f"Could not get order from {self.provider}, reason: {err}"
            self.logger.exception(msg)
            raise GetOrderError(msg) from err

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
            response = self.client.cancel_order(id=order_id, symbol=kwargs.get("symbol"))
            self.logger.info(f"Order with id: {order_id} was successfully cancelled on {self.provider}")
            return response
        except Exception as err:
            msg = f"Could not cancel order from {self.provider}, reason: {err}"
            self.logger.exception(msg)
            raise CancelOrderError(msg) from err
