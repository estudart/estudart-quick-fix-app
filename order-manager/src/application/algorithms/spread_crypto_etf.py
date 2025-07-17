import time
import logging

from src.domain.algorithms.entities import SpreadCryptoETF
from src.domain.algorithms.enums import AlgoStatus
from src.application.algorithms.base_algorithm import BaseAlgorithm
from src.application.orders.order_service import OrderService
from src.infrastructure.adapters.md_adapter import MDAdapter



class SpreadCryptoETFAdapter(BaseAlgorithm):
    def __init__(
            self,
            logger: logging.getLogger,
            algo: SpreadCryptoETF,
            order_service: OrderService,
            inav_md_adapter: MDAdapter, 
            crypto_md_adapter: MDAdapter
        ):
        self.logger = logger
        self.algo = algo
        self.order_service = order_service
        self.crypto_md_adapter = crypto_md_adapter
        self.inav_md_adapter = inav_md_adapter

    def fetch_crypto_price(self, ticker: str):
        return self.crypto_md_adapter.fetch_price(ticker)

    def fetch_stock_fair_price(self):
        return self.inav_md_adapter.fetch_price(self.algo.algo_data["symbol"])

    def send_crypto_market_order(
            self,
            exchange_name: str,
            strategy: str,
            stock_order_executed_quantity: float
        ):

        onshore_ticker = self.algo.algo_data["symbol"]
        offshore_ticker = self.algo.etf_underlying_assets[onshore_ticker]["offshore_ticker"]

        quantity_crypto_per_stock_share = (
            self.inav_md_adapter.get_crypto_quantity_on_onshore_etf(
                onshore_ticker, offshore_ticker
            )
        )
        quantity_crypto_to_execute = round(quantity_crypto_per_stock_share * stock_order_executed_quantity, 3)
        print(f"quantity of crypto execute: {quantity_crypto_to_execute}")
        order_data = self.algo.crypto_order_params_to_dict(quantity_crypto_to_execute)
        
        return self.order_service.send_order(
            exchange_name, strategy, order_data
        )

    def send_stock_order(
            self,
            exchange_name: str,
            strategy: str,
            price: float
        ):
        return self.order_service.send_order(
            exchange_name, strategy, self.algo.stock_order_params_to_dict(price)
        )
    
    def update_stock_order(
            self, 
            order_id: str,
            exchange_name: str,
            strategy: str,
            **kwargs
        ):
        return self.order_service.update_order(exchange_name, strategy, order_id, **kwargs)
    
    def get_crypto_order(
            self,
            exchange_name: str,
            strategy: str,
            order_id: str, 
            symbol: str
        ) -> dict:
        return self.order_service.get_order(
            exchange_name, strategy, order_id, symbol
        )

    def get_stock_order(
            self,
            exchange_name: str,
            strategy: str,
            order_id: str
        ) -> dict:
        return self.order_service.get_order(
            exchange_name, strategy, order_id
        )

    def get_order_placement_price(self, stock_fair_price: float, side: str, spread_threshold: float) -> float:
        spread = stock_fair_price * spread_threshold

        if side == "BUY":
            return stock_fair_price - spread
        elif side == "SELL":
            return stock_fair_price + spread
        else:
            raise ValueError(f"Invalid order side: '{side}'")

    def run_cycle(
            self,
            stock_order_id: str,
            accumulated_stock_order_exec_qty: int, 
            crypto_exchange_name: str = "binance", 
            stocks_exchange_name: str = "flowa", 
            crypto_strategy_name: str = "futures", 
            stocks_strategy_name: str = "simple-order"
        ):

        try:
            # GET THE ORDER
            stock_order = self.get_stock_order(
                exchange_name=stocks_exchange_name,
                strategy=stocks_strategy_name,
                order_id=stock_order_id
            )

            # GET EXECUTED QTY
            stock_order_executed_quantity = stock_order["exec_qty"] - accumulated_stock_order_exec_qty

            # SEND CRYPTO MARKET ORDER
            if stock_order_executed_quantity > 0:
                self.send_crypto_market_order(
                    exchange_name=crypto_exchange_name,
                    strategy=crypto_strategy_name,
                    stock_order_executed_quantity=stock_order_executed_quantity
                )

            if stock_order["quantity"] != stock_order["exec_qty"] + accumulated_stock_order_exec_qty: 
                # UPDATE PRICE
                self.update_stock_order(
                    order_id=stock_order_id,
                    exchange_name=stocks_exchange_name,
                    strategy=stocks_strategy_name,
                    price=self.fetch_stock_fair_price()
                )
            return stock_order_executed_quantity
        except Exception as err:
            raise SpreadCycleError(f"Could not run spread cycle, reason: {err}")

    def run_algo(self):
        is_first_order = True
        stock_order_id = None
        accumulated_stock_order_exec_qty = 0

        while self.algo.status == AlgoStatus.RUNNING:
            if is_first_order:
                stock_fair_price = self.fetch_stock_fair_price()
                side = self.algo.algo_data["side"]
                spread_threshold = self.algo.algo_data["spread_threshold"]
                
                stock_order_id = self.send_stock_order(
                    exchange_name="flowa",
                    strategy="simple-order",
                    price=self.get_order_placement_price(
                        stock_fair_price=stock_fair_price,
                        side=side,
                        spread_threshold=spread_threshold
                    )
                )
                is_first_order = False
            stock_order_executed_quantity = self.run_cycle(
                stock_order_id, accumulated_stock_order_exec_qty
            )

            accumulated_stock_order_exec_qty += stock_order_executed_quantity
            time.sleep(5)


class SpreadCycleError(Exception):
    pass