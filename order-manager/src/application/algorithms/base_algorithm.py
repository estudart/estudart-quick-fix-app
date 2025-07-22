from abc import ABC, abstractmethod



class BaseAlgorithm(ABC):
    @abstractmethod
    def run_algo(self):
        pass