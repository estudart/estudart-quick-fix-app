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

    def stop(self):
        self._stop_event.set()

    def dispatch_trade_report_event(self, message_data: dict):
        channel = f"trade-{message_data['StrategyID']}"
        self.redis_adapter.publish_message(channel, message_data)
        self.logger.info(f"{channel} | Trade report event was dispatched: {message_data}")

    def mount_message_data(self, asset: str, inav: float, amount_of_underlying_asset: float):
        return {
            "symbol": asset,
            "inav": round(inav, 2),
            "amount_of_underlying_asset": amount_of_underlying_asset
        }

    def start_collecting(self):
        while True:
            try:
                ws = self.reporter_adapter.get_ws(self.dispatch_trade_report_event)
                ws.run_forever()
            except Exception:
                self.logger.info("WebSocket disconnected. Reconnecting in 5 seconds...")
                time.sleep(5)

    def run(self):
        self.start_collecting()
