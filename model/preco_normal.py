from .price_strategy import PriceStrategy
from .servico import Service


class PrecoNormal(PriceStrategy):
    def calcular(self, servico: Service) -> float:
        return servico.preco
