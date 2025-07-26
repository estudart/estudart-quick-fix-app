import logging
from multiprocessing import Process

from src.domain.algorithms.entities import Algorithm
from src.application.algorithms.base_algorithm import BaseAlgorithm
from src.application.algorithms.spread_crypto_etf import SpreadCryptoETFAdapter
from src.infrastructure.adapters.clients.order_service_client import OrderServiceClient



class AlgoManager:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.algo_adapter_dict = {
            "spread-crypto-etf": SpreadCryptoETFAdapter
        }
        self.active_algos: dict[str, Process] = {}

    def get_algo_adapter(
            self, 
            algo: Algorithm,
            algo_name: str
        ) -> BaseAlgorithm:

        return self.algo_adapter_dict[algo_name](
            logger=self.logger,
            algo=algo,
            order_service_client=OrderServiceClient(self.logger)
        )

    def run_algorithm(self, algo: Algorithm, algo_name: str):
        algo_adapter = self.get_algo_adapter(algo, algo_name)
        algo_adapter.run_algo()

    def start_algo(self, algo: Algorithm, algo_name: str):
        process = Process(target=self.run_algorithm, args=(algo, algo_name))
        self.active_algos[algo.id] = process
    
    def stop_algo(self, algo_id: str):
        try:
            algo_process = self.active_algos[algo_id]
            algo_process.terminate()
            del self.active_algos[algo_id]
            self.logger.error(f"Algo was stopped, id: {algo_id}")
            return True
        except Exception as err:
            self.logger.error(f"Could not stop algo, reason: {err}")
            return False
