from .PriceStrategy import PriceStrategy
from .Service import Service


class PrecoNormal(PriceStrategy):
    def calcular(self, servico: Service) -> float:
        return servico.preco