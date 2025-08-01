from dependency_injector.wiring import inject, Provide
from flask import jsonify

from src.application.orders.order_service import OrderService
from src.infrastructure.adapters.order_adapter import SendOrderError
from src.interface.api.containers import Container



@inject
def send_order_request(data: dict, order_service: OrderService = Provide[Container.order_service]):
    try:
        data = order_service.send_order(
            exchange_name=data["exchange_name"],
            strategy=data["strategy"],
            order_data=data["order_data"]
        )
        return jsonify(data), 200
    except SendOrderError as err:
        data = {
            "success": False,
            "message": f"{err}"
        }
        return jsonify(data), 400
    except Exception as err:
        data = {
            "success": False,
            "message": f"Service could not compute order, reason: {err}"
        }
        return jsonify(data), 500