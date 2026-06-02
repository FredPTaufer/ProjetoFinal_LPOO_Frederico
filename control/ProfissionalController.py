import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dao.ProfissionalDAO import ProfissionalDAO
from model.Profissional import Profissional
from model.ExcecoesPersonalizadas import CpfInvalidoError


class ProfissionalController:

    def __init__(self):
        self.profissional_dao = ProfissionalDAO()

    def listar_profissionais(self):
        try:
            return self.profissional_dao.listar_todos()
        except Exception as e:
            print(f"Erro ao listar profissionais: {e}")
            return []

    def buscar_por_id(self, id_profissional: int):
        try:
            return self.profissional_dao.buscar_por_id(id_profissional)
        except Exception as e:
            print(f"Erro ao buscar profissional: {e}")
            return None

    def buscar_disponiveis(self):
        try:
            todos = self.profissional_dao.listar_todos()
            return [p for p in todos if p.disponivel]
        except Exception as e:
            print(f"Erro ao buscar profissionais disponiveis: {e}")
            return []

    def salvar_profissional(self, nome: str, cpf: str, especialidade: str):
        if not nome or not cpf or not especialidade:
            return False, "Todos os campos sao obrigatorios."

        try:
            existente = self.profissional_dao.buscar_por_tipo(especialidade)
            # Verifica duplicidade de CPF manualmente
            todos = self.profissional_dao.listar_todos()
            cpf_limpo = cpf.strip().replace(".", "").replace("-", "")
            if any(p.cpf == cpf_limpo for p in todos):
                return False, "Ja existe um profissional cadastrado com este CPF."

            profissional = Profissional(
                nome          = nome.strip(),
                cpf           = cpf.strip(),
                especialidade = especialidade.strip()
            )
            return self.profissional_dao.salvar(profissional)

        except CpfInvalidoError as e:
            return False, str(e)
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro ao salvar profissional: {e}"

    def atualizar_profissional(self, id_profissional: int, nome: str,
                               especialidade: str, disponivel: bool):
        if not nome or not especialidade:
            return False, "Nome e especialidade sao obrigatorios."

        try:
            profissional = self.profissional_dao.buscar_por_id(id_profissional)
            if not profissional:
                return False, "Profissional nao encontrado para edicao."

            profissional.nome          = nome.strip()
            profissional.especialidade = especialidade.strip()
            profissional.disponivel    = disponivel

            return self.profissional_dao.atualizar(profissional)

        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro ao atualizar profissional: {e}"

    def remover_profissional(self, id_profissional: int):
        try:
            return self.profissional_dao.remover(id_profissional)
        except Exception as e:
            return False, f"Erro ao remover profissional: {e}"