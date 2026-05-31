from abc import ABC


class Pessoa(ABC):
    def __init__(self, nome: str, cpf: str):
        self.nome = nome
        self.cpf = cpf
