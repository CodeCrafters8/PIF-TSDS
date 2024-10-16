
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
                             usuario.cuil, usuario.saldo_inicial, usuario.IdPerfilInversor))
            conexion.commit()
        finally:
            self.db.cerrar_conexion()
            
    def existe_email(self, email: str) -> bool:
        try:
            conexion = self.db.conectar()
            cursor = conexion.cursor()
            cursor.execute("SELECT COUNT(*) FROM Usuario WHERE Email = %s", (email,))
            resultado = cursor.fetchone()
            return resultado[0] > 0  # Retorna True si el email ya existe
        finally:
            self.db.cerrar_conexion()        
    
    #Metodo necesario para el INICIO DE SESION - verifica la Existencia del mismo en la base de datos.
    def obtener_usuario_por_email(self, email: str):
        try:
            conexion = self.db.conectar()
            cursor = conexion.cursor()
            cursor.execute("SELECT ID_Usuario, Nombre, Apellido, Email, Contrasena, Cuil, Saldo_Inicial, IdPerfilInversor FROM Usuario WHERE Email = %s", (email,))
            resultado = cursor.fetchone()
            if resultado:
                return User(*resultado)  # Asegúrate de que esto coincida con la estructura de tu clase User
            return None
        finally:
            self.db.cerrar_conexion()
    
    def actualizar_contrasena(self, id_usuario: int, nueva_contrasena: str):
        try:
            conexion = self.db.conectar()
            cursor = conexion.cursor()
            sql = """UPDATE Usuario SET Contrasena=%s WHERE ID_Usuario=%s"""
            cursor.execute(sql, (nueva_contrasena, id_usuario))
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
                                 usuario.cuil, usuario.saldo_inicial, usuario.IdPerfilInversor, usuario.id_usuario))
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