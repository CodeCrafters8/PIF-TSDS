from abc import ABC, abstractmethod

class user_dao(ABC):
    @abstractmethod
    def get(self, id: int):
        pass
    
    @abstractmethod
    def get_by_email(self, email: str):
        pass
    
    @abstractmethod
    def update(self, user):
        pass
    
    @abstractmethod 
    def delete(self, id: int):
        pass
    
    print("prueba")
    
