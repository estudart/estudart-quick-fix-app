import pytest
import time

from src.application.algorithms.spread_crypto_etf import SpreadCryptoETFAdapter
from src.application.orders.order_service import OrderService
from src.domain.algorithms.entities import SpreadCryptoETF
from src.infrastructure.adapters import LoggerAdapter, HashdexMDAdapter, BinanceMDAdapter


def make_algo(overrides: dict = None) -> SpreadCryptoETF:
    base_data = {
        "broker": "935",
        "account": "84855",
        "symbol": "BITH11",
        "side": "BUY",
        "quantity": 100,
        "spread_threshold": 0.02
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
        assert self.application_algo.send_stock_order("flowa", "simple-order", 30)

    def test_can_update_stock_order(self):
        order_id = self.application_algo.send_stock_order("flowa", "simple-order", 30)
        update = self.application_algo.update_stock_order(order_id, "flowa", "simple-order", price=55)
        assert update
    
    def test_get_order_placement_price(self):
        stock_fair_price = 150
        spread_threshold = 0.1

        order_placement_price_buy = self.application_algo.get_order_placement_price(
            stock_fair_price=stock_fair_price,
            side="BUY",
            spread_threshold=spread_threshold
        )

        order_placement_price_sell = self.application_algo.get_order_placement_price(
            stock_fair_price=stock_fair_price,
            side="SELL",
            spread_threshold=spread_threshold
        )

        assert order_placement_price_buy == 135
        assert order_placement_price_sell == 165
    
    def test_can_run_cycle(self):
        order_id = self.application_algo.send_stock_order("flowa", "simple-order", 30)
        cumulative_qty = 0
        while cumulative_qty != self.application_algo.algo.algo_data["quantity"]:
            cumulative_qty += self.application_algo.run_cycle(order_id, cumulative_qty)
            time.sleep(5)
        assert cumulative_qty