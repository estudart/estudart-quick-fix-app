import asyncio
import logging
from typing import List

from src.application.data_collectors.data_collector import DataCollector
from src.infrastructure.adapters.inav_md_adapter import InavMDAdapter
from src.infrastructure.adapters.queue.redis_adapter import RedisAdapter


class InavDataCollector(DataCollector):
    def __init__(
        self,
        logger: logging.Logger,
        collector_adapter: InavMDAdapter,
        redis_adapter: RedisAdapter,
        assets_list: List[str]
    ):
        self.logger = logger
        self.collector_adapter = collector_adapter
        self.redis_adapter = redis_adapter
        self.assets_list = assets_list
        self.onshore_offshore_mapping = {
            "BITH11": "HBTC.BH",
            "ETHE11": "HETH.BH",
            "SOLH11": "HSOL.BH"
        }

    def dispatch_price_collected_event(self, channel: str, message_data: dict):
        self.redis_adapter.publish_message(channel, message_data)
        self.logger.info(f"{channel} | Data collected event was dispatched to {channel} channel: {message_data}")

    def mount_message_data(self, asset: str, inav: float, amount_of_underlying_asset: float):
        return {
            "symbol": asset,
            "inav": inav,
            "amount_of_underlying_asset": amount_of_underlying_asset
        }

    async def collect_data(self, asset: str):
        try:
            inav = await asyncio.to_thread(self.collector_adapter.fetch_price, asset)
            # Set inav price to redis
            await asyncio.to_thread(self.redis_adapter.set_key, f"inav:{asset}", inav)
            amount_of_underlying_asset = await asyncio.to_thread(
                self.collector_adapter.get_crypto_quantity_on_onshore_etf,
                asset,
                self.onshore_offshore_mapping[asset]
            )

            self.logger.debug(f"New inav was collected {asset}: {inav}")
            message_data = self.mount_message_data(asset, inav, amount_of_underlying_asset)
            self.dispatch_price_collected_event(f"inav-{asset}", message_data)

        except Exception as err:
            self.logger.error(f"Could not collect inav for {asset}, reason: {err}")

    async def start_collecting(self, asset: str):
        while True:
            await self.collect_data(asset)

    async def run_async(self):
        tasks = [self.start_collecting(asset) for asset in self.assets_list]
        await asyncio.gather(*tasks)

    def run(self):
        asyncio.run(self.run_async())
