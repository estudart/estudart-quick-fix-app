import logging

from src.domain.algorithms import AlgoManager
from src.domain.algorithms.entities import Algorithm
from src.application.algorithms.spread_crypto_etf import SpreadCryptoETFAdapter
from src.application.algorithms.base_algorithm import BaseAlgorithm
from src.application.orders.order_service import OrderService
from src.infrastructure.adapters import LoggerAdapter



class AlgoService:
    def __init__(self, logger: logging.Logger = LoggerAdapter().get_logger()):
        self.logger = logger
        self.order_service = OrderService(logger=self.logger)
        self.algo_manager = AlgoManager(logger=self.logger)
        self.algo_adapter_dict = {
            "spread-crypto-etf": SpreadCryptoETFAdapter
        }

    def get_algo_adapter(
            self, 
            algo: Algorithm,
            algo_name: str
        ) -> BaseAlgorithm:

        return self.algo_adapter_dict[algo_name](
            logger=self.logger,
            algo=algo,
            order_service=self.order_service
        )
    
    def start_algo(
            self, 
            algo_name: str, 
            algo_data: dict
        ) -> None:

        try:
            algo = self.algo_manager.create_algo(algo_name, algo_data)
            algo_adapter = self.get_algo_adapter(algo, algo_name)
            algo_adapter.run_algo()
        except Exception as err:
            self.logger.error(f"Could not send order, reason: {err}")
            raise

    def stop_algo(self, algo_id: str) -> bool:
        try:
            self.algo_manager.stop_algo(algo_id)
            return True
        except Exception as err:
            self.logger.error(f"Could not stop algo, reason: {err}")
            return False
