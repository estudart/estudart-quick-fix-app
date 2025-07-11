from src.infrastructure.adapters.stocks.flowa.flowa_adapter import FlowaAdapter


class FlowaSimpleOrderAdapter(FlowaAdapter):
    def __init__(self):
        super().__init__()