from typing import Any, List


class GenericDAO:
    def salvar(self, obj: Any) -> None:
        raise NotImplementedError

    def listar_todos(self) -> List[Any]:
        raise NotImplementedError

    def remover(self, obj: Any) -> None:
        raise NotImplementedError

    def atualizar(self, obj: Any) -> None:
        raise NotImplementedError
