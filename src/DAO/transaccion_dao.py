from abc import ABC, abstractmethod

class transaccion_dao(ABC):
    @abstractmethod
    def get(self, id: int):
        pass
    
    @abstractmethod
    def get_by_inversor(self, inversor_id: int):
        pass
    
    @abstractmethod
    def create (self, transaccion):
        pass
    
    @abstractmethod
    def update(self, transaccion):
        pass
    
    @abstractmethod
    def delete( self, id: int):
        pass
    