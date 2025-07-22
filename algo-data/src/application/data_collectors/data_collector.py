from abc import ABC, abstractmethod



class DataCollector(ABC):
    @abstractmethod
    def start_collecting(self):
        pass