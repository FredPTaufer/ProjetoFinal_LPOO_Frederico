class ClienteController:
    def salvar_cliente(self, dados):
        raise NotImplementedError

    def listar_clientes(self):
        raise NotImplementedError

    def buscar_por_cpf(self, cpf: str):
        raise NotImplementedError
