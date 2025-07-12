from src.domain import SimpleOrder



class TestSimpleOrder:
    def test_can_create_order(self):
        crypto_order = {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "order_type": "LIMIT",
            "time_in_force": "GTC",
            "quantity": 0.001,
            "price": 30000
        }
        stocks_order = {
            "account": "1001",
            "broker": "005",
            "symbol": "PETR4",
            "side": "BUY",
            "order_type": "LIMIT",
            "time_in_force": "GTC",
            "quantity": 10,
            "price": 30000
        }

        assert SimpleOrder(**crypto_order)
        assert SimpleOrder(**stocks_order)
