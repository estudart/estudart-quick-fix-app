import os

from dotenv import load_dotenv

from src.infrastructure.adapters.order_adapter import OrderAdapter



load_dotenv()

ENV = os.environ.get("ENV", "DEV")

class FlowaAdapter(OrderAdapter):
    def __init__(
            self,
            api_secret: str = os.environ.get(f"FLOWA_API_SECRET_{ENV}"),
            client_id: str = os.environ.get(f"FLOWA_CLIENT_ID_{ENV}"),
            endpoint: str = os.environ.get(f"FLOWA_ENDPOINT_{ENV}"),
            token_endpoint: str = os.environ.get(f"FLOWA_TOKEN_ENDPOINT_{ENV}")
        ):
        self.api_secret = api_secret
        self.client_id = client_id
        self.endpoint = endpoint
        self.token_endpoint = token_endpoint