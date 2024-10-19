import mysql.connector
from DAO.user_dao import UserDAO
from database.data_base_conection import DBConn
from model.user import User

class UserDAOImpl(UserDAO):
    def __init__(self, db_conn: DBConn):  # Recibe la instancia de DBConn
        self.db_conn = db_conn  # Almacena la instancia de DBConn
        self.db_name = db_conn.get_data_base_name()

    def obtener_todos(self) -> list:
        conn = self.db_conn.connect_to_mysql()  # Obtiene la conexión
        with conn:  # Usa la conexión en un contexto
            try:
                cursor = conn.cursor()
                query = f"SELECT * FROM {self.db_conn.get_data_base_name()}.inversor"
                cursor.execute(query)
                resultados = cursor.fetchall()
                usuarios = [User(*fila) for fila in resultados]  # Crea objetos User
                return usuarios
            except mysql.connector.Error as err:
                raise err

    def insertar_usuario(self, usuario: User):
        conn = self.db_conn.connect_to_mysql()  # Obtiene la conexión
        with conn:  # Usa la conexión en un contexto
            try:
                cursor = conn.cursor()
                query = f"""INSERT INTO {self.db_conn.get_data_base_name()}.inversor
                            (cuil, nombre, apellido, email, contraseña, saldo_pesos, perfil_inversor_id) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(query, (usuario.cuil, usuario.nombre, usuario.apellido, usuario.email, usuario.contraseña,
                                        usuario.saldo_pesos, usuario.perfil_inversor_id))
                conn.commit()  # Confirma los cambios
            except mysql.connector.Error as err:
                raise err
            
    def existe_email(self, email: str) -> bool:
        conn = self.db_conn.connect_to_mysql()  # Obtiene la conexión
        with conn:  # Usa la conexión en un contexto
            try:
                cursor = conn.cursor()
                query = f"SELECT COUNT(*) FROM {self.db_conn.get_data_base_name()}.inversor WHERE email = %s"
                cursor.execute(query, (email,))
                resultado = cursor.fetchone()
                return resultado[0] > 0  # Retorna True si el email ya existe
            except mysql.connector.Error as err:
                raise err

    def obtener_usuario_por_email(self, email: str) -> User:
       conn = self.db_conn.connect_to_mysql()  # Obtiene la conexión
       with conn:  # Usa la conexión en un contexto
           try:
               cursor = conn.cursor()
               query = f"SELECT id_inversor, cuil, nombre, apellido, email, contraseña, saldo_pesos, perfil_inversor_id FROM {self.db_name}.inversor WHERE email = %s"
               cursor.execute(query, (email,))
               resultado = cursor.fetchone()
               if resultado:
                   return User(*resultado)  # Crea un objeto User
               return None  # Retorna None si no se encontró
           except mysql.connector.Error as err:
            raise err
    
    def actualizar_contraseña(self, id_inversor: int, nueva_contraseña: str):
        conn = self.db_conn.connect_to_mysql()  # Obtiene la conexión
        with conn:  # Usa la conexión en un contexto
            try:
                cursor = conn.cursor()
                query = f"UPDATE {self.db_conn.get_data_base_name()}.inversor SET contraseña =%s WHERE id_inversor =%s"
                cursor.execute(query, (nueva_contraseña, id_inversor))
                conn.commit()  # Confirma los cambios
            except mysql.connector.Error as err:
                raise err

    def actualizar_usuario(self, usuario: User):
        conn = self.db_conn.connect_to_mysql()  # Obtiene la conexión
        with conn:  # Usa la conexión en un contexto
            try:
                cursor = conn.cursor()
                query = f"""UPDATE {self.db_conn.get_data_base_name()}.inversor
                             SET cuil=%s, nombre=%s, apellido=%s, email=%s,  saldo_pesos=%s, perfil_inversor_id=%s 
                             WHERE ID_Usuario=%s"""
                cursor.execute(query, (usuario.cuil,usuario.nombre, usuario.apellido, usuario.email,  
                                       usuario.saldo_pesos, usuario.perfil_inversor_id, usuario.id_inversor))
                conn.commit()  # Confirma los cambios
            except mysql.connector.Error as err:
                raise err

    def eliminar_usuario(self, id_inversor: int):
        conn = self.db_conn.connect_to_mysql()  # Obtiene la conexión
        with conn:  # Usa la conexión en un contexto
            try:
                cursor = conn.cursor()
                query = f"DELETE FROM {self.db_conn.get_data_base_name()}.inversor WHERE id_inversor=%s"
                cursor.execute(query, (id_inversor,))
                conn.commit()  # Confirma los cambios
            except mysql.connector.Error as err:
                raise err

    def obtener_por_id(self, id_inversor: int) -> User:
        conn = self.db_conn.connect_to_mysql()  # Obtiene la conexión
        with conn:  # Usa la conexión en un contexto
            try:
                cursor = conn.cursor()
                query = f"SELECT id_inversor, cuil, nombre, apellido, email, contraseña, saldo_pesos, perfil_inversor_id FROM {self.db_conn.get_data_base_name()}.inversor WHERE id_inversor = %s"
                cursor.execute(query, (id_inversor,))
                resultado = cursor.fetchone()
                if resultado:
                    return User(*resultado)  # Crea un objeto User
                return None  # Retorna None si no se encontró
            except mysql.connector.Error as err:
                raise err