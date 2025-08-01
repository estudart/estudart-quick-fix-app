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
        required: true
        description: Name of the algo
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            broker:
              type: string
              example: "935"
            account:
              type: string
              example: "1001"
            symbol:
              type: string
              example: "ETHE11"
            side:
              type: string
              example: "BUY"
            quantity:
              type: integer
              example: 100
            spread_threshold:
              type: number
              example: 0.02
          required:
            - broker
            - account
            - symbol
            - side
            - quantity
            - spread_threshold
    responses:
      200:
        description: New algorithm was sent
    """

    return send_algo_request({
        **req.args.to_dict(),
        "algo_data": req.get_json()
    })

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
    
    return cancel_algo_request(req.args.to_dict())
