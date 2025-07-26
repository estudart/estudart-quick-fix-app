import pytest
import time

from src.application.algorithms.algo_service import AlgoService
from src.infrastructure.adapters import LoggerAdapter


logger = LoggerAdapter().get_logger()

class TestAlgoService:
    def setup_method(self):
        self.algo_service = AlgoService(
            logger=logger
        )
        self.algo_data = {
            "broker": "935",
            "account": "84855",
            "symbol": "ETHE11",
            "side": "BUY",
            "quantity": 100,
            "spread_threshold": 0.02
        }

    def test_can_start_algo(self):
        algo_id = self.algo_service.start_algo("spread-crypto-etf", self.algo_data)
        time.sleep(20)
        assert self.algo_service.stop_algo(algo_id)
        time.sleep(20)
