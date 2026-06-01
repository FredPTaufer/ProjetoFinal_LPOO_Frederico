from .Service import Service


class CorteFeminino(Service):
    def __init__(self, preco: float = 80.0, id: int = None):
        super().__init__("Corte Feminino", duracao=60, preco=preco, id=id)