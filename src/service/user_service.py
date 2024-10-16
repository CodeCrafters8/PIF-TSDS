import re
from database.data_base_conection import ConexionDB
from DAO.user_dao_imp import UserDAOImpl
from DAO.perfil_Inversor_dao_imp import PerfilInversorDAOImpl


class UserService:
    def __init__(self):
        self.db = ConexionDB()
        self.user_dao = UserDAOImpl(self.db)
        self.perfil_inversor_dao = PerfilInversorDAOImpl(self.db)

    def registrar_inversor(self, nombre, apellido, cuil, email, contrasena, saldo_inicial, tipo_perfil):
        if not self.validar_email(email):
            print("Email inválido.")
            return False
        if not self.validar_cuil(cuil):
            print("Cuil inválido.")
            return False
        
        return self.user_dao.registrar_usuario(nombre, apellido, cuil, email, contrasena, saldo_inicial, tipo_perfil)

    def iniciar_sesion(self, email, contrasena):
        usuario = self.user_dao.obtener_usuario_por_email(email)
        if usuario and usuario['contrasena'] == contrasena:
            print(f"Bienvenido, {usuario['Nombre']} {usuario['Apellido']}!")
            return True
        else:
            print("Email o contraseña incorrectos.")
            return False

    def recuperar_contrasena(self, email):
        usuario = self.user_dao.obtener_usuario_por_email(email)
        if usuario:
            nueva_contrasena = self.generar_contrasena_temporal()
            self.user_dao.actualizar_contrasena(usuario['ID_Usuario'], nueva_contrasena)
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