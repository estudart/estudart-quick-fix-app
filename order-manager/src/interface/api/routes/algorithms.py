from flask import Blueprint, request as req

from src.interface.api.controllers.algorithms import (
    send_algo_request,
    cancel_algo_request 
)



bp_algos = Blueprint("algorithms", __name__)

@bp_algos.route("/send-algo", methods=["POST"])
def send_algo_endpoint():
    """
    Send Algo
    ---
    tags:
     - Algorithm

    parameters:
     - name: algo_name
       in: query
       type: string
       default: 'spread-crypto-etf'
       required: True
       description: Name of the algo

     - name: algo_data
       in: query
       type: string
       default: '{
            "broker": "935",
            "account": "84855",
            "symbol": "ETHE11",
            "side": "BUY",
            "quantity": 100,
            "spread_threshold": 0.02
        }'
       required: True
       description: Parameter of the algorithm
    
    responses:
        200:
            description: New algorithm was sent
            
    """
    try:
        data = req.json()
    except:
        data = req.args.to_dict()
    
    return send_algo_request(data)

@bp_algos.route("/cancel-algo", methods=["DELETE"])
def cancel_algo_endpoint():
    """
    Cancel Algo
    ---
    tags:
     - Algorithm

    parameters:
     - name: algo_id
       in: query
       type: string
       default: '9125ff34-d180-4070-9360-d09e0aa2b3af'
       required: True
       description: Name of the algo
    
    responses:
        200:
            description: Algorithm was cancelled
            
    """
    try:
        data = req.json()
    except:
        data = req.args.to_dict()
    
    return cancel_algo_request(data)
