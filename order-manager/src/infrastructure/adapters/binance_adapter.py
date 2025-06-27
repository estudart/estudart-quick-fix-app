import os

from binance.client import Client
from dotenv import load_dotenv

from src.infrastructure.adapters import OrderAdapter

load_dotenv()

ENV = os.environ.get("ENV")

class BinanceAdapter(OrderAdapter):
    def __init__(self,
                 endpoint: str = os.environ.get(f"BINANCE_ENDPOINT_{ENV}"),
                 api_key: str = os.environ.get(f"BINANCE_API_KEY_{ENV}"), 
                 api_secret: str = os.environ.get(f"BINANCE_API_SECRET_{ENV}")):
        self.endpoint = endpoint
        self.api_key = api_key
        self.api_secret = api_secret

        self.client = None

    def _start_client(self) -> None:
        self.client = Client(self.api_key, self.api_secret)

    def send_order(self, order_data):
        self.client.create_order()
        return super().send_order(order_data)