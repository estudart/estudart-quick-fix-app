from flask import Blueprint, request as req

from src.interface.api.controllers.orders import (
    send_order_request, 
    get_order_request,
    cancel_order_request,
    update_order_request
)



bp_orders = Blueprint("orders", __name__)

@bp_orders.route("/send-order", methods=["POST"])
def send_order_endpoint():
    """
    Send Order
    ---
    tags:
     - Order

    parameters:
     - name: exchange_name
       in: query
       type: string
       default: 'binance'
       required: True
       description: Name of the exchange

     - name: strategy
       in: query
       type: string
       default: 'futures'
       required: True
       description: Name of the strategy

     - in: body
       name: body
       required: True
       schema:
        type: object
        properties:
          symbol:
            type: string
            example: "BTCUSDT"
          side:
            type: string
            example: "BUY"
          quantity:
            type: number
            example: 0.006
          price:
            type: number
            example: 30000
          order_type:
            type: string
            example: LIMIT
          time_in_force:
            type: string
            example: GTC
        required:
          - symbol
          - side
          - quantity
          - price
          - order_type
          - time_in_force
    
    responses:
        200:
            description: New order was sent
            
    """
    
    return send_order_request({
        **req.args.to_dict(),
        "order_data": req.get_json()
    })

@bp_orders.route("/get-order", methods=["GET"])
def get_order_endpoint():
    """
    Get Order
    ---
    tags:
     - Order

    parameters:
     - name: exchange_name
       in: query
       type: string
       default: 'binance'
       required: True
       description: Name of the exchange

     - name: strategy
       in: query
       type: string
       default: 'futures'
       required: True
       description: Name of the strategy

     - name: symbol
       in: query
       type: string
       default: 'BTCUSDT'
       required: False
       description: Symbol

     - name: order_id
       in: query
       type: string
       default: 'MTB_2_10_250724115927_00432'
       required: True
       description: Parameter of the order
    
    responses:
        200:
            description: New order was sent
            
    """
    
    return get_order_request(req.args.to_dict())

@bp_orders.route("/cancel-order", methods=["DELETE"])
def cancel_order_endpoint():
    """
    Cancel Order
    ---
    tags:
     - Order

    parameters:
     - name: exchange_name
       in: query
       type: string
       default: 'binance'
       required: True
       description: Name of the exchange

     - name: strategy
       in: query
       type: string
       default: 'futures'
       required: True
       description: Name of the strategy

     - name: symbol
       in: query
       type: string
       default: 'BTCUSDT'
       required: False
       description: Symbol

     - name: order_id
       in: query
       type: string
       default: 'MTB_2_10_250724115927_00432'
       required: True
       description: Parameter of the order
    
    responses:
        200:
            description: Order was successfully cancelled
            
    """

    return cancel_order_request(req.args.to_dict())

@bp_orders.route("/update-order", methods=["PUT"])
def update_order_endpoint():
    """
    Update Order
    ---
    tags:
     - Order

    parameters:
     - name: exchange_name
       in: query
       type: string
       default: 'flowa'
       required: True
       description: Name of the exchange

     - name: strategy
       in: query
       type: string
       default: 'simple-order'
       required: True
       description: Name of the strategy

     - name: symbol
       in: query
       type: string
       default: 'BTCUSDT'
       required: False
       description: Symbol

     - name: order_id
       in: query
       type: string
       default: 'MTB_2_10_250724115927_00432'
       required: True
       description: Id of the order

     - in: body
       name: body
       required: True
       schema:
        type: object
        properties:
          price:
            type: number
            example: 75
    
    responses:
        200:
            description: New order was updated
            
    """

    return update_order_request({
        **req.args.to_dict(),
        "order_data": req.get_json()
    })