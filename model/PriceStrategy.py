from abc import ABC, abstractmethod
from .Service import Service


class PriceStrategy(ABC):
    @abstractmethod
    def calcular(self, servico: Service) -> float:
        pass