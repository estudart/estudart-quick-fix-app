import logging
from threading import Thread
import time

from src.enums import ExchangeEnum, StrategyEnum
from src.domain.algorithms.entities import SpreadCryptoETF
from src.application.algorithms.base_algorithm import BaseAlgorithm
from src.infrastructure.adapters.clients.order_service_client import OrderServiceClient
from src.infrastructure.adapters.queue.redis_adapter import RedisAdapter



class SpreadCryptoETFAdapter(BaseAlgorithm):
    def __init__(
            self,
            logger: logging.Logger,
            algo: SpreadCryptoETF,
            order_service_client: OrderServiceClient
        ):
        self.logger = logger
        self.algo = algo
        self.order_service_client = order_service_client
        self.message_service = RedisAdapter(self.logger)
        self.stocks_exec_qty: int = 0
        self.quantity_crypto_per_stock_share: float = 0

    def run_algo(self):
        etf_symbol = self.algo.algo_data["symbol"]
        inav_data = self.message_service.get_key(f"inav:{etf_symbol}")
        stock_fair_price = float(inav_data["inav"])
        self.quantity_crypto_per_stock_share = float(inav_data["amount_of_underlying_asset"])
        stock_order_placement_price = self.get_order_placement_price(
            stock_fair_price=stock_fair_price,
            side=self.algo.algo_data["side"],
            spread_threshold=self.algo.algo_data["spread_threshold"]
        )

        for attempt in range(1, 4):
            try:
                stock_order_id = self.send_stock_order(
                    exchange_name=ExchangeEnum.FLOWA.value, 
                    strategy=StrategyEnum.SIMPLE_ORDER.value,
                    price=stock_order_placement_price
                )
                break
            except Exception as err:
                self.logger.exception(f"[Attempt {attempt}/3] {err}")
                self.logger.info("Retrying in 5 seconds...")
                time.sleep(5)

        self.subscribe_to_inav_updates(etf_symbol, stock_order_id)
        self.subscribe_to_order_updates(stock_order_id)
        
        self.start_listener_thread()

    def send_crypto_market_order(
            self,
            exchange_name: str,
            strategy: str,
            stock_order_executed_quantity: int,
            quantity_crypto_per_stock_share: float
        ):

        quantity_crypto_to_execute = round(quantity_crypto_per_stock_share * stock_order_executed_quantity, 3)
        self.logger.debug(f"stock order executed quantity: {stock_order_executed_quantity}")
        self.logger.debug(f"quantity_crypto_per_stock_share: {quantity_crypto_per_stock_share}")
        self.logger.debug(f"quantity of crypto execute: {quantity_crypto_to_execute}")
        order_data = self.algo.crypto_order_params_to_dict(quantity_crypto_to_execute)
        
        return self.order_service_client.send_order(exchange_name, strategy, order_data)

    def send_stock_order(self, exchange_name: str, strategy: str, price: float):
        stock_order_params = self.algo.stock_order_params_to_dict(price)
        return self.order_service_client.send_order(exchange_name, strategy, stock_order_params)
    
    def update_stock_order(self, order_id: str, exchange_name: str, strategy: str, order_data: dict):
        return self.order_service_client.update_order(exchange_name, strategy, order_id, order_data)
    
    def get_crypto_order(self,exchange_name: str,strategy: str,order_id: str, symbol: str) -> dict:
        return self.order_service_client.get_order(exchange_name, strategy, order_id, symbol=symbol)

    def get_stock_order(self,exchange_name: str,strategy: str,order_id: str) -> dict:
        return self.order_service_client.get_order(exchange_name, strategy, order_id)

    def get_order_placement_price(self, stock_fair_price: float, side: str, spread_threshold: float) -> float:
        spread = stock_fair_price * spread_threshold

        if side == "BUY":
            return stock_fair_price - spread
        elif side == "SELL":
            return stock_fair_price + spread
        else:
            raise ValueError(f"Invalid order side: '{side}'")
    
    def handle_inav_price_update(self, data: dict, order_id: str):
        if data["symbol"] == self.algo.algo_data["symbol"]:
            self.logger.info(f"[{data['symbol']}] Received INAV update: {data}")

            stock_fair_price = data["inav"]
            self.quantity_crypto_per_stock_share = data["amount_of_underlying_asset"]
            side = self.algo.algo_data["side"]
            spread_threshold = self.algo.algo_data["spread_threshold"]

            stock_order_placement_price = self.get_order_placement_price(
                stock_fair_price=stock_fair_price,
                side=side,
                spread_threshold=spread_threshold
            )
            for attempt in range(1, 4):
                try:
                    self.update_stock_order(
                        order_id=order_id,
                        exchange_name=ExchangeEnum.FLOWA.value,
                        strategy=StrategyEnum.SIMPLE_ORDER.value,
                        order_data={
                            "price": stock_order_placement_price
                        }
                    )
                    break
                except Exception as err:
                    self.logger.exception(f"[Attempt {attempt}/3] Failed to update stock order: {err}")
                    self.logger.info("Retrying in 5 seconds...")
                    time.sleep(5)

    def handle_trade_update(self, data: dict, order_id: str):
        self.logger.info(f"[{order_id}] Executed a new trade: {data}")

    def handle_order_update(self, data: dict, order_id: str):
        self.logger.info(f"[{order_id}] Executed a new trade: {data}")
        exec_qty = data["exec_qty"] - self.stocks_exec_qty
        if exec_qty > 0:
            for attempt in range(1, 4):
                try:
                    self.send_crypto_market_order(
                        exchange_name=ExchangeEnum.BINANCE.value,
                        strategy=StrategyEnum.FUTURES.value,
                        stock_order_executed_quantity=exec_qty,
                        quantity_crypto_per_stock_share=self.quantity_crypto_per_stock_share
                    )
                    break
                except Exception as err:
                    self.logger.exception(f"[Attempt {attempt}/3] Failed to send crypto order: {err}")
                    self.logger.info("Retrying in 5 seconds...")
                    time.sleep(5)
            self.stocks_exec_qty += exec_qty
        
        if self.stocks_exec_qty == self.algo.algo_data["quantity"]:
            ## Finish the algo here....
            self.message_service.unsubscribe(f"inav-{self.algo.algo_data['symbol']}")
            self.message_service.unsubscribe(f"order-{order_id}")
            self.logger.info(f"Algo has been totally executed")
            return
    
    def subscribe_to_inav_updates(self, symbol: str, order_id: str):
        def inav_callback(data):
            self.handle_inav_price_update(data, order_id)
        self.message_service.subscribe(f"inav-{symbol}", inav_callback)

    def subscribe_to_trade_updates(self, order_id: str):
        def trade_callback(data):
            self.handle_trade_update(data, order_id)
        self.message_service.subscribe(f"trade-{order_id}", trade_callback)

    def subscribe_to_order_updates(self, order_id: str):
        def order_callback(data):
            self.handle_order_update(data, order_id)
        self.message_service.subscribe(f"order-{order_id}", order_callback)
    
    def start_listener_thread(self):
        listener_thread = Thread(
            target=self.message_service.start_listening,
            daemon=False
        )
        listener_thread.start()
        listener_thread.join()
