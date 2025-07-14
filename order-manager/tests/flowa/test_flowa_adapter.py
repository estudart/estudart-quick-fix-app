from src.infrastructure import FlowaSimpleOrderAdapter



class TestFlowaAdapter:
    def setup_method(self):
        self.flowa_adapter = FlowaSimpleOrderAdapter()

    def test_create_manage_order(self):
        order_data = {
            "broker": "835",
            "account": "1001",
            "symbol": "BITH11",
            "side": "BUY",
            "quantity": 1,
            "price": 30,
            "order_type": "LIMIT",
            "time_in_force": "GTC"
        }
        order = self.flowa_adapter.send_order(order_data)
        order_id = order["StrategyId"]

        order = self.flowa_adapter.get_order(order_id)
        assert isinstance(order, dict)

        delete = self.flowa_adapter.cancel_order(order_id)
        assert delete
