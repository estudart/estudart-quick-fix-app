import json

from src.infrastructure.adapters.stocks.flowa.flowa_adapter import FlowaAdapter
from src.infrastructure.adapters.logger_adapter import LoggerAdapter


class FlowaSimpleOrderAdapter(FlowaAdapter):
    def __init__(self, logger = LoggerAdapter().get_logger()):
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

    def transform_get_order(self, order_data: dict) -> dict:
        return {
            "order_id": order_data["StrategyId"],
            "symbol": order_data["Symbol"],
            "side": order_data["Side"],
            "quantity": order_data["Quantity"],
            "price": order_data["Price"],
            "order_type": order_data["OrderType"],
            "exec_qty": order_data["ExecutedQuantity"],
            "time_in_force": order_data["TimeInForce"],
            "status": order_data["Status"]
        }