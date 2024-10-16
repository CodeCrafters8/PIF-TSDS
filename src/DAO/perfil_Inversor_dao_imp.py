from DAO.perfil_Inversor_dao import PerfilInversorDAO
from database.data_base_conection import ConexionDB
from model.perfil_Inversor import PerfilInversor

class PerfilInversorDAOImpl(PerfilInversorDAO):
    def __init__(self, db: ConexionDB):
        self.db = db

    def obtener_todos(self):
        conexion = self.db.conectar()
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM PerfilInversor")
            resultados = cursor.fetchall()
            perfiles = [PerfilInversor(*fila) for fila in resultados]
            return perfiles
        finally:
            cursor.close()  # Cerrar cursor
            self.db.cerrar_conexion()

    def insertar_perfil(self, perfil: PerfilInversor):
        conexion = self.db.conectar()
        try:
            cursor = conexion.cursor()
            sql = """INSERT INTO PerfilInversor (nombre, descripcion) VALUES (%s, %s)"""
            cursor.execute(sql, (perfil.nombre, perfil.descripcion))
            conexion.commit()
        finally:
            cursor.close()  # Cerrar cursor
            self.db.cerrar_conexion()

    def obtener_perfil_por_tipo(self, tipo_perfil):
        conexion = self.db.conectar()
        try:
            cursor = conexion.cursor()
            query = "SELECT * FROM PerfilInversor WHERE TipoPerfil = %s"
            cursor.execute(query, (tipo_perfil,))
            resultado = cursor.fetchone()
            return resultado
        finally:
            cursor.close()
            self.db.cerrar_conexion()
        
    def obtener_por_id(self, id_perfil: int):
        conexion = self.db.conectar()
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM PerfilInversor WHERE id = %s", (id_perfil,))
            resultado = cursor.fetchone()
            if resultado:
                return PerfilInversor(*resultado)
            return None
        finally:
            cursor.close()  # Cerrar cursor
            self.db.cerrar_conexion()

    def actualizar_perfil(self, perfil: PerfilInversor):
        conexion = self.db.conectar()
        try:
            cursor = conexion.cursor()
            sql = """UPDATE PerfilInversor SET nombre=%s, descripcion=%s WHERE id=%s"""
            cursor.execute(sql, (perfil.nombre, perfil.descripcion, perfil.id))
            conexion.commit()
        finally:
            cursor.close()  # Cerrar cursor
            self.db.cerrar_conexion()

    def eliminar_perfil(self, id_perfil: int):
        conexion = self.db.conectar()
        try:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM PerfilInversor WHERE id = %s", (id_perfil,))
            conexion.commit()
        finally:
            cursor.close()  # Cerrar cursor
            self.db.cerrar_conexion()