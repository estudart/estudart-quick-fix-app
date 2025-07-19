import os

import requests
from dotenv import load_dotenv

from src.infrastructure.adapters.inav_md_adapter import InavMDAdapter
from src.infrastructure.adapters.logger_adapter import LoggerAdapter

load_dotenv()

ENV = os.environ.get("ENV", "DEV")



class HashdexMDAdapter(InavMDAdapter):
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
        self.logger.debug(f"New inav fetched for {ticker}: {price}")
        return price
    
    def get_underlying_asset_quantity(self, price_data: dict) -> float:
        for underlying_asset in price_data["pcf"]:
            if underlying_asset["symbol"] != "Cash":
                return underlying_asset["quantity"]

    def get_crypto_quantity_on_onshore_etf(self, onshore_ticker: str, offshore_ticker: str) -> float:
        suffix = f"inav"

        onshore_request = requests.get(
            url=f"{self.endpoint}/{suffix}/{onshore_ticker}"
        )
        onshore_data = onshore_request.json()
        onshore_shares_quantity_per_creation = onshore_data["info"]["numberOfSharesPerCreationUnit"]
        offshore_quantity_on_onshore = self.get_underlying_asset_quantity(onshore_data)

        offshore_request = requests.get(
            url=f"{self.endpoint}/{suffix}/{offshore_ticker}"
        )
        offshore_data = offshore_request.json()
        crypto_quantity_on_offshore = self.get_underlying_asset_quantity(offshore_data)

        amount_of_crypto_on_onshore = (
            (offshore_quantity_on_onshore * crypto_quantity_on_offshore) 
            / onshore_shares_quantity_per_creation
        )
                
        self.logger.debug(f"New crypto quantity fetched for {onshore_ticker}: {amount_of_crypto_on_onshore}")
        return amount_of_crypto_on_onshore