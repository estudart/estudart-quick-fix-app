from dependency_injector.wiring import inject, Provide

from src.application.orders.order_service import OrderService
from src.infrastructure.adapters.order_adapter import GetOrderError
from src.interface.api.containers import Container



@inject
def get_order_request(data: dict, order_service: OrderService = Provide[Container.order_service]):
    try:
        return order_service.get_order(**data)
    except GetOrderError as err:
        return {
            "success": False,
            "message": f"{err}"
        }
    except Exception as err:
        return {
            "success": False,
            "message": f"Service could compute order, reason: {err}"
        }