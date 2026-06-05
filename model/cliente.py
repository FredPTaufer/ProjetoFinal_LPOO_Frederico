from .Pessoa import Pessoa


class Cliente(Pessoa):
    def __init__(self, nome: str, cpf: str, telefone: str, email: str, id: int = None):
        super().__init__(nome, cpf)
        self.telefone = telefone
        self.email = email
        self.id = id
        self.__historico = []

    @property
    def telefone(self):
        return self.__telefone

    @telefone.setter
    def telefone(self, valor):
        if not valor or not valor.strip():
            raise ValueError("Telefone não pode ser vazio.")
        self.__telefone = valor.strip()

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):
        if not valor or not valor.strip():
            raise ValueError("Email não pode ser vazio.")
        self.__email = valor.strip()

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, valor):
        self.__id = valor

    @property
    def historico(self):
        return list(self.__historico)

    def adicionarAgendamento(self, agendamento):
        self.__historico.append(agendamento)

    def listarHistorico(self):
        return list(self.__historico)

    def __str__(self):
        return (f"Cliente: {self.nome} | CPF: {self.cpf} | Tel: {self.telefone} | Email: {self.email}")