import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dao.DBConfig import DatabaseConfig
from dao.GenericDAO import GenericDAO
from model.Cliente import Cliente


class ClienteDAO(GenericDAO):
    def __init__(self):
        self.conexao = DatabaseConfig.get_connection()

    def salvar(self, cliente: Cliente):
        if not self.conexao:
            return False, "Não foi possível conectar ao banco de dados."
        cursor = None
        try:
            cursor = self.conexao.cursor()
            query = """
                INSERT INTO tb_clientes (cli_nome, cli_cpf, cli_telefone, cli_email)
                VALUES (%s, %s, %s, %s)
                RETURNING cli_id
            """
            cursor.execute(query, (
                cliente.nome,
                cliente.cpf,
                cliente.telefone,
                cliente.email
            ))
            cliente.id = cursor.fetchone()[0]
            self.conexao.commit()
            return True, "Cliente cadastrado com sucesso!"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao cadastrar cliente: {e}"
        finally:
            if cursor:
                cursor.close()

    def listar_todos(self):
        if not self.conexao:
            return []
        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute(
                "SELECT cli_id, cli_nome, cli_cpf, cli_telefone, cli_email "
                "FROM tb_clientes ORDER BY cli_nome"
            )
            return [self._montar_cliente(linha) for linha in cursor.fetchall()]
        except Exception as e:
            print(f"Erro ao listar clientes: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def remover(self, id_cliente: int):
        if not self.conexao:
            return False, "Não foi possível conectar ao banco de dados."
        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute(
                "DELETE FROM tb_clientes WHERE cli_id = %s", (id_cliente,)
            )
            if cursor.rowcount == 0:
                self.conexao.rollback()
                return False, "Cliente não encontrado para remoção."
            self.conexao.commit()
            return True, "Cliente removido com sucesso!"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao remover cliente: {e}"
        finally:
            if cursor:
                cursor.close()

    def atualizar(self, cliente: Cliente):
        if not self.conexao:
            return False, "Não foi possível conectar ao banco de dados."
        cursor = None
        try:
            cursor = self.conexao.cursor()
            query = """
                UPDATE tb_clientes
                SET cli_nome     = %s,
                    cli_telefone = %s,
                    cli_email    = %s
                WHERE cli_id = %s
            """
            cursor.execute(query, (
                cliente.nome,
                cliente.telefone,
                cliente.email,
                cliente.id
            ))
            if cursor.rowcount == 0:
                self.conexao.rollback()
                return False, "Cliente não encontrado para atualização."
            self.conexao.commit()
            return True, "Cliente atualizado com sucesso!"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao atualizar cliente: {e}"
        finally:
            if cursor:
                cursor.close()

    def buscar_por_id(self, id_cliente: int):
        if not self.conexao:
            return None
        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute(
                "SELECT cli_id, cli_nome, cli_cpf, cli_telefone, cli_email "
                "FROM tb_clientes WHERE cli_id = %s",
                (id_cliente,)
            )
            linha = cursor.fetchone()
            return self._montar_cliente(linha) if linha else None
        except Exception as e:
            print(f"Erro ao buscar cliente: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def buscar_por_cpf(self, cpf: str):
        if not self.conexao:
            return None
        cursor = None
        try:
            cursor = self.conexao.cursor()
            cpf_limpo = cpf.strip().replace(".", "").replace("-", "")
            cursor.execute(
                "SELECT cli_id, cli_nome, cli_cpf, cli_telefone, cli_email "
                "FROM tb_clientes WHERE cli_cpf = %s",
                (cpf_limpo,)
            )
            linha = cursor.fetchone()
            return self._montar_cliente(linha) if linha else None
        except Exception as e:
            print(f"Erro ao buscar cliente por CPF: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def _montar_cliente(self, linha):
        cli_id, nome, cpf, telefone, email = linha
        return Cliente(nome=nome, cpf=cpf, telefone=telefone, email=email, id=cli_id)