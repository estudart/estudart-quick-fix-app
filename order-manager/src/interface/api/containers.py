from dependency_injector import containers, providers

from src.infrastructure.adapters.logger_adapter import LoggerAdapter
from src.application.orders.order_service import OrderService
from src.application.algorithms.algo_service import AlgoService



class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.interface.api.controllers.orders.post_requests",
            "src.interface.api.controllers.orders.get_requests",
            "src.interface.api.controllers.orders.cancel_requests",
            "src.interface.api.controllers.orders.update_requests",
            "src.interface.api.controllers.algorithms.post_requests"
        ]
    )  # Adjust this if needed

    logger = providers.Singleton(LoggerAdapter().get_logger)


    order_service = providers.Singleton(
        OrderService,
        logger=logger
    )

    algo_service = providers.Singleton(
        AlgoService,
        logger=logger
    )