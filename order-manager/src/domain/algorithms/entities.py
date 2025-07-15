from abc import ABC, abstractmethod

import uuid

from src.domain.algorithms.enums import AlgoStatus



class Algorithm(ABC):
    def __init__(self, algo_data: dict):
        self.algo_data = algo_data
        self.status = None

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def should_trade(self, spread: float) -> bool:
        pass

    @abstractmethod
    def stock_order_params_to_dict(self):
        pass

    @abstractmethod
    def crypto_order_params_to_dict(self):
        pass


class SpreadCryptoETF(Algorithm):
    def __init__(self, algo_data: dict):
        super().__init__(algo_data)
        self.id = str(uuid.uuid4())
        self.status = AlgoStatus.CREATED
    
    def _validate_params(self):
        pass

    def should_trade(self, spread: float) -> bool:
        return spread > self.algo_data["spread_threshold"]
    
    def stop(self):
        self.status = AlgoStatus.STOPPED
    
    def to_dict(self):
        pass

    def stock_order_params_to_dict(self):
        pass

    def crypto_order_params_to_dict(self):
        pass