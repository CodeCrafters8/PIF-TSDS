import re
from database.data_base_conection import ConexionDB
from DAO.user_dao_imp import UserDAOImpl
from DAO.perfil_Inversor_dao_imp import PerfilInversorDAOImpl
from model.user import User  # Asegúrate de importar la clase User

class UserService:
    def __init__(self):
        self.db = ConexionDB()  # Conexión a la base de datos
        self.user_dao = UserDAOImpl(self.db)  # Pasar la conexión a UserDAOImpl
        self.perfil_inversor_dao = PerfilInversorDAOImpl(self.db)  # Pasar la conexión a PerfilInversorDAOImpl
        

    def registrar_inversor(self, nombre, apellido, cuil, email, contrasena, saldo_inicial, tipo_perfil):
        try:
            # Verificar si el email ya existe
            if self.user_dao.existe_email(email):
                print("El email ya está registrado. Intente con otro.")
                return False  # O lanzar una excepción según tu preferencia
            
            # Obtiene el Id del perfil directamente
            IdPerfilInversor = self.perfil_inversor_dao.obtener_perfil(tipo_perfil)
            
            if IdPerfilInversor is not None:  # Verifica si se encontró el perfil
                # Asegúrate de que saldo_inicial sea de tipo Decimal
                nuevo_usuario = User(None, nombre, apellido, email, contrasena, cuil, saldo_inicial, IdPerfilInversor)
                self.user_dao.insertar_usuario(nuevo_usuario)
                print("Registro exitoso.")
                return True
            else:
                print("Tipo de perfil no encontrado.")
                return False
        except Exception as e:
            print(f"Error en el registro: {e}")
            return False
       
    
    def iniciar_sesion(self, email, contrasena):
        usuario = self.user_dao.obtener_usuario_por_email(email)
        if usuario and usuario.contrasena == contrasena:  # Asegúrate de que la comparación de contraseñas sea segura
            print("Inicio de sesión exitoso.")
            return usuario
        else:
            print("Email o contraseña incorrectos.")
            return None
    

    def recuperar_contrasena(self, email):
        usuario = self.user_dao.obtener_usuario_por_email(email)
        if usuario:
            nueva_contrasena = input("Ingrese su nueva contraseña: ")
            self.user_dao.actualizar_contrasena(usuario.id_usuario, nueva_contrasena)
            print("Contraseña actualizada exitosamente.")
        else:
            print("Error: Usuario no encontrado.")

    @staticmethod
    def validar_email(email):
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(regex, email) is not None

    @staticmethod
    def validar_cuil(cuil):
        return len(cuil) == 11 and cuil.isdigit()

    @staticmethod
    def generar_contrasena_temporal():
        import random
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

# Ejemplo de uso de la clase UserService
if __name__ == "__main__":
    service = UserService()
    # Aquí puedes llamar a las funciones del servicio de usuario, por ejemplo:
    # service.registrar_inversor(...)