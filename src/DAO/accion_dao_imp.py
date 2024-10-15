# dao/accion_dao_imp.py
import mysql.connector
from DAO.accion_dao import AccionDAO
from model.accion import Accion

class AccionDAOImpl(AccionDAO):
    def __init__(self, connection_params):
        self.connection_params = connection_params

    def _conectar(self):
        return mysql.connector.connect(**self.connection_params)

    def agregar_accion(self, accion: Accion) -> None:
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Accion (Simbolo, Id_Empresa) VALUES (%s, %s)",
                (accion.simbolo, accion.id_empresa)
            )
            conn.commit()

    def obtener_accion(self, id_accion: int) -> Accion:
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ID_Accion, Simbolo, Id_Empresa FROM Accion WHERE ID_Accion = %s", (id_accion,))
            result = cursor.fetchone()
            return Accion(*result) if result else None

    def listar_acciones(self) -> list[Accion]:
        acciones = []
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ID_Accion, Simbolo, Id_Empresa FROM Accion")
            for row in cursor.fetchall():
                acciones.append(Accion(*row))
        return acciones

    def actualizar_accion(self, accion: Accion) -> None:
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Accion SET Simbolo = %s, Id_Empresa = %s WHERE ID_Accion = %s",
                (accion.simbolo, accion.id_empresa, accion.id_accion)
            )
            conn.commit()

    def eliminar_accion(self, id_accion: int) -> None:
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Accion WHERE ID_Accion = %s", (id_accion,))
            conn.commit()
