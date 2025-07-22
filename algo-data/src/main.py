from multiprocessing import Process

from src.application.data_collectors.inav_data_collector import InavDataCollector
from src.infrastructure.adapters.stocks.hashdex.hashdex_md_adapter import HashdexMDAdapter
from src.application.data_collectors.trade_data_collector import TradeDataCollector
from src.infrastructure.adapters.stocks.flowa.flowa_trade_reporter import FlowaTradeReporter
from src.infrastructure.adapters.logger_adapter import LoggerAdapter
from src.infrastructure.adapters.queue.redis_adapter import RedisAdapter



def start_inav_collector_process(logger):
    inav_collector = InavDataCollector(
        logger=logger,
        collector_adapter=HashdexMDAdapter(logger),
        redis_adapter=RedisAdapter(logger),
        assets_list=["BITH11", "ETHE11", "SOLH11"]
    )
    inav_collector.run()

def start_trade_reporter_process(logger):
    trade_reporter = TradeDataCollector(
        logger=logger,
        reporter_adapter=FlowaTradeReporter(
            channel="orders",
            logger=logger
        ),
        redis_adapter=RedisAdapter(logger)
    )
    trade_reporter.run()


if __name__ == '__main__':
    logger = LoggerAdapter().get_logger()

    process_list: list[Process] = [
        Process(target=start_inav_collector_process, args=(logger, )),
        Process(target=start_trade_reporter_process, args=(logger, ))
    ]

    try:
        for p in process_list:
            p.start()
    except KeyboardInterrupt:
        print("KeyboardInterrupt received. Terminating child processes...")

        for p in process_list:
            p.terminate()
        
        for p in process_list:
            p.join()
        
        print("All processes terminated.")
