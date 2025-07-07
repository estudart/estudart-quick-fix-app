



class Order:
    def __init__(
            self, 
            quantity: float, 
            price: float, 
            symbol: str,
            side: str,
            order_type: str,
            time_in_force: str):
    
        self.quantity = quantity
        self.price = price
        self.symbol = symbol
        self.side = side
        self.order_type = order_type
        self.time_in_force = time_in_force
        self._validate()

    def _validate(self) -> bool:
        if not (
            isinstance(self.quantity, (int, float)) and
            isinstance(self.price, (int, float)) and
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
            "symbol": self.symbol,
            "side": self.side,
            "order_type": self.order_type,
            "time_in_force": self.time_in_force
        }
