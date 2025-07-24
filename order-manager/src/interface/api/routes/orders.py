from flask import Blueprint, request as req, jsonify

from src.interface.api.controllers.orders import send_order_request



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

     - name: order_data
       in: query
       type: string
       default: '{"symbol":"BTCUSDT","side":"BUY","quantity":0.006,"price":30000,"order_type":"LIMIT","time_in_force":"GTC"}'
       required: True
       description: Parameter of the order
    
    responses:
        200:
            description: New order was sent
            
    """
    try:
        data = req.json()
    except:
        data = req.args.to_dict()
    
    return jsonify(send_order_request(data))