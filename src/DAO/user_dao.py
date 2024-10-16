from abc import ABC, abstractmethod
from model.user import User

class UserDAO(ABC):
    @abstractmethod
    def obtener_todos(self):
        pass

    @abstractmethod
    def insertar_usuario(self, usuario: User):
        pass

    @abstractmethod
    def obtener_por_id(self, id_usuario: int):
        pass

    @abstractmethod
    def actualizar_usuario(self, usuario: User):
        pass

    @abstractmethod
    def eliminar_usuario(self, id_usuario: int):
        pass