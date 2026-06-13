import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dao.ClienteDAO import ClienteDAO
from dao.ProfissionalDAO import ProfissionalDAO
from model.Cliente import Cliente
from model.ExcecoesPersonalizadas import CpfInvalidoError


class ClienteController:
    def __init__(self):
        self.cliente_dao = ClienteDAO()
        self.profissional_dao = ProfissionalDAO()

    def listar_clientes(self):
        try:
            return self.cliente_dao.listar_todos()
        except Exception as e:
            print(f"Erro ao listar clientes: {e}")
            return []

    def buscar_por_id(self, id_cliente: int):
        try:
            return self.cliente_dao.buscar_por_id(id_cliente)
        except Exception as e:
            print(f"Erro ao buscar cliente: {e}")
            return None

    def buscar_por_cpf(self, cpf: str):
        try:
            return self.cliente_dao.buscar_por_cpf(cpf.strip())
        except Exception as e:
            print(f"Erro ao buscar cliente por CPF: {e}")
            return None

    def salvar_cliente(self, nome: str, cpf: str, telefone: str, email: str):
        if not nome or not cpf or not telefone or not email:
            return False, "Todos os campos são obrigatórios."

        try:
            cpf_limpo = cpf.strip().replace(".", "").replace("-", "")

            # Verifica duplicidade entre clientes
            if self.cliente_dao.buscar_por_cpf(cpf_limpo):
                return False, "Já existe um cliente cadastrado com este CPF."

            # Verifica se o CPF pertence a um profissional
            todos_pro = self.profissional_dao.listar_todos()
            if any(p.cpf == cpf_limpo for p in todos_pro):
                return False, "Este CPF já está cadastrado como Profissional."

            cliente = Cliente(
                nome = nome.strip(),
                cpf = cpf_limpo,
                telefone = telefone.strip(),
                email = email.strip()
            )
            return self.cliente_dao.salvar(cliente)

        except CpfInvalidoError as e:
            return False, str(e)
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro ao salvar cliente: {e}"

    def atualizar_cliente(self, id_cliente: int, nome: str, telefone: str, email: str):
        if not nome or not telefone or not email:
            return False, "Todos os campos são obrigatórios."

        try:
            cliente = self.cliente_dao.buscar_por_id(id_cliente)
            if not cliente:
                return False, "Cliente não encontrado para edição."

            cliente.nome = nome.strip()
            cliente.telefone = telefone.strip()
            cliente.email = email.strip()

            return self.cliente_dao.atualizar(cliente)

        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro ao atualizar cliente: {e}"

    def remover_cliente(self, id_cliente: int):
        try:
            return self.cliente_dao.remover(id_cliente)
        except Exception as e:
            return False, f"Erro ao remover cliente: {e}"