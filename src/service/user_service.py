# service/user_service.py

from model.user import User  
from DAO.user_dao import UserDao  
import bcrypt
class UserService:
    def __init__(self, user_dao: UserDao):
        self.user_dao = user_dao
        
    def get_user(self, inversor_id):
        """
        Obtiene un usuario por su ID.
        :param inversor_id: ID del usuario.
        :return: Objeto User si se encuentra, None si no se encuentra.
        """
        return self.user_dao.get(inversor_id)
    
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
        """_summary_
            Inicia sesión buscando al usuario por su email y verificando su contraseña.
        Args:
            email (srt): email del usuario
            contraseña (str): contraseña del usuario

        Returns:
            User: Objeto User si el inicio de sesión es exitoso, None si no lo es.
        """
        intentos_fallidos = 0
        max_intentos = 3

        while intentos_fallidos < max_intentos:
            # Buscar el usuario por email
            user = self.user_dao.obtener_usuario_por_email(email)

            if user:
                if user.verificar_contraseña(contraseña):
                    return user
                else:
                    intentos_fallidos += 1
                    if intentos_fallidos < max_intentos:
                        raise self.UserServiceError("Contraseña incorrecta")
            else:
                intentos_fallidos += 1
                if intentos_fallidos < max_intentos:
                    raise self.UserServiceError("Email no registrado")
        
        raise self.UserServiceError("Demasiados intentos fallidos. Tu cuenta ha sido bloqueada temporalmente.")

        
    def recuperar_contraseña (self, email):
        try: 
            user = self.user_dao.obtener_usuario_por_email(email)
            
            if user:
                nueva_contraseña = input("Introduzca nueva contraseña")
                
                hashed_password =bcrypt.hashpw(nueva_contraseña.encode('utf-8'),bcrypt.gensalt())
                
                self.user_dao.actualizar_contraseña(user.id_inversor, hashed_password.decode('utf-8'))
                
                print("Su contraseña ha sido actualizada")
                return nueva_contraseña
            else:

                raise self.UserServiceError("Email no registrado.")

        except Exception as e:
            raise self.UserServiceError(f"Error al recuperar la contraseña: {e}")
