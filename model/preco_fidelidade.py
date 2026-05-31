from .price_strategy import PriceStrategy
from .servico import Service


class PrecoFidelidade(PriceStrategy):
    def calcular(self, servico: Service) -> float:
        return servico.preco * 0.85
