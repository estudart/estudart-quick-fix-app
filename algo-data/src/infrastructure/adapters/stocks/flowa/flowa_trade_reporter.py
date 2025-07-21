from typing import Callable
import logging
import requests
import os

import websocket
import msgpack
from dotenv import load_dotenv

from src.infrastructure.adapters.trade_reporter_adapter import TradeReporter
from src.infrastructure.adapters.logger_adapter import LoggerAdapter

load_dotenv()

ENV = os.environ.get("ENV", "DEV")


class FlowaTradeReporter(TradeReporter):
    def __init__(
            self,
            channel: str,
            logger: logging.Logger = LoggerAdapter().get_logger()
        ) -> None:
        self.api_secret: str = os.environ.get(f"FLOWA_API_SECRET_{ENV}")
        self.client_id: str = os.environ.get(f"FLOWA_CLIENT_ID_{ENV}")
        self.endpoint: str = os.environ.get(f"FLOWA_WS_ENDPOINT_{ENV}")
        self.token_endpoint = os.environ.get(f"FLOWA_TOKEN_ENDPOINT_{ENV}")
        self.on_event: Callable = None
        self.logger = logger
        self.channel = channel
        self.provider = "Flowa"

    def on_message(self, ws: websocket.WebSocketApp, message):
        if message == b'\xff':
            ws.send(b'1')
            return
        
        try:
            msg_data = msgpack.unpackb(message)
            self.logger.info(f"{self.provider}-{self.channel} | Received: {msg_data}")
            self.on_event(msg_data)
        except Exception as err:
            self.logger.error(f"Error processing message: {err}")

    def on_error(self, ws:websocket.WebSocketApp , error):
        self.logger.error(f"Error: {error}")

    def get_token(self):
            token_request = {
                'grant_type': 'client_credentials',  # do not change
                'scope': 'atgapi',    # do not change
                'client_id': self.client_id,
                'client_secret': self.api_secret
            }
            response = requests.post(self.token_endpoint, data=token_request)
            response.raise_for_status()
            return response.json()['access_token']


    def on_open(self, ws: websocket.WebSocketApp):
        self.logger.info(f"{self.provider}-{self.channel}: sending auth token.")
        token = self.get_token()
        ws.send(token)
        self.logger.info(f"{self.provider}-{self.channel}: Connection with websocket established.")


    def on_close(self, ws: websocket.WebSocketApp, close_status_code, close_msg):
        self.logger.info(f"{self.provider}: Connection was closed with code: {close_status_code}, message: {close_msg}")


    def start_reporting(self, callback: Callable):
        websocket.enableTrace(False)
        self.on_event = callback
        if self.channel == "orders":
            ws = websocket.WebSocketApp(
                f"{self.endpoint}/ws/strategies",
                on_message=self.on_message,
                on_error=self.on_error,
                on_open=self.on_open,
                on_close=self.on_close
            )
        elif self.channel == "trades":
            ws = websocket.WebSocketApp(
                f"{self.endpoint}/ws/trades",
                on_message=self.on_message,
                on_error=self.on_error,
                on_open=self.on_open,
                on_close=self.on_close
            )

        ws.run_forever()
