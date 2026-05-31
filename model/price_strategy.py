from abc import ABC, abstractmethod
from .servico import Service


class PriceStrategy(ABC):
    @abstractmethod
    def calcular(self, servico: Service) -> float:
        raise NotImplementedError
