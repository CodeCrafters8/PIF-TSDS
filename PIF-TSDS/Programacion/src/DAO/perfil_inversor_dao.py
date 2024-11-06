from abc import ABC, abstractmethod
from model.perfil_inversor import PerfilInversor


class PerfilInversorDAO(ABC):
    @abstractmethod
    def obtener_perfil(self, tipo_inversor):
        pass    