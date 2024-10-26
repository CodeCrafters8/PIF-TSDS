import mysql.connector
from DAO.accion_dao import AccionDAO
from model.accion import Accion
from database.data_base_conection import DBConn

class AccionDAOImpl(AccionDAO):
    def __init__(self, db_conn: DBConn):
        self.db_conn = db_conn

    def _conectar(self):
        conn = self.db_conn.connect_to_mysql()
        if conn is None:
            raise Exception("No se pudo establecer la conexión a la base de datos.")
        return conn

    def agregar_accion(self, accion: Accion) -> None:
        conn = self._conectar()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO acciones (id_accion, ticker, nombre, empresa_id) VALUES (%s, %s, %s, %s)",
                (accion.id_accion, accion.ticker, accion.nombre, accion.empresa_id)
            )
            conn.commit()
            print("Acción agregada exitosamente.")
        except Exception as e:
            print(f"Error al agregar acción: {e}")
        finally:
            cursor.close()  # Cierra el cursor

    def obtener_accion_por_id(self, accion_id):
        conn = self._conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT ID_Accion, ticker, nombre, empresa_id FROM Acciones WHERE ID_Accion = %s", (accion_id,))
            row = cursor.fetchone()
            if row:
                return Accion(*row)  # Crea un objeto Accion con los datos de la base de datos
        except Exception as e:
            print(f"Error al obtener la acción: {e}")
        finally:
            cursor.close()
        return None

    def listar_acciones(self) -> list[Accion]:
        acciones = []
        conn = self._conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT ID_Accion, ticker, nombre, empresa_id FROM Acciones")
            for row in cursor.fetchall():
                acciones.append(Accion(*row))
        except Exception as e:
            print(f"Error al listar acciones: {e}")
        finally:
            cursor.close()  # Cierra el cursor
        return acciones

    def actualizar_accion(self, accion: Accion) -> None:
        conn = self._conectar()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE Acciones SET ticker = %s, nombre = %s, empresa_id = %s WHERE ID_Accion = %s",
                (accion.ticker, accion.nombre, accion.empresa_id, accion.id_accion)
            )
            conn.commit()
            print("Acción actualizada exitosamente.")
        except Exception as e:
            print(f"Error al actualizar acción: {e}")
        finally:
            cursor.close()  # Cierra el cursor

    def eliminar_accion(self, id_accion: int) -> None:
        conn = self._conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Acciones WHERE ID_Accion = %s", (id_accion,))
            conn.commit()
            print("Acción eliminada exitosamente.")
        except Exception as e:
            print(f"Error al eliminar acción: {e}")
        finally:
            cursor.close()  # Cierra el cursor
