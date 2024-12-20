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
                query_inversor = f"""INSERT INTO {self.db_conn.get_data_base_name()}.inversor
                            (cuil, nombre, apellido, email, contraseña, saldo_pesos, perfil_inversor_id) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(query_inversor, (usuario.cuil, usuario.nombre, usuario.apellido, usuario.email, usuario.contraseña,
                                        usuario.saldo_pesos, usuario.perfil_inversor_id))
                
                id_inversor = cursor.lastrowid
                
                query_portafolio  = f""" INSERT INTO {self.db_conn.get_data_base_name()}.portafolio (total_invertido, id_inversor)
                             VALUES (%s, %s)"""
                
                cursor.execute(query_portafolio, (0.0, id_inversor))
                
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

    def obtener_usuario_por_id(self, id_inversor: int) -> User:
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
            
    def obtener_informacion_inversores(self, id_inversor):
        conn = self.db_conn.connect_to_mysql()
        with conn:
            cursor = conn.cursor()
            query = """
            SELECT 
                i.nombre,
                i.apellido,
                i.email,
                pi.tipo_inversor,
                COALESCE(SUM(p.total_invertido), 0) AS total_invertido,
                i.saldo_pesos
            FROM 
                inversor i
            JOIN 
                perfil_inversor pi ON i.perfil_inversor_id = pi.id_perfil_inversor
            LEFT JOIN 
                portafolio p ON i.id_inversor = p.id_inversor
            WHERE 
                i.id_inversor = %s
            GROUP BY 
                i.id_inversor;
            """
            cursor.execute(query, (id_inversor,))
            resultados = cursor.fetchall()
            return resultados
        
    def existe_usuario(self, email):
        conn = self.db_conn.connect_to_mysql()  # Conectar a la base de datos
        query = "SELECT COUNT(*) FROM inversor WHERE Email = %s"
        cursor = conn.cursor()
        
        try:
            cursor.execute(query, (email,))
            resultado = cursor.fetchone()  # Obtener el resultado de la consulta
            return resultado[0] > 0  # Retorna True si el usuario existe
        finally:
            cursor.close()  # Cerrar el cursor


    def actualizar_saldo(self, user: User, total: float, id_operacion: int):
        """
        Actualiza el saldo del usuario según el tipo de operación.
        
        Parámetros:
            user (User): El usuario cuyo saldo necesita ser actualizado.
            total (float): La cantidad por la que se ajustará el saldo.
            id_operacion (int): El identificador de la operación (1 para compra, 2 para venta).
        """
        conn = self.db_conn.connect_to_mysql()  # Conectar a la base de datos
        try:
            cursor = conn.cursor()
            
            # Determinar si debemos restar o sumar al saldo según id_operacion
            if id_operacion == 2:  # Venta
                nuevo_saldo = user.saldo_pesos + total
            elif id_operacion == 1:  # Compra
                nuevo_saldo = user.saldo_pesos - total
            else:
                raise ValueError("id_operacion no válido. Debe ser 1 (compra) o 2 (venta).")
            
            # Actualizar el saldo del usuario en la base de datos
            query = """
                UPDATE inversor SET saldo_pesos = %s WHERE id_inversor = %s
            """
            cursor.execute(query, (nuevo_saldo, user.id_inversor))
            
            # Confirmar cambios
            conn.commit()
            print("Saldo actualizado correctamente en la tabla usuario.")
            
            # Actualizar el saldo en la instancia del usuario
            user.saldo_pesos = nuevo_saldo
        except Exception as e:
            print(f"Error al actualizar el saldo: {e}")
            conn.rollback()
        finally:
            
            if cursor:          
                cursor.close()
            
