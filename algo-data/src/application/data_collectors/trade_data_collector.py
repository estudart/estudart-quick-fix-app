import time
import logging

from src.application.data_collectors.data_collector import DataCollector
from src.infrastructure.adapters.trade_reporter_adapter import TradeReporter
from src.infrastructure.adapters.queue.redis_adapter import RedisAdapter


class TradeDataCollector(DataCollector):
    def __init__(
        self,
        logger: logging.Logger,
        reporter_adapter: TradeReporter,
        redis_adapter: RedisAdapter
    ):
        self.logger = logger
        self.reporter_adapter = reporter_adapter
        self.redis_adapter = redis_adapter

    def dispatch_trade_report_event(self, message_data: dict):
        channel = f"trade-{message_data['StrategyID']}"
        self.redis_adapter.publish_message(channel, message_data)
        self.logger.info(f"{channel} | Trade report event was dispatched: {message_data}")

    def dispatch_order_report_event(self, message_data: dict):
        channel = f"order-{message_data['StrategyId']}"
        processed_message_data = self.process_order_message_data(message_data)
        self.redis_adapter.publish_message(channel, processed_message_data)
        self.logger.info(f"{channel} | Order report event was dispatched: {processed_message_data}")

    def process_order_message_data(self, message_data: dict):
        return {
            "order_id": message_data["StrategyId"],
            "symbol": message_data["Symbol"],
            "side": message_data["Side"],
            "quantity": message_data["Quantity"],
            "price": message_data["Price"],
            "order_type": message_data["OrderType"],
            "exec_qty": message_data["ExecutedQuantity"],
            "time_in_force": message_data["TimeInForce"],
            "status": message_data["Status"]
        }

    def start_collecting(self):
        while True:
            try:
                ws = self.reporter_adapter.get_ws(self.dispatch_order_report_event)
                ws.run_forever()
            except Exception:
                self.logger.info("WebSocket disconnected. Reconnecting in 5 seconds...")
                time.sleep(5)

    def run(self):
        self.start_collecting()
