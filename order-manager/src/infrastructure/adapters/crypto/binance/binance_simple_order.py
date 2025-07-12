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

    def send_order(self, order_data: dict) -> dict:
        try:
            binance_order = self.transform_order(order_data)
            order = self.client.create_order(**binance_order)
            self.logger.info(f"Order was sent to Binance: {order}")
            return order
        except Exception as err:
            self.logger.error(f"Could not send order to Binance, reason: {err}")        
            raise
