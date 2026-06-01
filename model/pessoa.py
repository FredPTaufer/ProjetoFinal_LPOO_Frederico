from abc import ABC, abstractmethod
from .ExcecoesPersonalizadas import CpfInvalidoError


class Pessoa(ABC):
    def __init__(self, nome: str, cpf: str):
        self.nome = nome
        self.cpf  = cpf

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, valor):
        if not valor or not valor.strip():
            raise ValueError("Nome nao pode ser vazio.")
        self.__nome = valor.strip()

    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, valor):
        cpf_limpo = valor.strip().replace(".", "").replace("-", "")
        if not cpf_limpo.isdigit() or len(cpf_limpo) != 11:
            raise CpfInvalidoError("CPF invalido: deve conter exatamente 11 digitos numericos.")
        self.__cpf = cpf_limpo

    def __str__(self):
        return f"{self.__class__.__name__}: {self.nome} (CPF: {self.cpf})"