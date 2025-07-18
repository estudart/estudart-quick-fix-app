from src.application.data_collectors.inav_data_collector import InavDataCollector
from src.infrastructure.adapters.stocks.hashdex.hashdex_md_adapter import HashdexMDAdapter
from src.infrastructure.adapters.logger_adapter import LoggerAdapter
from src.infrastructure.adapters.queue.redis_adapter import RedisAdapter



if __name__ == '__main__':
    logger = LoggerAdapter().get_logger()
    inav_collector = InavDataCollector(
        logger=logger,
        collector_adapter=HashdexMDAdapter(logger),
        redis_adapter=RedisAdapter(logger),
        assets_list=["BITH11", "ETHE11", "SOLH11"]
    )
    inav_collector.run()