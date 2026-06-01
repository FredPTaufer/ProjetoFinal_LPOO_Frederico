from .PriceStrategy import PriceStrategy
from .Service import Service


class PrecoPromocional(PriceStrategy):
    DESCONTO = 0.20

    def calcular(self, servico: Service) -> float:
        return servico.preco * (1 - self.DESCONTO)