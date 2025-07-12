import json

from src.infrastructure.adapters.stocks.flowa.flowa_adapter import FlowaAdapter


class FlowaSimpleOrderAdapter(FlowaAdapter):
    def __init__(self, logger=...):
        super().__init__(logger)
        self.suffix = "simple-order"

    def transform_order(self, order_data: str) -> dict:
        return {
            "Broker": order_data["broker"],
            "Account": order_data["account"],
            "Symbol": order_data["symbol"],
            "Side": order_data["side"],
            "OrderType": order_data["order_type"],
            "TimeInForce": order_data["time_in_force"],
            "Quantity": order_data["quantity"],
            "Price": str(order_data["price"])
        }
