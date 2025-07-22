import pytest

from src.infrastructure import CoinbaseDollarAdapter



class TestCoinbaseDollarAdapter:
    def setup_method(self):
        self.coinbase_dollar_adapter = CoinbaseDollarAdapter()

    @pytest.mark.parametrize("ticker", ["USD"])
    def test_fetch_prices(self, ticker: str):
        price = self.coinbase_dollar_adapter.fetch_price(ticker)
        assert isinstance(price, float)
    
    def test_wrong_ticker_raises_exception(self):
        with pytest.raises(Exception):
            self.coinbase_dollar_adapter.fetch_price("random")