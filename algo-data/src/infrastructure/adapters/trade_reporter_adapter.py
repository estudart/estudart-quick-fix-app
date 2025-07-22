from abc import ABC, abstractmethod

import websocket



class TradeReporter(ABC):
    @abstractmethod
    def get_ws(self) -> websocket.WebSocketApp:
        pass