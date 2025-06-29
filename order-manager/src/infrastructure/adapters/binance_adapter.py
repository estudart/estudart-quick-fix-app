import os

from binance.client import Client
from dotenv import load_dotenv

from src.infrastructure.adapters import OrderAdapter

load_dotenv()

ENV = os.environ.get("ENV", "DEV")

class BinanceAdapter(OrderAdapter):
    def __init__(self,
                 endpoint: str = os.environ.get(f"BINANCE_ENDPOINT_{ENV}"),
                 api_key: str = os.environ.get(f"BINANCE_API_KEY_{ENV}"), 
                 api_secret: str = os.environ.get(f"BINANCE_API_SECRET_{ENV}")):
        self.endpoint = endpoint
        self.api_key = api_key
        self.api_secret = api_secret

        self.client = None

        self._start_client()

    def _start_client(self) -> None:
        self.client = Client(self.api_key, self.api_secret)
        self.client.API_URL = self.endpoint

    def send_order(self, order_data: dict) -> None:
        order = self.client.create_order(**order_data)
        print(order)

    def get_open_orders(self):
        open_orders = self.client.get_open_orders()
        return open_orders