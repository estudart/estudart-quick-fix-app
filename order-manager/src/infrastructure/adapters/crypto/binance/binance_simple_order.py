from binance.client import BinanceRequestException, BinanceAPIException

from src.infrastructure.adapters.crypto.binance import BinanceAdapter



class BinanceSimpleOrderAdapter(BinanceAdapter):
    def transform_order(self, order_data: str):
        return {
            "symbol": order_data["symbol"],
            "side": order_data["side"],
            "type": order_data["order_type"],
            "timeInForce": order_data["time_in_force"],
            "quantity": order_data["quantity"],
            "price": str(order_data["price"])
        }
