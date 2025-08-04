import os
import requests
from datetime import datetime, timedelta

from dotenv import load_dotenv

from src.infrastructure.adapters.order_adapter import (
    OrderAdapter, 
    SendOrderError, 
    GetOrderError,
    CancelOrderError,
    UpdateOrderError
)
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
        self.refreshed_token_time = None
        self.suffix = None
        self.provider = "Flowa"

    def get_token(self) -> str:
        token_request = {
            'grant_type': 'client_credentials',  # do not change
            'scope': 'atgapi',    # do not change
            'client_id': self.client_id,
            'client_secret': self.api_secret
        }
        if self.token is None or datetime.now() - self.refreshed_token_time > timedelta(hours=8):
            response = requests.post(self.token_endpoint, data=token_request)
            response.raise_for_status()
            self.token = response.json()['access_token']
            self.logger.debug(f"New refreshed cached {self.provider} token: {self.token}")
            self.logger.info(f"{self.provider} token was refreshed")
            self.refreshed_token_time = datetime.now()
        else:
            self.logger.debug(f"{self.provider} token is refreshed")

        return self.token
    
    def mount_request_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.get_token()
        }

    def transform_order(self, order_data: str):
        raise NotImplementedError
    
    def transform_get_order(self, order_id: str) -> dict:
        raise NotImplementedError
    
    def transform_update_order(self, order_dict: dict) -> dict:
        raise NotImplementedError

    def send_order(self, order_data: dict) -> str:
        try:
            flowa_order = self.transform_order(order_data)
            response = requests.post(
                url=f"{self.endpoint}/{self.suffix}",
                json=flowa_order,
                headers=self.mount_request_headers()
            )
            response.raise_for_status()
            order = response.json()
            if not order["Success"]:
                raise SendOrderError(f'Failed to send order, reason: {order["Error"]}')
            self.logger.info(f"Order was sent to {self.provider}: {order}")
            return order["StrategyId"]
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
            response = requests.get(
                f'{self.endpoint}/{self.suffix}/{order_id}',
                headers=self.mount_request_headers()
            )
            response.raise_for_status()
            order = response.json()
            return self.transform_get_order(order)
        except Exception as err:
            msg = f"Could not get order from {self.provider}, reason: {err}"
            self.logger.exception(msg)
            raise GetOrderError(msg) from err
    
    def update_order(self, order_id, **kwargs) -> bool:
        try:
            update_params = self.transform_update_order({**kwargs})
            response = requests.put(
                f'{self.endpoint}/{self.suffix}/{order_id}',
                headers=self.mount_request_headers(),
                json=update_params
            )
            response.raise_for_status()
            order = response.json()
            if not order["Success"]:
                raise UpdateOrderError(f'Failed to update order, reason: {order["Error"]}')
            self.logger.info(f"Order with id: {order_id} was successfully updated on {self.provider}")
        except (requests.RequestException, ValueError, KeyError) as err:
            msg = f"Could not update order to {self.provider}, reason: {err}"
            self.logger.exception(msg)
            raise UpdateOrderError(msg) from err
        except Exception as err:
            msg = f"Could not update order to {self.provider}, reason: {err}"
            self.logger.exception(msg)
            raise
    
    def cancel_order(self, order_id: str, **kwargs) -> bool:
        try:
            response = requests.delete(
                f'{self.endpoint}/{self.suffix}/{order_id}',
                headers=self.mount_request_headers()
            )
            response.raise_for_status()
            self.logger.info(f"Order with id: {order_id} was successfully cancelled on {self.provider}")
            return response.json()
        except Exception as err:
            msg = f"Could not cancel order from {self.provider}, reason: {err}"
            self.logger.exception(msg)
            raise CancelOrderError(msg) from err
