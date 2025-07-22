from enum import Enum



class ExchangeEnum(str, Enum):
    BINANCE = "binance"
    FLOWA = "flowa"

class StrategyEnum(str, Enum):
    SIMPLE_ORDER = "simple-order"
    FUTURES = "futures"