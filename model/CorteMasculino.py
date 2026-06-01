from .Service import Service


class CorteMasculino(Service):
    def __init__(self, preco: float = 50.0, id: int = None):
        super().__init__("Corte Masculino", duracao=30, preco=preco, id=id)