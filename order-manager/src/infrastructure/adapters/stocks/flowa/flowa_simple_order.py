import json

import requests

from src.infrastructure.adapters.stocks.flowa.flowa_adapter import FlowaAdapter


class FlowaSimpleOrderAdapter(FlowaAdapter):
    def transform_order(self, order_data: str):
        return {
            "Symbol": order_data["symbol"],
            "Side": order_data["side"],
            "OrderType": order_data["order_type"],
            "TimeInForce": order_data["time_in_force"],
            "Quantity": order_data["quantity"],
            "Price": str(order_data["price"])
        }

    def send_order(self, order_data: dict) -> dict:
        try:
            flowa_order = self.transform_order(order_data)
            order = requests.post(
                url=f"{self.endpoint}/simple-order",
                data=json.dumps(**flowa_order),
                headers=self.mount_request_headers()
            )
            self.logger.info(f"Order was sent to {self.provider}: {order}")
            return order
        except Exception as err:
            self.logger.error(f"Could not send order to {self.provider}, reason: {err}")        
            raise