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
        if not self.validar_email(email):
            print("Email inválido.")
            return False
        if not self.validar_cuil(cuil):
            print("Cuil inválido.")
            return False
        
        # Obtiene el ID del perfil inversor
        perfil_inversor = self.perfil_inversor_dao.obtener_perfil_por_tipo(tipo_perfil)  # Debes implementar este método
        if perfil_inversor is None:
            print("Tipo de perfil no válido.")
            return False
        
        id_perfil_inversor = perfil_inversor['id']  # Asegúrate de que esta línea coincida con tu estructura de datos
        
        # Crea una instancia de User incluyendo id_perfil_inversor
        usuario = User(id_perfil_inversor, nombre, apellido, email, contrasena, cuil, saldo_inicial)
        return self.user_dao.insertar_usuario(usuario)
    

    def iniciar_sesion(self, email, contrasena):
        usuario = self.user_dao.obtener_usuario_por_email(email)
        if usuario and usuario.contrasena == contrasena:
            print(f"Bienvenido, {usuario.nombre} {usuario.apellido}!")
            return True
        else:
            print("Email o contraseña incorrectos.")
            return False

    def recuperar_contrasena(self, email):
        usuario = self.user_dao.obtener_usuario_por_email(email)
        if usuario:
            nueva_contrasena = self.generar_contrasena_temporal()
            self.user_dao.actualizar_contrasena(usuario.id_usuario, nueva_contrasena)
            print(f"Nueva contraseña temporal generada: {nueva_contrasena}")
        else:
            print("No se encontró un usuario con ese email.")

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