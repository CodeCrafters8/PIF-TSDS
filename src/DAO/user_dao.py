from abc import ABC, abstractmethod
from model.user import User

class UserDAO(ABC):
    @abstractmethod
    def obtener_todos(self) -> list:
        pass

    @abstractmethod
    def insertar_usuario(self, usuario: User):
        pass

    @abstractmethod
    def existe_email(self, email: str) -> bool:
        pass

    @abstractmethod
    def obtener_usuario_por_email(self, email: str) -> User:
        pass

    @abstractmethod
    def actualizar_contraseña(self, id_inversor: int, nueva_contraseña: str):
        pass

    @abstractmethod
    def obtener_por_id(self, id_inversor: int) -> User:
        pass

    @abstractmethod
    def actualizar_usuario(self, usuario: User):
        pass

    @abstractmethod
    def eliminar_usuario(self, id_inversor: int):
        pass