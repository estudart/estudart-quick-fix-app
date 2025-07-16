import pytest

from src.infrastructure import HashdexMDAdapter



class TestHashdexMDAdapter:
    def setup_method(self):
        self.hashdex_md_adapter = HashdexMDAdapter()

    @pytest.mark.parametrize("ticker", ["BITH11", "ETHE11", "SOLH11"])
    def test_fetch_prices(self, ticker: str):
        price = self.hashdex_md_adapter.fetch_price(ticker)
        assert isinstance(price, float)
    
    def test_wrong_ticker_raises_exception(self):
        with pytest.raises(Exception):
            self.hashdex_md_adapter.fetch_price("random")

    @pytest.mark.parametrize(
        ("onshore_ticker", "offshore_ticker"),
        [
            ("BITH11", "HBTC.BH"),
            ("ETHE11", "HETH.BH"),
            ("SOLH11", "HSOL.BH"),
        ]
    )
    def test_fetch_underlying_quantity(self, onshore_ticker: str, offshore_ticker: str):
        quantity = self.hashdex_md_adapter.get_crypto_quantity_on_onshore_etf(
            onshore_ticker, offshore_ticker
        )
        assert isinstance(quantity, float)
