import pytest

from src.infrastructure import HashdexMDAdapter



class TestHashdexMDAdapter:
    def setup_method(self):
        self.binanace_adapter = HashdexMDAdapter()

    @pytest.mark.parametrize("ticker", ["BITH11", "ETHE11", "SOLH11"])
    def test_fetch_prices(self, ticker: str):
        price = self.binanace_adapter.fetch_price(ticker)
        assert isinstance(price, float)
    
    def test_wrong_ticker_raises_exception(self):
        with pytest.raises(Exception):
            self.binanace_adapter.fetch_price("random")