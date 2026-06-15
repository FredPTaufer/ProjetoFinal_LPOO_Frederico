import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dao.DBConfig import DatabaseConfig
from dao.GenericDAO import GenericDAO
from model.ServiceFactory import ServiceFactory


class ServicoDAO(GenericDAO):
    def __init__(self):
        pass

    def salvar(self, servico):
        conexao = DatabaseConfig.get_connection()
        if not conexao:
            return False, "Não foi possível conectar ao banco de dados."
        cursor = None
        try:
            cursor = conexao.cursor()
            query = """
                INSERT INTO tb_servicos (ser_nome, ser_tipo, ser_duracao, ser_preco)
                VALUES (%s, %s, %s, %s)
                RETURNING ser_id
            """
            cursor.execute(query, (
                servico.nome,
                type(servico).__name__.lower(),
                servico.duracao,
                servico.preco
            ))
            servico.id = cursor.fetchone()[0]
            conexao.commit()
            return True, "Serviço cadastrado com sucesso!"
        except Exception as e:
            conexao.rollback()
            return False, f"Erro ao cadastrar serviço: {e}"
        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()

    def listar_todos(self):
        conexao = DatabaseConfig.get_connection()
        if not conexao:
            return []
        cursor = None
        try:
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT ser_id, ser_tipo, ser_preco "
                "FROM tb_servicos ORDER BY ser_tipo"
            )
            return [self._montar_servico(linha) for linha in cursor.fetchall()]
        except Exception as e:
            print(f"Erro ao listar serviços: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()

    def remover(self, id_servico: int):
        conexao = DatabaseConfig.get_connection()
        if not conexao:
            return False, "Não foi possível conectar ao banco de dados."
        cursor = None
        try:
            cursor = conexao.cursor()
            cursor.execute(
                "DELETE FROM tb_servicos WHERE ser_id = %s", (id_servico,)
            )
            if cursor.rowcount == 0:
                conexao.rollback()
                return False, "Serviço não encontrado para remoção."
            conexao.commit()
            return True, "Serviço removido com sucesso!"
        except Exception as e:
            conexao.rollback()
            return False, f"Erro ao remover serviço: {e}"
        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()

    def atualizar(self, servico):
        conexao = DatabaseConfig.get_connection()
        if not conexao:
            return False, "Não foi possível conectar ao banco de dados."
        cursor = None
        try:
            cursor = conexao.cursor()
            query = """
                UPDATE tb_servicos
                SET ser_preco = %s
                WHERE ser_id = %s
            """
            cursor.execute(query, (servico.preco, servico.id))
            if cursor.rowcount == 0:
                conexao.rollback()
                return False, "Serviço não encontrado para atualização."
            conexao.commit()
            return True, "Serviço atualizado com sucesso!"
        except Exception as e:
            conexao.rollback()
            return False, f"Erro ao atualizar serviço: {e}"
        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()

    def buscar_por_id(self, id_servico: int):
        conexao = DatabaseConfig.get_connection()
        if not conexao:
            return None
        cursor = None
        try:
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT ser_id, ser_tipo, ser_preco FROM tb_servicos WHERE ser_id = %s",
                (id_servico,)
            )
            linha = cursor.fetchone()
            return self._montar_servico(linha) if linha else None
        except Exception as e:
            print(f"Erro ao buscar serviço: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()

    def buscar_por_tipo(self, tipo: str):
        conexao = DatabaseConfig.get_connection()
        if not conexao:
            return None
        cursor = None
        try:
            cursor = conexao.cursor()
            cursor.execute(
                "SELECT ser_id, ser_tipo, ser_preco "
                "FROM tb_servicos WHERE ser_tipo = %s",
                (tipo.strip().lower(),)
            )
            linha = cursor.fetchone()
            return self._montar_servico(linha) if linha else None
        except Exception as e:
            print(f"Erro ao buscar serviço por tipo: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()

    def _montar_servico(self, linha):
        ser_id, tipo, preco = linha
        return ServiceFactory.criar(tipo=tipo, preco=float(preco), id=ser_id)