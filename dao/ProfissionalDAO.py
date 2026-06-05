import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dao.DBConfig import DatabaseConfig
from dao.GenericDAO import GenericDAO
from model.Profissional import Profissional


class ProfissionalDAO(GenericDAO):
    def __init__(self):
        self.conexao = DatabaseConfig.get_connection()

    def salvar(self, profissional: Profissional):
        if not self.conexao:
            return False, "Não foi possível conectar ao banco de dados."
        cursor = None
        try:
            cursor = self.conexao.cursor()
            query = """
                INSERT INTO tb_profissionais
                    (pro_nome, pro_cpf, pro_especialidade, pro_disponivel)
                VALUES (%s, %s, %s, %s)
                RETURNING pro_id
            """
            cursor.execute(query, (
                profissional.nome,
                profissional.cpf,
                profissional.especialidade,
                profissional.disponivel
            ))
            profissional.id = cursor.fetchone()[0]
            self.conexao.commit()
            return True, "Profissional cadastrado com sucesso!"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao cadastrar profissional: {e}"
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
                "SELECT pro_id, pro_nome, pro_cpf, pro_especialidade, pro_disponivel "
                "FROM tb_profissionais ORDER BY pro_nome"
            )
            return [self._montar_profissional(linha) for linha in cursor.fetchall()]
        except Exception as e:
            print(f"Erro ao listar profissionais: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def remover(self, id_profissional: int):
        if not self.conexao:
            return False, "Não foi possível conectar ao banco de dados."
        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute(
                "DELETE FROM tb_profissionais WHERE pro_id = %s",
                (id_profissional,)
            )
            if cursor.rowcount == 0:
                self.conexao.rollback()
                return False, "Profissional não encontrado para remoção."
            self.conexao.commit()
            return True, "Profissional removido com sucesso!"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao remover profissional: {e}"
        finally:
            if cursor:
                cursor.close()

    def atualizar(self, profissional: Profissional):
        if not self.conexao:
            return False, "Não foi possível conectar ao banco de dados."
        cursor = None
        try:
            cursor = self.conexao.cursor()
            query = """
                UPDATE tb_profissionais
                SET pro_nome          = %s,
                    pro_especialidade = %s,
                    pro_disponivel    = %s
                WHERE pro_id = %s
            """
            cursor.execute(query, (
                profissional.nome,
                profissional.especialidade,
                profissional.disponivel,
                profissional.id
            ))
            if cursor.rowcount == 0:
                self.conexao.rollback()
                return False, "Profissional não encontrado para atualização."
            self.conexao.commit()
            return True, "Profissional atualizado com sucesso!"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao atualizar profissional: {e}"
        finally:
            if cursor:
                cursor.close()

    def buscar_por_id(self, id_profissional: int):
        if not self.conexao:
            return None
        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute(
                "SELECT pro_id, pro_nome, pro_cpf, pro_especialidade, pro_disponivel "
                "FROM tb_profissionais WHERE pro_id = %s",
                (id_profissional,)
            )
            linha = cursor.fetchone()
            return self._montar_profissional(linha) if linha else None
        except Exception as e:
            print(f"Erro ao buscar profissional: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def buscar_por_tipo(self, especialidade: str):
        if not self.conexao:
            return []
        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute(
                "SELECT pro_id, pro_nome, pro_cpf, pro_especialidade, pro_disponivel "
                "FROM tb_profissionais "
                "WHERE LOWER(pro_especialidade) = LOWER(%s) "
                "ORDER BY pro_nome",
                (especialidade.strip(),)
            )
            return [self._montar_profissional(linha) for linha in cursor.fetchall()]
        except Exception as e:
            print(f"Erro ao buscar profissional por especialidade: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def _montar_profissional(self, linha):
        pro_id, nome, cpf, especialidade, disponivel = linha
        p = Profissional(nome=nome, cpf=cpf, especialidade=especialidade, id=pro_id)
        p.disponivel = disponivel
        return p