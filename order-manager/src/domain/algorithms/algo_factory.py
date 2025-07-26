from src.infrastructure.adapters import LoggerAdapter
from src.domain.algorithms.entities import SpreadCryptoETF



class AlgoFactory:
    def __init__(self, logger = LoggerAdapter().get_logger()):
        self.logger = logger
        self.algo_dict = {
            "spread-crypto-etf": SpreadCryptoETF
        }
        self.active_algos = {}

    def create_algo(self, algo_name: str, algo_data: dict):
        try:
            algo_class = self.algo_dict[algo_name]
            algo = algo_class(algo_data)
            self.active_algos[algo.id] = algo
            return algo
        except Exception as err:
            raise AlgoCreationError(
                f"Could not create algorithm, reason: {err}"
            )

class AlgoCreationError(Exception):
    pass

class AlgoStopError(Exception):
    pass