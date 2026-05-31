class AgendamentoController:
    def criar_agendamento(self, dados):
        raise NotImplementedError

    def listar_agendamentos(self):
        raise NotImplementedError

    def concluir(self, id: int):
        raise NotImplementedError

    def cancelar(self, id: int):
        raise NotImplementedError
