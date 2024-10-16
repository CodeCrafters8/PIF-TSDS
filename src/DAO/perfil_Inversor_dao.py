from abc import ABC, abstractmethod
from model.perfil_Inversor import PerfilInversor

class PerfilInversorDAO(ABC):
    @abstractmethod
    def obtener_todos(self):
        pass

    @abstractmethod
    def insertar_perfil(self, perfil: PerfilInversor):
        pass

    @abstractmethod
    def obtener_por_id(self, id_perfil: int):
        pass