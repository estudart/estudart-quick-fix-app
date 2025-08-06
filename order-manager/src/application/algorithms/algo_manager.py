import logging
from multiprocessing import Process
import uuid

from src.domain.algorithms import AlgoFactory
from src.application.algorithms.spread_crypto_etf import SpreadCryptoETFAdapter
from src.infrastructure.adapters.clients.order_service_client import OrderServiceClient
from src.infrastructure.adapters.logger_adapter import LoggerAdapter
from src.infrastructure.adapters.queue.redis_adapter import RedisAdapter



class AlgoManager:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.active_algos: dict[str, Process] = {}
        self.redis_adapter = RedisAdapter(self.logger)

    def start_algo(self, algo_data: dict, algo_name: str) -> None:
        algo_id = str(uuid.uuid4())

        process = Process(target=run_algorithm, args=(algo_id, algo_data, algo_name))
        process.start()

        self.active_algos[algo_id] = process
        return algo_id
    
    def stop_algo(self, algo_id: str) -> bool:
        try:
            process = self.active_algos[algo_id]

            self.redis_adapter.publish_message(f"cancel-{algo_id}")
            
            if process.is_alive():
                self.logger.info(f"Signaling Algo process {algo_id} to stop gracefully...")
                process.join(timeout=10)
                
                if process.is_alive():
                    self.logger.warning(
                        f"Algo process {algo_id} did not terminate gracefully after signal, forcing "
                        "termination."
                    )
                    process.terminate()
                    process.join(timeout=5)
                    if process.is_alive():
                        self.logger.error(
                            f"Algo process {algo_id} still alive after forced termination, killing.")
                        process.kill()
            
            del self.active_algos[algo_id]
            self.logger.info(f"Algo process {algo_id} was stopped.")
            return True
        except KeyError:
            self.logger.error(f"Algo with ID {algo_id} not found in active_algos.")
            return False
        except Exception as err:
            self.logger.exception(f"Error stopping algo {algo_id}: {err}")
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