import logging
from multiprocessing import Process
import uuid

from src.domain.algorithms import AlgoFactory
from src.application.algorithms.spread_crypto_etf import SpreadCryptoETFAdapter
from src.infrastructure.adapters.clients.order_service_client import OrderServiceClient
from src.infrastructure.adapters.logger_adapter import LoggerAdapter



class AlgoManager:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.algo_factory = AlgoFactory(logger=self.logger)
        self.active_algos: dict[str, Process] = {}

    def start_algo(self, algo_data: dict, algo_name: str) -> None:
        algo_id = str(uuid.uuid4())
        process = Process(target=run_algorithm, args=(algo_id, algo_data, algo_name))
        process.start()
        self.active_algos[algo_id] = process
        return algo_id
    
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


def run_algorithm(id: str, algo_data: dict, algo_name: str) -> None:
    algo_adapter_dict = {
        "spread-crypto-etf": SpreadCryptoETFAdapter
    }
    algo = AlgoFactory().create_algo(id, algo_name, algo_data)
    logger = LoggerAdapter().get_logger()
    algo_adapter = algo_adapter_dict[algo_name](
            logger=logger,
            algo=algo,
            order_service_client=OrderServiceClient(logger)
        )
    algo_adapter.run_algo()