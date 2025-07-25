import pytest

from src.infrastructure import BinanceFuturesOrderAdapter, CancelOrderError, GetOrderError, SendOrderError



class TestBinanceFuturesAdapter:
    def setup_method(self):
        self.binance_adapter = BinanceFuturesOrderAdapter()

    def test_create_manage_order(self):
        order_data = {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "quantity": 0.006,
            "price": 30000,
            "order_type": "LIMIT",
            "time_in_force": "GTC"
        }
        order_id = self.binance_adapter.send_order(order_data)

        order = self.binance_adapter.get_order(order_id, symbol=order_data["symbol"])
        assert isinstance(order, dict)

        delete = self.binance_adapter.cancel_order(order_id, symbol=order_data["symbol"])
        assert delete

    def test_market_order(self):
        order_data = {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "quantity": 0.006,
            "order_type": "MARKET"
        }
        order_id = self.binance_adapter.send_order(order_data)

        order = self.binance_adapter.get_order(order_id, symbol=order_data["symbol"])
        assert isinstance(order, dict)
    
    def test_get_open_orders(self):
        open_orders = self.binance_adapter.get_open_orders()
        assert isinstance(open_orders, list)

    def test_get_order_without_symbol_raises_exception(self):
        order_id = "testing"
        with pytest.raises(GetOrderError, match="Missing required argument: 'symbol'"):
            self.binance_adapter.get_order(order_id)
    
    def test_cancel_order_without_symbol_raises_exception(self):
        order_id = "testing"
        with pytest.raises(CancelOrderError, match="Missing required argument: 'symbol'"):
            self.binance_adapter.cancel_order(order_id)
