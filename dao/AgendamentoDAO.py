import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime
from dao.DBConfig import DatabaseConfig
from dao.GenericDAO import GenericDAO
from dao.ClienteDAO import ClienteDAO
from dao.ProfissionalDAO import ProfissionalDAO
from dao.ServicoDAO import ServicoDAO
from model.Agendamento import Agendamento
from model.StatusAgendamento import StatusAgendamento
from model.PrecoNormal import PrecoNormal
from model.PrecoPromocional import PrecoPromocional
from model.PrecoFidelidade import PrecoFidelidade


def _estrategia_para_string(estrategia) -> str:
    nome = type(estrategia).__name__.lower()
    if "promocional" in nome:
        return "promocional"
    if "fidelidade" in nome:
        return "fidelidade"
    return "normal"


def _string_para_estrategia(valor: str):
    if valor == "promocional":
        return PrecoPromocional()
    if valor == "fidelidade":
        return PrecoFidelidade()
    return PrecoNormal()


class AgendamentoDAO(GenericDAO):

    def __init__(self):
        self.conexao  = DatabaseConfig.get_connection()
        self._cli_dao = ClienteDAO()
        self._pro_dao = ProfissionalDAO()
        self._ser_dao = ServicoDAO()

    def salvar(self, agendamento: Agendamento):
        # Valida se os objetos relacionados estão salvos no banco
        if not agendamento.cliente.id:
            return False, "Cliente nao esta cadastrado no banco."
        if not agendamento.profissional.id:
            return False, "Profissional nao esta cadastrado no banco."
        if not agendamento.servico.id:
            return False, "Servico nao esta cadastrado no banco."

        if not self.conexao:
            return False, "Nao foi possivel conectar ao banco de dados."
        cursor = None
        try:
            cursor = self.conexao.cursor()
            query = """
                INSERT INTO tb_agendamentos
                    (age_cli_id, age_pro_id, age_ser_id,
                     age_data_hora, age_status, age_estrategia)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING age_id
            """
            cursor.execute(query, (
                agendamento.cliente.id,
                agendamento.profissional.id,
                agendamento.servico.id,
                agendamento.data_hora,
                agendamento.status.value,
                _estrategia_para_string(agendamento.estrategia)
            ))
            agendamento.id = cursor.fetchone()[0]
            self.conexao.commit()
            return True, "Agendamento cadastrado com sucesso!"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao cadastrar agendamento: {e}"
        finally:
            if cursor:
                cursor.close()

    def listar_todos(self):
        if not self.conexao:
            return []
        cursor = None
        try:
            cursor = self.conexao.cursor()
            query = """
                SELECT age_id, age_cli_id, age_pro_id, age_ser_id,
                       age_data_hora, age_status, age_estrategia
                FROM tb_agendamentos
                ORDER BY
                    CASE age_status
                        WHEN 'agendado'  THEN 1
                        WHEN 'concluido' THEN 2
                        WHEN 'cancelado' THEN 3
                    END,
                    age_data_hora ASC
            """
            cursor.execute(query)
            resultado = [
                a for a in (self._montar_agendamento(l) for l in cursor.fetchall()) if a
            ]
            return resultado
        except Exception as e:
            print(f"Erro ao listar agendamentos: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def remover(self, id_agendamento: int):
        if not self.conexao:
            return False, "Nao foi possivel conectar ao banco de dados."
        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute(
                "DELETE FROM tb_agendamentos WHERE age_id = %s",
                (id_agendamento,)
            )
            if cursor.rowcount == 0:
                self.conexao.rollback()
                return False, "Agendamento nao encontrado para remocao."
            self.conexao.commit()
            return True, "Agendamento removido com sucesso!"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao remover agendamento: {e}"
        finally:
            if cursor:
                cursor.close()

    def atualizar(self, agendamento: Agendamento):
        if not agendamento.cliente.id:
            return False, "Cliente nao esta cadastrado no banco."
        if not agendamento.profissional.id:
            return False, "Profissional nao esta cadastrado no banco."
        if not agendamento.servico.id:
            return False, "Servico nao esta cadastrado no banco."

        if not self.conexao:
            return False, "Nao foi possivel conectar ao banco de dados."
        cursor = None
        try:
            cursor = self.conexao.cursor()
            query = """
                UPDATE tb_agendamentos
                SET age_cli_id     = %s,
                    age_pro_id     = %s,
                    age_ser_id     = %s,
                    age_data_hora  = %s,
                    age_status     = %s,
                    age_estrategia = %s
                WHERE age_id = %s
            """
            cursor.execute(query, (
                agendamento.cliente.id,
                agendamento.profissional.id,
                agendamento.servico.id,
                agendamento.data_hora,
                agendamento.status.value,
                _estrategia_para_string(agendamento.estrategia),
                agendamento.id
            ))
            if cursor.rowcount == 0:
                self.conexao.rollback()
                return False, "Agendamento nao encontrado para atualizacao."
            self.conexao.commit()
            return True, "Agendamento atualizado com sucesso!"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao atualizar agendamento: {e}"
        finally:
            if cursor:
                cursor.close()

    def buscar_por_id(self, id_agendamento: int):
        if not self.conexao:
            return None
        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute(
                """
                SELECT age_id, age_cli_id, age_pro_id, age_ser_id,
                       age_data_hora, age_status, age_estrategia
                FROM tb_agendamentos WHERE age_id = %s
                """,
                (id_agendamento,)
            )
            linha = cursor.fetchone()
            return self._montar_agendamento(linha) if linha else None
        except Exception as e:
            print(f"Erro ao buscar agendamento: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def buscar_por_cliente(self, id_cliente: int):
        if not self.conexao:
            return []
        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute(
                """
                SELECT age_id, age_cli_id, age_pro_id, age_ser_id,
                       age_data_hora, age_status, age_estrategia
                FROM tb_agendamentos
                WHERE age_cli_id = %s
                ORDER BY age_data_hora DESC
                """,
                (id_cliente,)
            )
            return [
                a for a in (self._montar_agendamento(l) for l in cursor.fetchall()) if a
            ]
        except Exception as e:
            print(f"Erro ao buscar agendamentos por cliente: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def atualizar_status(self, id_agendamento: int, novo_status: StatusAgendamento):
        if not self.conexao:
            return False, "Nao foi possivel conectar ao banco de dados."
        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute(
                "UPDATE tb_agendamentos SET age_status = %s WHERE age_id = %s",
                (novo_status.value, id_agendamento)
            )
            if cursor.rowcount == 0:
                self.conexao.rollback()
                return False, "Agendamento nao encontrado."
            self.conexao.commit()
            return True, "Status atualizado com sucesso!"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao atualizar status: {e}"
        finally:
            if cursor:
                cursor.close()

    def _montar_agendamento(self, linha):
        age_id, cli_id, pro_id, ser_id, data_hora, status_str, estrategia_str = linha

        cliente      = self._cli_dao.buscar_por_id(cli_id)
        profissional = self._pro_dao.buscar_por_id(pro_id)
        servico      = self._ser_dao.buscar_por_id(ser_id)

        # Se algum relacionamento foi removido do banco, ignora o agendamento
        if not cliente or not profissional or not servico:
            print(f"Aviso: agendamento #{age_id} com referencia invalida — ignorado.")
            return None

        estrategia = _string_para_estrategia(estrategia_str)
        status     = StatusAgendamento(status_str)

        if isinstance(data_hora, str):
            data_hora = datetime.fromisoformat(data_hora)

        return Agendamento(
            cliente      = cliente,
            profissional = profissional,
            servico      = servico,
            data_hora    = data_hora,
            estrategia   = estrategia,
            status       = status,
            id           = age_id
        )
        
    def verificar_conflito(self, id_profissional: int, data_hora: datetime, ignorar_id: int = None) -> bool:
        """
        Retorna True se já existe agendamento ativo para o mesmo
        profissional no mesmo horário.
        """
        if not self.conexao:
            return False
        cursor = None
        try:
            cursor = self.conexao.cursor()
            query = """
                SELECT 1 FROM tb_agendamentos
                WHERE age_pro_id   = %s
                AND   age_data_hora = %s
                AND   age_status   != 'cancelado'
            """
            params = [id_profissional, data_hora]

            if ignorar_id:
                query += " AND age_id != %s"
                params.append(ignorar_id)

            cursor.execute(query, tuple(params))
            return cursor.fetchone() is not None
        except Exception as e:
            print(f"Erro ao verificar conflito: {e}")
            return False
        finally:
            if cursor:
                cursor.close()