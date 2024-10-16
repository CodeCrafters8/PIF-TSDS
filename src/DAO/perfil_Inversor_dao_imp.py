from DAO.perfil_Inversor_dao import PerfilInversorDAO
from database.data_base_conection import ConexionDB
from model.perfil_Inversor import PerfilInversor


class PerfilInversorDAOImpl(PerfilInversorDAO):
    def __init__(self):
        self.db = ConexionDB()

    def obtener_todos(self):
        try:
            conexion = self.db.conectar()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM PerfilInversor")
            resultados = cursor.fetchall()
            perfiles = [PerfilInversor(*fila) for fila in resultados]
            return perfiles
        finally:
            self.db.cerrar_conexion()

    def insertar_perfil(self, perfil: PerfilInversor):
        try:
            conexion = self.db.conectar()
            cursor = conexion.cursor()
            sql = """INSERT INTO PerfilInversor (TipoPerfil) VALUES (%s)"""
            cursor.execute(sql, (perfil.tipo_perfil,))
            conexion.commit()
        finally:
            self.db.cerrar_conexion()

    def obtener_por_id(self, id_perfil: int):
        try:
            conexion = self.db.conectar()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM PerfilInversor WHERE IdPerfilInversor = %s", (id_perfil,))
            resultado = cursor.fetchone()
            if resultado:
                return PerfilInversor(*resultado)
            return None
        finally:
            self.db.cerrar_conexion()