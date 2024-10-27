from abc import ABC, abstractmethod
from model.transaccion import Transaccion

class TransaccionDAO(ABC):
    @abstractmethod
    def consultar(self, id: int):
        pass
    
    @abstractmethod
    def consultar_por_inversor(self, inversor_id: int):
        pass
    
    @abstractmethod
    def crear (self, transaccion):
        pass
    
    @abstractmethod
    def actualizar(self, transaccion):
        pass
    
    @abstractmethod
    def eliminar( self, id: int):
        pass
    