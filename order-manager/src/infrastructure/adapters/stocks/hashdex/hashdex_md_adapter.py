import os

import requests
from dotenv import load_dotenv

from src.infrastructure.adapters.md_adapter import MDAdapter
from src.infrastructure.adapters.logger_adapter import LoggerAdapter

load_dotenv()

ENV = os.environ.get("ENV", "DEV")



class HashdexMDAdapter(MDAdapter):
    def __init__(self, logger = LoggerAdapter().get_logger()):
        self.endpoint = os.environ.get(f"HASHDEX_MD_ENDPOINT_{ENV}")
        self.logger = logger
    
    def fetch_price(self, ticker: str) -> float:
        suffix = f"inav"

        response = requests.get(
            url=f"{self.endpoint}/{suffix}/{ticker}"
        )
        price_data = response.json()
        price = float(price_data["inavPerShare"])
        self.logger.info(f"New inav fetched for {ticker}: {price}")
        return price