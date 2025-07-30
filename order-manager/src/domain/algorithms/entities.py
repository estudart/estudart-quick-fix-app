from abc import ABC, abstractmethod

from src.domain.algorithms.enums import AlgoStatus



class Algorithm(ABC):
    def __init__(self, id: str, algo_data: dict):
        self.id = id
        self.algo_data = algo_data
        self.status = None

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def should_trade(self, spread: float) -> bool:
        pass

    @abstractmethod
    def stock_order_params_to_dict(self, price: float):
        pass

    @abstractmethod
    def crypto_order_params_to_dict(self, quantity: float, side: str) -> dict:
        pass


"""
ALGO DATA MODEL
algo_data = {
    "broker": "935",
    "account": "84855",
    "symbol": "BITH11",
    "side": "BUY",
    "quantity": 100,
    "spread_threshold": 0.01
}
"""


class SpreadCryptoETF(Algorithm):
    def __init__(self, id: str, algo_data: dict):
        super().__init__(id, algo_data)
        self.status = AlgoStatus.CREATED
        self.etf_underlying_assets = {
            "BITH11": {
                "is_single_asset": True,
                "underlying_assets": ["BTCUSDT"]
            },
            "ETHE11": {
                "is_single_asset": True,
                "underlying_assets": ["ETHUSDT"]
            },
            "SOLH11": {
                "is_single_asset": True,
                "underlying_assets": ["SOLUSDT"]
            }
        }
        self._validate_params()
    
    def _validate_params(self):
        if not self.algo_data.get("broker"):
            raise ValueError("Missing required argument: 'broker'")
        if not self.algo_data.get("account"):
            raise ValueError("Missing required argument: 'account'")
        if not self.algo_data.get("symbol"):
            raise ValueError("Missing required argument: 'symbol'")
        if not self.algo_data.get("side"):
            raise ValueError("Missing required argument: 'side'")
        if not self.algo_data.get("quantity"):
            raise ValueError("Missing required argument: 'quantity'")
        if not self.algo_data.get("spread_threshold"):
            raise ValueError("Missing required argument: 'spread_threshold'")

    def should_trade(self, spread: float) -> bool:
        return spread > self.algo_data["spread_threshold"]
    
    def stop(self):
        self.status = AlgoStatus.STOPPED
    
    def to_dict(self):
        pass

    def get_underlying_assets(self, etf: str) -> list[str]:
        available = list(self.etf_underlying_assets.keys())
        if not etf in available:
            raise ValueError(
                f"Selected ETF '{etf}' is not tradable by this strategy. "
                f"Available options: {available}"
            )
        underlying_assets = self.etf_underlying_assets[etf]["underlying_assets"]
        return underlying_assets

    def stock_order_params_to_dict(self, price: float) -> dict:
        return {
            **self.algo_data,
            "price": price,
            "order_type": "LIMIT",
            "time_in_force": "GTC"
        }

    def crypto_order_params_to_dict(self, quantity: float) -> dict:
        etf = self.algo_data["symbol"]
        return {
            "symbol": self.get_underlying_assets(etf)[0],
            "side": "BUY" if self.algo_data["side"] == "SELL" else "SELL",
            "quantity": quantity,
            "order_type": "MARKET"
        }