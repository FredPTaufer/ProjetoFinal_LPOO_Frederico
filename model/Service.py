from abc import ABC, abstractmethod
from .ExcecoesPersonalizadas import PrecoInvalidoError, DuracaoInvalidaError


class Service(ABC):
    def __init__(self, nome: str, duracao: int, preco: float, id: int = None):
        self.nome    = nome
        self.duracao = duracao
        self.preco   = preco
        self.id      = id

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, valor):
        if not valor or not valor.strip():
            raise ValueError("Nome do servico nao pode ser vazio.")
        self.__nome = valor.strip()

    @property
    def duracao(self):
        return self.__duracao

    @duracao.setter
    def duracao(self, valor):
        if valor <= 0:
            raise DuracaoInvalidaError("Duracao deve ser maior que zero.")
        self.__duracao = valor

    @property
    def preco(self):
        return self.__preco

    @preco.setter
    def preco(self, valor):
        if valor <= 0:
            raise PrecoInvalidoError("Preco deve ser maior que zero.")
        self.__preco = valor

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, valor):
        self.__id = valor

    def __str__(self):
        return (f"{self.__class__.__name__}: {self.nome} "
                f"| Duracao: {self.duracao} min | Preco: R$ {self.preco:.2f}")