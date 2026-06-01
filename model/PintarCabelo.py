from .Service import Service


class PintarCabelo(Service):
    def __init__(self, preco: float = 150.0, id: int = None):
        super().__init__("Pintar Cabelo", duracao=120, preco=preco, id=id)