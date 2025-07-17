from binance.client import BinanceRequestException, BinanceAPIException

from src.infrastructure.adapters.crypto.binance import BinanceFuturesAdapter



class BinanceFuturesOrderAdapter(BinanceFuturesAdapter):
    def transform_order(self, order_data: dict):
        transformed = {
            "symbol": order_data["symbol"],
            "side": order_data["side"],
            "type": order_data["order_type"],
            "quantity": order_data["quantity"]
        }
        if transformed["type"] == "LIMIT":
            transformed.update(
                price=str(order_data["price"]),
                timeInForce=order_data["time_in_force"],
            )
        return transformed
    
    def transform_get_order(self, order_data):
        return {
            "symbol": order_data["symbol"],
            "side": order_data["side"],
            "quantity": order_data["origQty"],
            "price": float(order_data["price"]),
            "order_type": order_data["type"],
            "exec_qty": order_data["executedQty"],
            "time_in_force": order_data["timeInForce"],
            "status": order_data["status"]
        }
