from datetime import datetime
from .cliente import Cliente
from .profissional import Profissional
from .servico import Service
from .status_agendamento import StatusAgendamento


class Agendamento:
    def __init__(
        self,
        id: int,
        data_hora: datetime,
        cliente: Cliente,
        profissional: Profissional,
        servico: Service,
        status: StatusAgendamento = StatusAgendamento.AGENDADO,
    ):
        self.id = id
        self.data_hora = data_hora
        self.cliente = cliente
        self.profissional = profissional
        self.servico = servico
        self.status = status

    def calcular_valor(self) -> float:
        return self.servico.preco
