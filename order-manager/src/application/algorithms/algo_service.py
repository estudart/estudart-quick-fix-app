import logging

from src.domain.algorithms import AlgoManager
from src.domain.algorithms.entities import Algorithm
from src.application.algorithms.spread_crypto_etf import SpreadCryptoETFAdapter
from src.application.algorithms.base_algorithm import BaseAlgorithm
from src.application.orders.order_service import OrderService
from src.infrastructure.adapters import LoggerAdapter
from src.infrastructure.adapters.crypto.binance.binance_md_adapter import BinanceMDAdapter
from src.infrastructure.adapters.stocks.hashdex.hashdex_md_adapter import HashdexMDAdapter
from src.infrastructure.adapters.crypto.coinbase.coinbase_dollar_adapter import CoinbaseDollarAdapter
from src.infrastructure.adapters.md_adapter import MDAdapter



class AlgoService:
    def __init__(self, logger: logging.Logger = LoggerAdapter().get_logger()):
        self.logger = logger
        self.order_service = OrderService(logger=self.logger)
        self.algo_manager = AlgoManager(logger=self.logger)
        self.algo_adapter_dict = {
            "spread-crypto-etf": SpreadCryptoETFAdapter
        }
        self.crypto_md_adapter_dict = {
            "binance": BinanceMDAdapter(self.logger)
        }
        self.inav_md_adapter_dict = {
            "hashdex": HashdexMDAdapter(self.logger)
        }
        self.dollar_adapter_dict = {
            "coinbase": CoinbaseDollarAdapter(self.logger)
        }
    
    def get_crypto_md_adapter(self, crypto_md_provider: str) -> MDAdapter:
        return self.crypto_md_adapter_dict[crypto_md_provider]

    def get_inav_md_adapter(self, inav_md_provider: str) -> MDAdapter:
        return self.inav_md_adapter_dict[inav_md_provider]
    
    def get_dollar_adapter(self, dollar_provider: str) -> MDAdapter:
        return self.dollar_adapter_dict[dollar_provider]

    def get_algo_adapter(
            self, 
            algo: Algorithm,
            algo_name: str, 
            inav_md_provider: str, 
            crypto_md_provider: str
        ) -> BaseAlgorithm:

        return self.algo_adapter_dict[algo_name](
            logger=self.logger,
            algo=algo,
            order_service=self.order_service,
            inav_md_adapter=self.get_inav_md_adapter(inav_md_provider),
            crypto_md_adapter=self.get_crypto_md_adapter(crypto_md_provider),
        )
    
    def start_algo(
            self, 
            algo_name: str, 
            algo_data: dict, 
            inav_md_provider: str = "hashdex", 
            crypto_md_provider: str = "binance"
        ) -> None:

        try:
            algo = self.algo_manager.create_algo(algo_name, algo_data)
            algo_adapter = self.get_algo_adapter(
                algo, algo_name, inav_md_provider, crypto_md_provider
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
