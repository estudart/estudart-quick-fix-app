import json

from src.infrastructure.adapters.clients.order_service_client import OrderServiceClient
from src.infrastructure.adapters.logger_adapter import LoggerAdapter



class TestOrderServiceClient:
    def setup_method(self):
        self.client = OrderServiceClient(LoggerAdapter().get_logger())
    
    def test_client_can_send_crypto_order(self):
        order_data = {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "quantity": 0.006,
            "price": 30000,
            "order_type": "LIMIT",
            "time_in_force": "GTC"
        }
        assert self.client.send_order(exchange_name="binance", strategy="futures", order_data=order_data)