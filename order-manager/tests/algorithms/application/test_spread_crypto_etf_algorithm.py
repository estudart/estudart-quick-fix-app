import pytest

from src.application.algorithms.spread_crypto_etf import SpreadCryptoETFAdapter
from src.application.orders.order_service import OrderService
from src.domain.algorithms.entities import SpreadCryptoETF
from src.infrastructure.adapters import LoggerAdapter, HashdexMDAdapter, BinanceMDAdapter


def make_algo(overrides: dict = None) -> SpreadCryptoETF:
    base_data = {
        "broker": "935",
        "account": "1001",
        "symbol": "BITH11",
        "side": "BUY",
        "quantity": 1,
        "spread_threshold": 0.03
    }
    if overrides:
        base_data.update(overrides)
    return SpreadCryptoETF(algo_data=base_data)

logger = LoggerAdapter().get_logger()

class TestSpreadCryptoETFAdapter:
    def setup_method(self):
        self.application_algo = SpreadCryptoETFAdapter(
            logger=logger,
            algo=make_algo(),
            order_service=OrderService(logger),
            inav_md_adapter=HashdexMDAdapter(logger),
            crypto_md_adapter=BinanceMDAdapter(logger)
        )

    def test_can_generate_stocks_order_params(self):
        stocks_order_params = self.application_algo.algo.stock_order_params_to_dict(30)
        print(stocks_order_params)

    def test_can_send_stock_order(self):
        assert self.application_algo.send_stock_order(
            "flowa", "simple-order", 30
        )
