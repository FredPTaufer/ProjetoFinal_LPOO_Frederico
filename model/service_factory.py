from .corte_masculino import CorteMasculino
from .corte_feminino import CorteFeminino
from .barba import Barba
from .pintar_cabelo import PintarCabelo
from .sobrancelha import Sobrancelha
from .servico import Service


class ServiceFactory:
    @staticmethod
    def criar(tipo: str) -> Service:
        tipo = tipo.lower()
        if tipo == "corte masculino":
            return CorteMasculino("Corte Masculino", 30, 50.0)
        if tipo == "corte feminino":
            return CorteFeminino("Corte Feminino", 45, 70.0)
        if tipo == "barba":
            return Barba("Barba", 20, 30.0)
        if tipo == "pintar cabelo":
            return PintarCabelo("Pintar Cabelo", 60, 100.0)
        if tipo == "sobrancelha":
            return Sobrancelha("Sobrancelha", 15, 25.0)
        raise ValueError(f"Serviço desconhecido: {tipo}")
