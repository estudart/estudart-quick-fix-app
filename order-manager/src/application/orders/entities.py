


class Order:
    def __init__(self, quantity: float, price: float, symbol: str):
        self.quantity = quantity
        self.price = price
        self.symbol = symbol
        self._validate()

    def _validate(self) -> bool:
        if not (
            isinstance(self.quantity, float) and
            isinstance(self.price, float) and
            isinstance(self.symbol, str)
        ):
            raise TypeError("Types are incorrect")
        
        if self.quantity <= 0:
            raise ValueError("Quantity should be greater then 0")
        if self.price <= 0:
            raise ValueError("Price should be greater then 0")
        if not self.symbol:
            raise ValueError("Symbol is required")
        
        return True
    
    def to_dict(self) -> dict:
        return {
            "quantity": self.quantity,
            "price": self.price,
            "symbol": self.symbol
        }
