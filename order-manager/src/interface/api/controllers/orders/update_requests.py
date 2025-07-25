import json

from dependency_injector.wiring import inject, Provide

from src.application.orders.order_service import OrderService
from src.infrastructure.adapters.order_adapter import UpdateOrderError
from src.interface.api.containers import Container



@inject
def update_order_request(data: dict, order_service: OrderService = Provide[Container.order_service]):
    try:
        return order_service.update_order(
            exchange_name=data["exchange_name"],
            strategy=data["strategy"],
            order_id=data["order_id"],
            **json.loads(data["order_data"])
        )
    except UpdateOrderError as err:
        return {
            "success": False,
            "message": f"{err}"
        }
    except Exception as err:
        return {
            "success": False,
            "message": f"Service could not compute order, reason: {err}"
        }