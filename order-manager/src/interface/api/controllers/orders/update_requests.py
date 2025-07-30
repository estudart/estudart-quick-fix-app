import json

from dependency_injector.wiring import inject, Provide
from flask import jsonify

from src.application.orders.order_service import OrderService
from src.infrastructure.adapters.order_adapter import UpdateOrderError
from src.interface.api.containers import Container



@inject
def update_order_request(data: dict, order_service: OrderService = Provide[Container.order_service]):
    try:
        data = order_service.update_order(
            exchange_name=data["exchange_name"],
            strategy=data["strategy"],
            order_id=data["order_id"],
            **json.loads(data["order_data"])
        )
        return jsonify(data), 200
    except UpdateOrderError as err:
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