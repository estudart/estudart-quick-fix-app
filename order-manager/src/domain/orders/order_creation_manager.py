from src.infrastructure.adapters import LoggerAdapter
from src.domain.orders import SimpleOrder



class OrderCreationManager:
    def __init__(self, logger = LoggerAdapter().get_logger()):
        self.logger = logger
        self.order_dict = {
            "simple-order": SimpleOrder
        }

    def create_order(self, strategie: str, order_data: dict):
        try:
            order_class = self.order_dict[strategie]
            order = order_class(**order_data)
            return order
        except Exception as err:
            raise OrderCreationError(f"Could not create order, reason: {err}")


class OrderCreationError(Exception):
    pass