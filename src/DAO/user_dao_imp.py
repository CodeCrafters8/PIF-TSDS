
from DAO.user_dao import UserDAO
from database.data_base_conection import ConexionDB
from model.user import User

class UserDAOImpl(UserDAO):
    def __init__(self, db: ConexionDB):  # Recibe la conexión a la base de datos
        self.db = db

    def obtener_todos(self):
        try:
            conexion = self.db.conectar()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM Usuario")
            resultados = cursor.fetchall()
            usuarios = [User(*fila) for fila in resultados]
            return usuarios
        finally:
            self.db.cerrar_conexion()

    def insertar_usuario(self, usuario: User):
        try:
            conexion = self.db.conectar()
            cursor = conexion.cursor()
            sql = """INSERT INTO Usuario (Nombre, Apellido, Email, Contrasena, Cuil, Saldo_Inicial, IdPerfilInversor)
                     VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (usuario.nombre, usuario.apellido, usuario.email, usuario.contrasena,
                                 usuario.cuil, usuario.saldo_inicial, usuario.id_perfil_inversor))
            conexion.commit()
        finally:
            self.db.cerrar_conexion()

    def obtener_por_id(self, id_usuario: int):
        try:
            conexion = self.db.conectar()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM Usuario WHERE ID_Usuario = %s", (id_usuario,))
            resultado = cursor.fetchone()
            if resultado:
                return User(*resultado)
            return None
        finally:
            self.db.cerrar_conexion()

    def actualizar_usuario(self, usuario: User):
        try:
            conexion = self.db.conectar()
            cursor = conexion.cursor()
            sql = """UPDATE Usuario SET Nombre=%s, Apellido=%s, Email=%s, Contrasena=%s, Cuil=%s, Saldo_Inicial=%s, IdPerfilInversor=%s 
                     WHERE ID_Usuario=%s"""
            cursor.execute(sql, (usuario.nombre, usuario.apellido, usuario.email, usuario.contrasena,
                                 usuario.cuil, usuario.saldo_inicial, usuario.id_perfil_inversor, usuario.id_usuario))
            conexion.commit()
        finally:
            self.db.cerrar_conexion()

    def eliminar_usuario(self, id_usuario: int):
        try:
            conexion = self.db.conectar()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM Usuario WHERE ID_Usuario = %s", (id_usuario,))
            conexion.commit()
        finally:
            self.db.cerrar_conexion()