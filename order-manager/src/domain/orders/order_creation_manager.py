from src.infrastructure.adapters.logger_adapter import LoggerAdapter
from src.domain.orders.entities import SimpleOrder



class OrderCreationManager:
    def __init__(self, logger = LoggerAdapter().get_logger()):
        self.logger = logger
        self.order_dict = {
            "simple-order": SimpleOrder,
            "futures": SimpleOrder
        }

    def create_order(self, strategy: str, order_data: dict):
        try:
            order_class = self.order_dict[strategy]
            order = order_class(**order_data)
            return order
        except Exception as err:
            raise OrderCreationError(
                f"Could not create order, reason: {err}"
            )


class OrderCreationError(Exception):
    pass