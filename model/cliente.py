from .pessoa import Pessoa


class Cliente(Pessoa):
    def __init__(self, nome: str, cpf: str, telefone: str = "", email: str = ""):
        super().__init__(nome, cpf)
        self.telefone = telefone
        self.email = email
        self.historico = []
