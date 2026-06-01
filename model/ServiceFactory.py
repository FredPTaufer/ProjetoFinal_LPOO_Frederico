from .CorteMasculino import CorteMasculino
from .CorteFeminino  import CorteFeminino
from .Barba           import Barba
from .PintarCabelo   import PintarCabelo
from .Sobrancelha     import Sobrancelha


class ServiceFactory:
    _tipos = {
        "cortemasculino" : CorteMasculino,
        "cortefeminino"  : CorteFeminino,
        "barba"          : Barba,
        "pintarcabelo"   : PintarCabelo,
        "sobrancelha"    : Sobrancelha,
    }

    @staticmethod
    def criar(tipo: str, preco: float = None, id: int = None):
        chave = tipo.strip().lower().replace(" ", "")
        if chave not in ServiceFactory._tipos:
            raise ValueError(
                f"Tipo de servico invalido: '{tipo}'. "
                f"Opcoes: {list(ServiceFactory._tipos.keys())}"
            )
        classe = ServiceFactory._tipos[chave]
        if preco is not None:
            return classe(preco=preco, id=id)
        return classe(id=id)

    @staticmethod
    def tipos_disponiveis():
        return list(ServiceFactory._tipos.keys())