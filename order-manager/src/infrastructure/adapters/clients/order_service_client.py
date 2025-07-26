import logging
import httpx
import json



class OrderServiceClient:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.base_url = "http://localhost:5000/api/v1"
        self.client = httpx.AsyncClient()
    
    async def send_order(self, exchange_name: str, strategy: str, order_data: dict) -> dict:
        try:
            json_payload = {
                "exchange_name": exchange_name,
                "strategy": strategy,
                "order_data": json.dumps(order_data)
            }
            response = await self.client.post(f"{self.base_url}/send-order", params=json_payload)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as err:
            self.logger.error(f"[OrderHttpClient] Failed to send order: {err}")
            raise

    def get_order(self):
        pass

    def update_order(self):
        pass