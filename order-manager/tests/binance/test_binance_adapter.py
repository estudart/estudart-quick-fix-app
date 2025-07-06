from src.infrastructure import BinanceAdapter

class TestBinanceAdapter:
    def setup_method(self):
        self.binanace_adapter = BinanceAdapter()

    def test_create_manage_order(self):
        order_data = {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "type": "LIMIT",
            "timeInForce": "GTC",
            "quantity": 0.001,
            "price": "30000"
        }
        order = self.binanace_adapter.send_order(order_data)
        order_id = order["orderId"]

        order = self.binanace_adapter.get_order("BTCUSDT", order_id)
        print(order)
        assert isinstance(order, dict)

        delete = self.binanace_adapter.cancel_order("BTCUSDT", order_id)
        assert delete
    
    def test_get_open_orders(self):
        open_orders = self.binanace_adapter.get_open_orders()
        print(open_orders)
        assert isinstance(open_orders, list)
