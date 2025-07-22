import time

from src.infrastructure.adapters.stocks.flowa.flowa_trade_reporter import FlowaTradeReporter
from src.infrastructure.adapters.logger_adapter import LoggerAdapter



class TestFlowaTradeReporter:
    def setup_method(self):
        self.logger = LoggerAdapter().get_logger()
        self.trade_reporter = FlowaTradeReporter(
            channel="orders",
            logger=self.logger
        )

    def test_can_connect_websocket(self):
        def callback_method(message_data):
            self.logger.info(message_data)
        attempts = 0
        while attempts < 3:
            try:
                ws = self.trade_reporter.get_ws(callback_method)
                ws.run_forever()
            except Exception as err:
                self.logger.error(err)
            attempts+=1
            self.logger.info(f"Attempt {attempts} | WebSocket disconnected. Reconnecting in 30 seconds...")
            time.sleep(30)

