import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime, date, time, timedelta
from dao.AgendamentoDAO import AgendamentoDAO
from dao.ClienteDAO import ClienteDAO
from dao.ProfissionalDAO import ProfissionalDAO
from dao.ServicoDAO import ServicoDAO
from model.Agendamento import Agendamento
from model.StatusAgendamento import StatusAgendamento
from model.PrecoNormal import PrecoNormal
from model.PrecoPromocional import PrecoPromocional
from model.PrecoFidelidade import PrecoFidelidade
from model.ExcecoesPersonalizadas import DataHoraInvalidaError


def _string_para_estrategia(valor: str):
    if valor.strip().lower() == "promocional":
        return PrecoPromocional()
    if valor.strip().lower() == "fidelidade":
        return PrecoFidelidade()
    return PrecoNormal()


class AgendamentoController:
    def __init__(self):
        self.agendamento_dao = AgendamentoDAO()
        self.cliente_dao = ClienteDAO()
        self.profissional_dao = ProfissionalDAO()
        self.servico_dao = ServicoDAO()

    def listar_agendamentos(self):
        try:
            return self.agendamento_dao.listar_todos()
        except Exception as e:
            print(f"Erro ao listar agendamentos: {e}")
            return []

    def buscar_por_id(self, id_agendamento: int):
        try:
            return self.agendamento_dao.buscar_por_id(id_agendamento)
        except Exception as e:
            print(f"Erro ao buscar agendamento: {e}")
            return None

    def buscar_por_cliente(self, id_cliente: int):
        try:
            return self.agendamento_dao.buscar_por_cliente(id_cliente)
        except Exception as e:
            print(f"Erro ao buscar agendamentos do cliente: {e}")
            return []

    def horarios_disponiveis(self, id_profissional: int, id_servico: int, data_str: str):
        try:
            data_obj = datetime.strptime(data_str.strip(), "%d/%m/%Y").date()
            servico = self.servico_dao.buscar_por_id(id_servico)
            if not servico:
                return []

            duracao = servico.duracao
            agora   = datetime.now()

            periodos = [(time(8,  0), time(12, 0)),(time(13, 0), time(17, 0)),]

            slots = []
            for inicio, fim in periodos:
                slot = datetime.combine(data_obj, inicio)
                fim_dt = datetime.combine(data_obj, fim)

                while slot + timedelta(minutes=duracao) <= fim_dt:
                    if slot > agora:
                        conflito = self.agendamento_dao.verificar_conflito(id_profissional, slot, duracao)
                        if not conflito:
                            slots.append(slot)
                    slot += timedelta(minutes=duracao)

            return slots

        except Exception as e:
            print(f"Erro ao buscar horários disponíveis: {e}")
            return []

    def criar_agendamento(self, id_cliente: int, id_profissional: int, id_servico: int, data_hora_str: str, estrategia_str: str = "normal"):
        if not id_cliente or not id_profissional or not id_servico or not data_hora_str:
            return False, "Todos os campos são obrigatórios."

        try:
            data_hora = datetime.strptime(data_hora_str.strip(), "%d/%m/%Y %H:%M")

            if data_hora < datetime.now():
                return False, "A data e hora do agendamento devem ser futuras."

            cliente = self.cliente_dao.buscar_por_id(id_cliente)
            profissional = self.profissional_dao.buscar_por_id(id_profissional)
            servico = self.servico_dao.buscar_por_id(id_servico)

            if not cliente:
                return False, "Cliente não encontrado."
            if not profissional:
                return False, "Profissional não encontrado."
            if not servico:
                return False, "Serviço não encontrado."

            if self.agendamento_dao.verificar_conflito(id_profissional, data_hora, servico.duracao):
                return False, (
                    f"O profissional já possui um atendimento neste período.\n"
                    f"O serviço '{servico.nome}' dura {servico.duracao} minutos.\n"
                    "Escolha outro horário."
                )

            estrategia  = _string_para_estrategia(estrategia_str)
            agendamento = Agendamento(
                cliente = cliente,
                profissional = profissional,
                servico = servico,
                data_hora = data_hora,
                estrategia = estrategia,
                status = StatusAgendamento.AGENDADO
            )
            return self.agendamento_dao.salvar(agendamento)

        except ValueError:
            return False, "Formato de data inválido. Use DD/MM/AAAA HH:MM."
        except DataHoraInvalidaError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro ao criar agendamento: {e}"

    def atualizar_agendamento(self, id_agendamento: int, id_cliente: int, id_profissional: int, id_servico: int, data_hora_str: str, estrategia_str: str, status_str: str):
        if not all([id_agendamento, id_cliente, id_profissional, id_servico, data_hora_str, estrategia_str, status_str]):
            return False, "Todos os campos são obrigatórios."

        try:
            data_hora = datetime.strptime(data_hora_str.strip(), "%d/%m/%Y %H:%M")

            agendamento = self.agendamento_dao.buscar_por_id(id_agendamento)
            if not agendamento:
                return False, "Agendamento não encontrado para edição."

            cliente = self.cliente_dao.buscar_por_id(id_cliente)
            profissional = self.profissional_dao.buscar_por_id(id_profissional)
            servico = self.servico_dao.buscar_por_id(id_servico)

            if not cliente:
                return False, "Cliente não encontrado."
            if not profissional:
                return False, "Profissional não encontrado."
            if not servico:
                return False, "Serviço não encontrado."

            if self.agendamento_dao.verificar_conflito(id_profissional, data_hora, servico.duracao, ignorar_id=id_agendamento):
                return False, (
                    f"O profissional já possui um atendimento neste período.\n"
                    f"O serviço '{servico.nome}' dura {servico.duracao} minutos.\n"
                    "Escolha outro horário."
                )

            agendamento.cliente = cliente
            agendamento.profissional = profissional
            agendamento.servico = servico
            agendamento.data_hora = data_hora
            agendamento.estrategia = _string_para_estrategia(estrategia_str)
            agendamento.status = StatusAgendamento(status_str.strip().lower())

            return self.agendamento_dao.atualizar(agendamento)

        except ValueError:
            return False, "Formato de data inválido. Use DD/MM/AAAA HH:MM."
        except Exception as e:
            return False, f"Erro ao atualizar agendamento: {e}"

    def concluir(self, id_agendamento: int):
        try:
            agendamento = self.agendamento_dao.buscar_por_id(id_agendamento)
            if not agendamento:
                return False, "Agendamento não encontrado."
            if agendamento.status != StatusAgendamento.AGENDADO:
                return False, "Só é possível concluir um agendamento com status 'Agendado'."

            return self.agendamento_dao.atualizar_status(id_agendamento, StatusAgendamento.CONCLUIDO)
        except Exception as e:
            return False, f"Erro ao concluir agendamento: {e}"

    def cancelar(self, id_agendamento: int):
        try:
            agendamento = self.agendamento_dao.buscar_por_id(id_agendamento)
            if not agendamento:
                return False, "Agendamento não encontrado."
            if agendamento.status != StatusAgendamento.AGENDADO:
                return False, "Só é possível cancelar um agendamento com status 'Agendado'."

            return self.agendamento_dao.atualizar_status(id_agendamento, StatusAgendamento.CANCELADO)
        except Exception as e:
            return False, f"Erro ao cancelar agendamento: {e}"

    def remover_agendamento(self, id_agendamento: int):
        
        try:
            return self.agendamento_dao.remover(id_agendamento)
        except Exception as e:
            return False, f"Erro ao remover agendamento: {e}"