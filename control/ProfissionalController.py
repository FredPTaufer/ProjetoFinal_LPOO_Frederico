import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dao.ProfissionalDAO import ProfissionalDAO
from dao.ClienteDAO import ClienteDAO
from model.Profissional import Profissional
from model.ExcecoesPersonalizadas import CpfInvalidoError


class ProfissionalController:
    def __init__(self):
        self.profissional_dao = ProfissionalDAO()
        self.cliente_dao = ClienteDAO()

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

    def salvar_profissional(self, nome: str, cpf: str, especialidade: str):
        if not nome or not cpf or not especialidade:
            return False, "Todos os campos são obrigatórios."

        try:
            cpf_limpo = cpf.strip().replace(".", "").replace("-", "")

            # Verifica duplicidade entre profissionais
            todos_pro = self.profissional_dao.listar_todos()
            if any(p.cpf == cpf_limpo for p in todos_pro):
                return False, "Já existe um profissional cadastrado com este CPF."

            # Verifica se o CPF pertence a um cliente
            if self.cliente_dao.buscar_por_cpf(cpf_limpo):
                return False, "Este CPF já está cadastrado como Cliente."

            profissional = Profissional(
                nome = nome.strip(),
                cpf = cpf_limpo,
                especialidade = especialidade.strip()
            )
            return self.profissional_dao.salvar(profissional)

        except CpfInvalidoError as e:
            return False, str(e)
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro ao salvar profissional: {e}"

    def atualizar_profissional(self, id_profissional: int, nome: str, especialidade: str):
        if not nome or not especialidade:
            return False, "Nome e especialidade são obrigatórios."

        try:
            profissional = self.profissional_dao.buscar_por_id(id_profissional)
            if not profissional:
                return False, "Profissional não encontrado para edição."

            profissional.nome = nome.strip()
            profissional.especialidade = especialidade.strip()

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

    def buscar_por_servico(self, nome_servico: str):
        try:
            todos = self.profissional_dao.listar_todos()
            return [
                p for p in todos
                if nome_servico.strip().lower() in
                [e.strip().lower() for e in p.especialidade.split(",")]
            ]
        except Exception as e:
            print(f"Erro ao buscar profissionais por serviço: {e}")
            return []