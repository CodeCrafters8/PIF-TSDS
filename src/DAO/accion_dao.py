from abc import ABC, abstractmethod
from model.accion import Accion

class AccionDAO(ABC):
    @abstractmethod
    def agregar_accion(self, accion: Accion) -> None:
        pass

    @abstractmethod
    def obtener_accion(self, id_accion: int) -> Accion:
        pass

    @abstractmethod
    def listar_acciones(self) -> list[Accion]:
        pass

    @abstractmethod
    def actualizar_accion(self, accion: Accion) -> None:
        pass

    @abstractmethod
    def eliminar_accion(self, id_accion: int) -> None:
        pass