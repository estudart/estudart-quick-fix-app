from dependency_injector.wiring import inject, Provide

from src.application.orders.order_service import OrderService
from src.infrastructure.adapters.order_adapter import CancelOrderError
from src.interface.api.containers import Container



@inject
def cancel_order_request(data: dict, order_service: OrderService = Provide[Container.order_service]):
    try:
        return {
            "success": True,
            "message": "Order was successfully cancelled",
            "data": order_service.cancel_order(**data)
        }
    except CancelOrderError as err:
        return {
            "success": False,
            "message": f"{err}"
        }
    except Exception as err:
        return {
            "success": False,
            "message": f"Service could not compute order, reason: {err}"
        }