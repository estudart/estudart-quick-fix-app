import logging

from src.application.algorithms.algo_manager import AlgoManager
from src.infrastructure.adapters import LoggerAdapter



class AlgoService:
    def __init__(self, logger: logging.Logger = LoggerAdapter().get_logger()):
        self.logger = logger
        self.algo_manager = AlgoManager(logger=self.logger)
        self.logger.info(f"Algo service has successfully started")

    def start_algo(
            self, 
            algo_name: str, 
            algo_data: dict
        ) -> None:

        try:
            return self.algo_manager.start_algo(algo_data, algo_name)
        except Exception as err:
            self.logger.error(f"Could not start algo, reason: {err}")
            raise

    def stop_algo(self, algo_id: str) -> bool:
        return self.algo_manager.stop_algo(algo_id)
