from src.application.orders.order_service import OrderService



class TestOrderService:
    def setup_method(self):
        self.order_service = OrderService()

    def test_create_binance_simple_order(self):
        order_data = {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "order_type": "LIMIT",
            "time_in_force": "GTC",
            "quantity": 0.001,
            "price": 30000
        }
        self.order_service.send_order("binance", "simple-order", order_data)
    
    def test_create_binance_futures_order(self):
        order_data = {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "quantity": 0.006,
            "price": 30000,
            "order_type": "LIMIT",
            "time_in_force": "GTC",
        }
        self.order_service.send_order("binance", "simple-order", order_data)

    def test_create_flowa_simple_order(self):
        order_data = {
            "broker": "935",
            "account": "1001",
            "symbol": "BITH11",
            "side": "BUY",
            "quantity": 1,
            "price": 30,
            "order_type": "LIMIT",
            "time_in_force": "GTC"
        }
        self.order_service.send_order("flowa", "simple-order", order_data)