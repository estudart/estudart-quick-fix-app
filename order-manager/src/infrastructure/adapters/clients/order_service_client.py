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
                "strategy": strategy
            }
            response = self.client.post(f"{self.base_url}/send-order", params=params, json=order_data)
            response.raise_for_status()
            return response.json()
        except (httpx.HTTPError, httpx.HTTPStatusError) as err:
            self.logger.error(f"[OrderHttpClient] Failed to send order: {err}")
            raise
        except Exception as err:
            self.logger.exception(f"[OrderHttpClient] Failed to send order with unkown exception: {err}")
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
        except (httpx.HTTPError, httpx.HTTPStatusError) as err:
            self.logger.error(f"[OrderHttpClient] Failed to get order: {err}")
            raise
        except Exception as err:
            self.logger.exception(f"[OrderHttpClient] Failed to get order with unkown exception: {err}")
            raise

    def update_order(self, exchange_name: str, strategy: str, order_id: dict, order_data: dict, **kwargs) -> dict:
        try:
            params = {
                "exchange_name": exchange_name,
                "strategy": strategy,
                "order_id": order_id,
                **kwargs
            }
            response = self.client.put(f"{self.base_url}/update-order", params=params, json=order_data)
            response.raise_for_status()
            return response.json()
        except (httpx.HTTPError, httpx.HTTPStatusError) as err:
            self.logger.error(f"[OrderHttpClient] Failed to update order: {err}")
            raise
        except Exception as err:
            self.logger.exception(f"[OrderHttpClient] Failed to update order with unkown exception: {err}")
            raise

    def cancel_order(self, exchange_name: str, strategy: str, order_id: str, **kwargs) -> dict:
        try:
            params = {
                "exchange_name": exchange_name,
                "strategy": strategy,
                "order_id": order_id,
                **kwargs
            }
            response = self.client.delete(f"{self.base_url}/cancel-order", params=params)
            response.raise_for_status()
            return response.json()
        except (httpx.HTTPError, httpx.HTTPStatusError) as err:
            self.logger.error(f"[OrderHttpClient] Failed to cancel order: {err}")
            raise
        except Exception as err:
            self.logger.exception(f"[OrderHttpClient] Failed to cancel order with unkown exception: {err}")
            raise