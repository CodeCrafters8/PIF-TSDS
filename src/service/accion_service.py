# service/accion_service.py
from DAO.accion_dao_imp import AccionDAOImpl
from model.accion import Accion

class AccionService:
    def __init__(self, accion_dao: AccionDAOImpl):
        self.accion_dao = accion_dao

    def crear_accion(self, simbolo: str, id_empresa: int) -> None:
        nueva_accion = Accion(id_accion=None, simbolo=simbolo, id_empresa=id_empresa)
        self.accion_dao.agregar_accion(nueva_accion)

    def obtener_accion(self, id_accion: int) -> Accion:
        return self.accion_dao.obtener_accion(id_accion)

    def listar_acciones(self) -> list[Accion]:
        return self.accion_dao.listar_acciones()

    def actualizar_accion(self, accion: Accion) -> None:
        self.accion_dao.actualizar_accion(accion)

    def eliminar_accion(self, id_accion: int) -> None:
        self.accion_dao.eliminar_accion(id_accion)
