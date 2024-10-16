from abc import ABC, abstractmethod
from model.perfil_Inversor import PerfilInversor

class PerfilInversorDAO(ABC):
   
    @abstractmethod
    def obtener_perfil(self, tipo_perfil: int):
        pass