from abc import ABC, abstractmethod

class stock_dao(ABC):
    @abstractmethod
    def get(self, id: int):
        pass
    
    @abstractmethod
    def get_by_inversor(self, inversor_id: int):
        pass
    
    @abstractmethod
    def create(self, activo):
        pass
    
    @abstractmethod
    def update(self, activo):
        pass
    
    @abstractmethod
    def delete(self, id: int):
        pass
    