from src.application import OrderService



class TestOrderService:
    def setup_method(self):
        self.order_service = OrderService()

    def test_create_simple_order(self):
        order_data = {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "order_type": "LIMIT",
            "time_in_force": "GTC",
            "quantity": 0.001,
            "price": 30000
        }
        self.order_service.send_order("binance", "simple-order", order_data)