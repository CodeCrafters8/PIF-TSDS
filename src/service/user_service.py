import re
from database.data_base_conection import DBConn
from DAO.user_dao_imp import UserDAOImpl
from DAO.perfil_inversor_dao_imp import PerfilInversorDAOImpl
from model.user import User

class UserService:
    def __init__(self, db_conn: DBConn):
        self.db_conn = db_conn  # Conexión a la base de datos
        self.user_dao = UserDAOImpl(self.db_conn)  # Pasar la conexión a UserDAOImpl
        self.perfil_inversor_dao = PerfilInversorDAOImpl(self.db_conn)  # Pasar la conexión a PerfilInversorDAOImpl

    def registrar_inversor(self, cuil, nombre, apellido, email, contraseña, saldo_pesos, tipo_inversor):
        try:
            # Verificar si el email ya existe
            if self.user_dao.existe_email(email):
                print("El email ya está registrado. Intente con otro.")
                return False
            # Obtiene el Id del perfil directamente
            id_perfil_inversor = self.perfil_inversor_dao.obtener_perfil(tipo_inversor)
            
            if id_perfil_inversor is not None:  # Verifica si se encontró el perfil
                # Crea un nuevo usuario
                nuevo_usuario = User(None,  cuil, nombre, apellido, email, contraseña, saldo_pesos, id_perfil_inversor)
                # Inserta el nuevo usuario
                self.user_dao.insertar_usuario(nuevo_usuario)
                print("Registro exitoso.")
                return True
            else:
                print("Tipo de perfil no encontrado.")
                return False
        except Exception as e:
            print(f"Error en el registro: {e}")
            return False

    def iniciar_sesion(self, email, contraseña):
        usuario = self.user_dao.obtener_usuario_por_email(email)
        if usuario and usuario.contraseña == contraseña:  # Comparación de contraseñas
            print("Inicio de sesión exitoso.")
            return usuario.id_inversor  # Devuelve el ID del inversor
        else:
            print("Email o contraseña incorrectos.")
            return None

    def obtener_usuario_por_id(self, id_inversor):
        return self.user_dao.obtener_por_id(id_inversor)
    
    def recuperar_contraseña(self, email):
        usuario = self.user_dao.obtener_usuario_por_email(email)
        if usuario:
            nueva_contraseña = input("Ingrese su nueva contraseña: ")
            self.user_dao.actualizar_contraseña(usuario.id_inversor, nueva_contraseña)
            return True  # Retorna True si se actualizó la contraseña
        else:
            return False 
            
    def obtener_informacion_inversores(self, id_inversor):
        return self.user_dao.obtener_informacion_inversores(id_inversor)  # Pasa el id_inversor aquí

    @staticmethod
    def validar_email(email):
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(regex, email) is not None

    @staticmethod
    def validar_cuil(cuil):
        return len(cuil) == 11 and cuil.isdigit()

    @staticmethod
    def generar_contraseña_temporal():
        import random
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))
