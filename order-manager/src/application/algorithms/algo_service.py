import logging

from src.domain.algorithms import AlgoManager
from src.domain.algorithms.entities import Algorithm
from src.application.algorithms.spread_crypto_etf import SpreadCryptoETFAdapter
from src.application.algorithms.base_algorithm import BaseAlgorithm
from src.application.orders.order_service import OrderService
from src.infrastructure.adapters import LoggerAdapter
from src.infrastructure.adapters.stocks.hashdex.hashdex_md_adapter import HashdexMDAdapter
from src.infrastructure.adapters.md_adapter import MDAdapter



class AlgoService:
    def __init__(self, logger: logging.Logger = LoggerAdapter().get_logger()):
        self.logger = logger
        self.order_service = OrderService(logger=self.logger)
        self.algo_manager = AlgoManager(logger=self.logger)
        self.algo_adapter_dict = {
            "spread-crypto-etf": SpreadCryptoETFAdapter
        }
        self.inav_md_adapter_dict = {
            "hashdex": HashdexMDAdapter(self.logger)
        }

    def get_inav_md_adapter(self, inav_md_provider: str) -> MDAdapter:
        return self.inav_md_adapter_dict[inav_md_provider]

    def get_algo_adapter(
            self, 
            algo: Algorithm,
            algo_name: str, 
            inav_md_provider: str
        ) -> BaseAlgorithm:

        return self.algo_adapter_dict[algo_name](
            logger=self.logger,
            algo=algo,
            order_service=self.order_service,
            inav_md_adapter=self.get_inav_md_adapter(inav_md_provider)
        )
    
    def start_algo(
            self, 
            algo_name: str, 
            algo_data: dict, 
            inav_md_provider: str = "hashdex"
        ) -> None:

        try:
            algo = self.algo_manager.create_algo(algo_name, algo_data)
            algo_adapter = self.get_algo_adapter(
                algo, algo_name, inav_md_provider
            )
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
