from .generic_dao import GenericDAO


class AgendamentoDAO(GenericDAO):
    def buscar_por_cliente(self, cliente_id: int):
        raise NotImplementedError
