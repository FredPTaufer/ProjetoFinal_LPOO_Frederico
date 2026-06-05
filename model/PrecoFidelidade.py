from .PriceStrategy import PriceStrategy
from .Service import Service


class PrecoFidelidade(PriceStrategy):
    DESCONTO = 0.15

    def calcular(self, servico: Service):
        return servico.preco * (1 - self.DESCONTO)