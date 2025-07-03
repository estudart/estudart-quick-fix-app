from src.infrastructure import BinanceAdapter

class TestBinanceAdapter:
    def setup_method(self):
        self.binanace_adapter = BinanceAdapter()

    def test_send_order(self):
        order_data = {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "type": "LIMIT",
            "timeInForce": "GTC",
            "quantity": 0.001,
            "price": "30000"
        }
        self.binanace_adapter.send_order(order_data)

    def test_get_order(self):
        order = self.binanace_adapter.get_order("BTCUSDT", "492537")
        assert isinstance(order, dict)
    
    def test_get_open_orders(self):
        open_orders = self.binanace_adapter.get_open_orders()
        assert isinstance(open_orders, list)

    def test_cancel_order(self):
        delete = self.binanace_adapter.cancel_order("BTCUSDT", "492537")
        assert delete