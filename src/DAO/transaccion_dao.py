from abc import ABC, abstractmethod

class Transaccion_dao(ABC):
    @abstractmethod
    def get(self, id_operacion: int):
        pass
    
    @abstractmethod
    def get_by_inversor(self, user_id: int):
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

    @abstractmethod
    def get_stock_quantity_in_portfolio(self, inversor_id, accion_id):
        pass
