from .Pessoa import Pessoa


class Profissional(Pessoa):
    def __init__(self, nome: str, cpf: str, especialidade: str, id: int = None):
        super().__init__(nome, cpf)
        self.especialidade = especialidade
        self.id = id
        self.__servicos = []

    @property
    def especialidade(self):
        return self.__especialidade

    @especialidade.setter
    def especialidade(self, valor):
        if not valor or not valor.strip():
            raise ValueError("Especialidade não pode ser vazia.")
        self.__especialidade = valor.strip()

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, valor):
        self.__id = valor

    @property
    def servicos(self):
        return list(self.__servicos)

    def adicionarServico(self, servico):
        self.__servicos.append(servico)

    def podeRealizar(self, servico):
        return any(type(s).__name__ == type(servico).__name__ for s in self.__servicos)

    def __str__(self):
        return (f"Profissional: {self.nome} | CPF: {self.cpf} | Especialidade: {self.especialidade}")