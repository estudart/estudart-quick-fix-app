import logging
import threading
import multiprocessing
import time

from src.decorators import retry_decorator
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
            order_service_client: OrderServiceClient,
            cancel_event: multiprocessing.Event # type: ignore
        ):
        self.logger = logger
        self.algo = algo
        self.order_service_client = order_service_client
        self.message_service = RedisAdapter(self.logger)
        self.cancel_event = cancel_event
        self.stop_cancellation_event_thread = threading.Event()

        self.stock_order_id = None
        self.stocks_exec_qty: int = 0
        self.stock_order_price = None
        self.quantity_crypto_per_stock_share: float = 0
        self.retry_time: int = 1

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
        # Update the current price of the order
        self.stock_order_price = stock_order_placement_price
        # Send first order to start the algo
        try:
            self.stock_order_id = self.send_stock_order(stock_order_placement_price)
        except Exception as err:
            self.logger.error(f"Could not send stock order after multiple retries, reason: {err}")
            self.cancel_event.set()
        # Subscribe update events
        self.subscribe_to_inav_updates(etf_symbol, self.stock_order_id)
        self.subscribe_to_order_updates(self.stock_order_id)
        # Start threads
        self.start_cancellation_event_thread()
        self.start_listener_thread()

    def get_order_placement_price(self, stock_fair_price: float, side: str, spread_threshold: float) -> float:
        spread = stock_fair_price * spread_threshold

        if side == "BUY":
            return stock_fair_price - spread
        elif side == "SELL":
            return stock_fair_price + spread
        else:
            raise ValueError(f"Invalid order side: '{side}'")
    
    @retry_decorator(max_retries=4, delay=1)
    def send_stock_order(self, stock_order_placement_price: float) -> str:
        return self.order_service_client.send_order(
            ExchangeEnum.FLOWA.value, 
            StrategyEnum.SIMPLE_ORDER.value, 
            order_data=self.algo.stock_order_params_to_dict(
                stock_order_placement_price
            )
        )
    
    @retry_decorator(max_retries=4, delay=1)
    def send_crypto_order(self, exec_qty, quantity_crypto_per_stock_share):
        quantity_crypto_to_execute = round(quantity_crypto_per_stock_share * exec_qty, 3)
        return self.order_service_client.send_order(
            exchange_name=ExchangeEnum.BINANCE.value, 
            strategy=StrategyEnum.FUTURES.value, 
            order_data=self.algo.crypto_order_params_to_dict(quantity_crypto_to_execute)
        )

    @retry_decorator(max_retries=4, delay=1)
    def update_stock_order(self, stock_order_id: str, stock_order_placement_price):
        self.order_service_client.update_order(
            order_id=stock_order_id,
            exchange_name=ExchangeEnum.FLOWA.value,
            strategy=StrategyEnum.SIMPLE_ORDER.value,
            order_data={
                "price": stock_order_placement_price
            }
        )
        return True
    
    @retry_decorator(max_retries=4, delay=1)
    def cancel_stock_order(self):
        return self.order_service_client.cancel_order(
            exchange_name=ExchangeEnum.FLOWA.value,
            strategy=StrategyEnum.SIMPLE_ORDER.value,
            order_id=self.stock_order_id
        )

    def is_finished(self):
        return self.stocks_exec_qty == self.algo.algo_data["quantity"]
    
    def handle_inav_price_update(self, data: dict, order_id: str):
        if self.is_finished():
            return
        
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

            if round(stock_order_placement_price, 2) != round(self.stock_order_price, 2):
                try:
                    self.update_stock_order(self.stock_order_id, stock_order_placement_price)
                    # Update the current price of the order
                    self.stock_order_price = stock_order_placement_price
                except Exception as err:
                    self.logger.error(f"Could not update stock order after multiple retries, reason: {err}")
                    self.cancel_event.set()

    def handle_order_update(self, data: dict, order_id: str):
        self.logger.info(f"[{order_id}] Received an order event: {data}")
        exec_qty = data["exec_qty"] - self.stocks_exec_qty
        if exec_qty > 0:
            try:
                self.send_crypto_order(exec_qty, self.quantity_crypto_per_stock_share)
            except Exception as err:
                self.logger.error(f"Could not send crypto order after multiple retries, reason: {err}")
                self.cancel_event.set()
            self.stocks_exec_qty += exec_qty
        
        if self.is_finished():
            # Finish the algo here....
            self.logger.info(f"Algo has been totally executed")
            # Stop all listeners to update channels.
            self.stop_listeners()
            # Stop cancellation thread, as the algo is finished, there is no way it can be cancelled any longer.
            self.stop_cancellation_event_thread.set()
            return
        
    def subscribe_to_inav_updates(self, symbol: str, order_id: str):
        def inav_callback(data):
            self.handle_inav_price_update(data, order_id)
        self.message_service.subscribe(f"inav-{symbol}", inav_callback)

    def subscribe_to_order_updates(self, order_id: str):
        def order_callback(data):
            self.handle_order_update(data, order_id)
        self.message_service.subscribe(f"order-{order_id}", order_callback)

    def monitor_cancellation(self):
        # Start periodically checking for cancel requests
        self.logger.info(f"Cancellation thread listener started...")
        while not self.cancel_event.is_set():
            if self.stop_cancellation_event_thread.is_set():
                return
            time.sleep(0.5)
        self.logger.info(f"Cancellation event was triggered.")
        # Stop all listeners to update channels.
        self.stop_listeners()
        # Cancel stock order
        self.logger.info(f"Cancelling stock order...")
        self.cancel_stock_order()
        return
    
    def start_listener_thread(self):
        listener_thread = threading.Thread(
            target=self.message_service.start_listening,
            daemon=False
        )
        listener_thread.start()
        listener_thread.join()

    def stop_listeners(self):
        self.logger.info(f"Unsubscribing channels on pubsub...")
        self.message_service.unsubscribe(f"inav-{self.algo.algo_data['symbol']}")
        self.message_service.unsubscribe(f"order-{self.stock_order_id}")

    def start_cancellation_event_thread(self):
        monitor_cancellation_event_thread = threading.Thread(
            target=self.monitor_cancellation,
            daemon=False
        )
        monitor_cancellation_event_thread.start()
