import os
import requests
from datetime import datetime, timedelta
import json

from dotenv import load_dotenv

from src.infrastructure.adapters.order_adapter import OrderAdapter
from src.infrastructure.adapters.logger_adapter import LoggerAdapter


load_dotenv()

ENV = os.environ.get("ENV", "DEV")

class FlowaAdapter(OrderAdapter):
    def __init__(self, logger = LoggerAdapter().get_logger()):
        self.api_secret = os.environ.get(f"FLOWA_API_SECRET_{ENV}")
        self.client_id = os.environ.get(f"FLOWA_CLIENT_ID_{ENV}")
        self.endpoint = os.environ.get(f"FLOWA_ENDPOINT_{ENV}")
        self.token_endpoint = os.environ.get(f"FLOWA_TOKEN_ENDPOINT_{ENV}")
        self.logger = logger
        self.token = None
        self.suffix = None
        self.provider = "Flowa"

    def get_token(self) -> str:
        token_request = {
            'grant_type': 'client_credentials',  # do not change
            'scope': 'atgapi',    # do not change
            'client_id': self.client_id,
            'client_secret': self.api_secret
        }
        if self.token is None or datetime.now() - refreshed_token_time > timedelta(hours=8):
            response = requests.post(self.token_endpoint, data=token_request)
            response.raise_for_status()

            self.token = response.json()['access_token']
            self.logger.info(f"New refreshed cached atg-token: {self.token}")
            refreshed_token_time = datetime.now()
        else:
            self.logger.info(f"atg-token is refreshed")

        return self.token
    
    def mount_request_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.get_token()
        }

    def transform_order(self, order_data: str):
        raise NotImplementedError

    def send_order(self, order_data: dict) -> dict:
        try:
            flowa_order = self.transform_order(order_data)
            order = requests.post(
                url=f"{self.endpoint}/{self.suffix}",
                data=json.dumps(**flowa_order),
                headers=self.mount_request_headers()
            )
            self.logger.info(f"Order was sent to {self.provider}: {order}")
            return order
        except Exception as err:
            self.logger.error(f"Could not send order to {self.provider}, reason: {err}")        
            raise
    
    def get_order(self, order_id: str):
        response = requests.get(
            f'{self.endpoint}/{self.suffix}/{order_id}',
            headers=self.mount_request_headers()
        )
        response.raise_for_status()
        order = response.json()
        return order
