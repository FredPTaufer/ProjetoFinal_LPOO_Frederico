from .Service import Service


class Barba(Service):
    def __init__(self, preco: float = 35.0, id: int = None):
        super().__init__("Barba", duracao=20, preco=preco, id=id)