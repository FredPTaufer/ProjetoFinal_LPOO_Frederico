from .Service import Service


class Sobrancelha(Service):
    def __init__(self, preco: float = 25.0, id: int = None):
        super().__init__("Sobrancelha", duracao=15, preco=preco, id=id)