import os

import requests
from dotenv import load_dotenv

from src.infrastructure.adapters.md_adapter import MDAdapter
from src.infrastructure.adapters.logger_adapter import LoggerAdapter

load_dotenv()

ENV = os.environ.get("ENV", "DEV")



class CoinbaseDollarAdapter(MDAdapter):
    def __init__(self, logger = LoggerAdapter().get_logger()):
        self.endpoint = os.environ.get(f"COINBASE_DOLLAR_ENDPOINT_{ENV}")
        self.logger = logger
    
    def fetch_price(self, ticker: str = "USD") -> float:
        suffix = f"exchange-rates"
        params = {"currency": ticker}

        response = requests.get(
            url=f"{self.endpoint}/{suffix}",
            params=params
        )
        price_data = response.json()
        price = round(float(price_data["data"]["rates"]["BRL"]), 4)
        self.logger.info(f"New price fetched for {ticker}: {price}")
        return price
