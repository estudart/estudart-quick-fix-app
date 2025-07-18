import pytest
from src.domain.algorithms.entities import SpreadCryptoETF, AlgoStatus


def make_algo(overrides: dict = None):
    base_data = {
        "broker": "935",
        "account": "1001",
        "symbol": "BITH11",
        "side": "BUY",
        "quantity": 0.001,
        "spread_threshold": 0.03
    }
    if overrides:
        base_data.update(overrides)
    return SpreadCryptoETF(algo_data=base_data)


class TestSpreadCryptoETF:

    def test_can_create_algorithm(self):
        assert make_algo()

    def test_missing_broker_raises_exception(self):
        with pytest.raises(ValueError, match="Missing required argument: 'broker'"):
            make_algo({"broker": None})

    def test_missing_account_raises_exception(self):
        with pytest.raises(ValueError, match="Missing required argument: 'account'"):
            make_algo({"account": None})

    def test_missing_symbol_raises_exception(self):
        with pytest.raises(ValueError, match="Missing required argument: 'symbol'"):
            make_algo({"symbol": None})

    def test_missing_side_raises_exception(self):
        with pytest.raises(ValueError, match="Missing required argument: 'side'"):
            make_algo({"side": None})

    def test_missing_quantity_raises_exception(self):
        with pytest.raises(ValueError, match="Missing required argument: 'quantity'"):
            make_algo({"quantity": None})

    def test_missing_spread_threshold_raises_exception(self):
        with pytest.raises(ValueError, match="Missing required argument: 'spread_threshold'"):
            make_algo({"spread_threshold": None})

    def test_shorter_spread_returns_false(self):
        algo = make_algo({"spread_threshold": 0.03})
        assert not algo.should_trade(0.02)

    def test_bigger_spread_returns_true(self):
        algo = make_algo({"spread_threshold": 0.01})
        assert algo.should_trade(0.05)

    def test_stop_algo_set_status_to_stopped(self):
        algo = make_algo()
        algo.stop()
        assert algo.status == AlgoStatus.STOPPED

    def test_unregistered_etf_raises_exception(self):
        algo = make_algo({"symbol": "TEST"})
        with pytest.raises(ValueError, match="'TEST' is not tradable"):
            etf = algo.algo_data["symbol"]
            algo.get_underlying_assets(etf)
