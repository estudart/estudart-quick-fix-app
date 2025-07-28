import logging
import httpx
import json



class OrderServiceClient:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.base_url = "http://localhost:5000/api/v1"
        self.client = httpx.Client()
    
    def send_order(self, exchange_name: str, strategy: str, order_data: dict) -> dict:
        try:
            params = {
                "exchange_name": exchange_name,
                "strategy": strategy,
                "order_data": json.dumps(order_data)
            }
            response = self.client.post(f"{self.base_url}/send-order", params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as err:
            self.logger.error(f"[OrderHttpClient] Failed to send order: {err}")
            raise

    def get_order(self, exchange_name: str, strategy: str, order_id: dict, **kwargs) -> dict:
        try:
            params = {
                "exchange_name": exchange_name,
                "strategy": strategy,
                "order_id": order_id,
                **kwargs
            }
            response = self.client.get(f"{self.base_url}/get-order", params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as err:
            self.logger.error(f"[OrderHttpClient] Failed to send order: {err}")
            raise

    def update_order(self, exchange_name: str, strategy: str, order_id: dict, order_data: dict, **kwargs) -> dict:
        try:
            params = {
                "exchange_name": exchange_name,
                "strategy": strategy,
                "order_id": order_id,
                "order_data": json.dumps(order_data),
                **kwargs
            }
            response = self.client.put(f"{self.base_url}/update-order", params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as err:
            self.logger.error(f"[OrderHttpClient] Failed to send order: {err}")
            raise