import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dao.ServicoDAO import ServicoDAO
from model.ServiceFactory import ServiceFactory
from model.ExcecoesPersonalizadas import PrecoInvalidoError


class ServicoController:
    def __init__(self):
        self.servico_dao = ServicoDAO()

    def listar_servicos(self):
        try:
            return self.servico_dao.listar_todos()
        except Exception as e:
            print(f"Erro ao listar serviços: {e}")
            return []

    def buscar_por_id(self, id_servico: int):
        try:
            return self.servico_dao.buscar_por_id(id_servico)
        except Exception as e:
            print(f"Erro ao buscar serviço: {e}")
            return None

    def tipos_disponiveis(self):
        return ServiceFactory.tipos_disponiveis()

    def salvar_servico(self, tipo: str, preco_str: str):
        if not tipo or not preco_str:
            return False, "Todos os campos são obrigatórios."

        try:
            preco = float(preco_str.replace(",", "."))
            if preco <= 0:
                return False, "O preço deve ser um valor positivo."

            existente = self.servico_dao.buscar_por_tipo(tipo.strip().lower())
            if existente:
                return False, f"Já existe um servico do tipo '{tipo}' cadastrado."

            servico = ServiceFactory.criar(tipo=tipo.strip(), preco=preco)
            return self.servico_dao.salvar(servico)

        except ValueError as e:
            return False, f"Preço inválido: {e}"
        except PrecoInvalidoError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro ao salvar serviço: {e}"

    def atualizar_servico(self, id_servico: int, preco_str: str):
        if not preco_str:
            return False, "O preço é obrigatório."

        try:
            preco = float(preco_str.replace(",", "."))
            if preco <= 0:
                return False, "O preço deve ser um valor positivo."

            servico = self.servico_dao.buscar_por_id(id_servico)
            if not servico:
                return False, "Serviço não encontrado para edição."

            servico.preco = preco
            return self.servico_dao.atualizar(servico)

        except ValueError as e:
            return False, f"Preço inválido: {e}"
        except PrecoInvalidoError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Erro ao atualizar serviço: {e}"

    def remover_servico(self, id_servico: int):
        try:
            return self.servico_dao.remover(id_servico)
        except Exception as e:
            return False, f"Erro ao remover serviço: {e}"