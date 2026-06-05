from datetime import datetime
from .Cliente import Cliente
from .Profissional import Profissional
from .Service import Service
from .PriceStrategy import PriceStrategy
from .PrecoNormal import PrecoNormal
from .StatusAgendamento import StatusAgendamento
from .ExcecoesPersonalizadas import DataHoraInvalidaError


class Agendamento:
    def __init__(
        self,
        cliente : Cliente,
        profissional : Profissional,
        servico : Service,
        data_hora : datetime,
        estrategia : PriceStrategy = None,
        status : StatusAgendamento = StatusAgendamento.AGENDADO,
        id : int = None
    ):
        self.cliente = cliente
        self.profissional = profissional
        self.servico = servico
        self.data_hora = data_hora
        self.estrategia = estrategia if estrategia else PrecoNormal()
        self.status = status
        self.id = id

    @property
    def cliente(self):
        return self.__cliente

    @cliente.setter
    def cliente(self, valor):
        if valor is None:
            raise ValueError("Cliente não pode ser None.")
        self.__cliente = valor

    @property
    def profissional(self):
        return self.__profissional

    @profissional.setter
    def profissional(self, valor):
        if valor is None:
            raise ValueError("Profissional não pode ser None.")
        self.__profissional = valor

    @property
    def servico(self):
        return self.__servico

    @servico.setter
    def servico(self, valor):
        if valor is None:
            raise ValueError("Serviço não pode ser None.")
        self.__servico = valor

    @property
    def data_hora(self):
        return self.__data_hora

    @data_hora.setter
    def data_hora(self, valor):
        if not isinstance(valor, datetime):
            raise DataHoraInvalidaError("data_hora deve ser um objeto datetime.")
        self.__data_hora = valor

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, valor):
        if not isinstance(valor, StatusAgendamento):
            raise ValueError("Status deve ser um StatusAgendamento válido.")
        self.__status = valor

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, valor):
        self.__id = valor

    def calcularValor(self):
        return self.estrategia.calcular(self.servico)

    def __str__(self):
        return (
            f"Agendamento #{self.id}\n"
            f"  Cliente     : {self.cliente.nome}\n"
            f"  Profissional: {self.profissional.nome}\n"
            f"  Servico     : {self.servico.nome}\n"
            f"  Data/Hora   : {self.data_hora.strftime('%d/%m/%Y %H:%M')}\n"
            f"  Status      : {self.status.value}\n"
            f"  Valor       : R$ {self.calcularValor():.2f}"
        )