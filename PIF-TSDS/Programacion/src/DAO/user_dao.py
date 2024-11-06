from abc import ABC, abstractmethod
from model.user import User

class UserDAO(ABC):
    @abstractmethod
    def obtener_todos(self) -> list:
        """Obtiene todos los usuarios."""
        pass

    @abstractmethod
    def insertar_usuario(self, usuario: User):
        """Inserta un nuevo usuario en la base de datos."""
        pass

    @abstractmethod
    def existe_email(self, email: str) -> bool:
        """Verifica si un email ya está registrado."""
        pass

    @abstractmethod
    def obtener_usuario_por_email(self, email: str) -> User:
        """Obtiene un usuario a partir de su email."""
        pass

    @abstractmethod
    def actualizar_contraseña(self, id_inversor: int, nueva_contraseña: str):
        """Actualiza la contraseña de un usuario."""
        pass

    @abstractmethod
    def obtener_usuario_por_id(self, id_inversor: int) -> User:
        """Obtiene un usuario por su ID."""
        pass

    @abstractmethod
    def actualizar_usuario(self, usuario: User):
        """Actualiza los datos de un usuario existente."""
        pass

    @abstractmethod
    def eliminar_usuario(self, id_inversor: int):
        """Elimina un usuario de la base de datos."""
        pass

    @abstractmethod
    def obtener_informacion_inversores(self, id_inversor: int):
        """Obtiene información adicional sobre un inversor específico."""
        pass

    @abstractmethod
    def existe_usuario(self, email: str) -> bool:
        """Verifica si un usuario existe en la base de datos."""
        pass

    @abstractmethod
    def actualizar_saldo(self, user: User, total_costo: float):
        """Actualiza el saldo de un usuario."""
        pass
