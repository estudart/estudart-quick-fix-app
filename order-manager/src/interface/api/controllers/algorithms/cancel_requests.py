import json

from dependency_injector.wiring import inject, Provide
from flask import jsonify

from src.application.algorithms.algo_service import AlgoService
from src.interface.api.containers import Container



@inject
def cancel_algo_request(data: dict, algo_service: AlgoService = Provide[Container.algo_service]):
    try:
        data = algo_service.stop_algo(algo_id=data["algo_id"])
        return jsonify(data), 200
    except Exception as err:
        data = {
            "success": False,
            "message": f"Service could not compute order, reason: {err}"
        }
        return jsonify(data), 500