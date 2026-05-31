from typing import List
from .pessoa import Pessoa


class Profissional(Pessoa):
    def __init__(self, nome: str, cpf: str, especialidade: str = "", disponivel: bool = True):
        super().__init__(nome, cpf)
        self.especialidade = especialidade
        self.servicos: List[str] = []
        self.disponivel = disponivel
