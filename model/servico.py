from abc import ABC


class Service(ABC):
    def __init__(self, nome: str, duracao: int, preco: float):
        self.nome = nome
        self.duracao = duracao
        self.preco = preco
