



class SimpleOrder:
    def __init__(
            self, 
            quantity: float, 
            price: float, 
            symbol: str,
            side: str,
            order_type: str,
            time_in_force: str,
            **kwargs
        ):
    
        self.quantity = quantity
        self.price = price
        self.symbol = symbol
        self.side = side
        self.order_type = order_type
        self.time_in_force = time_in_force
        self.broker = kwargs.get("broker", None)
        self.account = kwargs.get("account", None)
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
        order_data = {
            "quantity": self.quantity,
            "price": self.price,
            "symbol": self.symbol,
            "side": self.side,
            "order_type": self.order_type,
            "time_in_force": self.time_in_force
        }
        # Logic for sending orders to Flowa
        if self.broker:
            order_data.update(
                broker=self.broker,
                account=self.account
            )
        return order_data
