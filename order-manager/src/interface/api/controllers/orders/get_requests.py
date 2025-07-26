from dependency_injector.wiring import inject, Provide
from flask import jsonify

from src.application.orders.order_service import OrderService
from src.infrastructure.adapters.order_adapter import GetOrderError
from src.interface.api.containers import Container



@inject
def get_order_request(data: dict, order_service: OrderService = Provide[Container.order_service]):
    try:
        data = order_service.get_order(**data)
        return jsonify(data), 200
    except GetOrderError as err:
        data = {
            "success": False,
            "message": f"{err}"
        }
        return jsonify(data), 400
    except Exception as err:
        data = {
            "success": False,
            "message": f"Service could compute order, reason: {err}"
        }
        return jsonify(data), 500