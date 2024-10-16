import mysql.connector
from model.user import user
from DAO.user_dao import user_dao

def iniciar_sesion (user_dao):
    intentos_fallidos = 0
    max_intentos = 3
    
    while intentos_fallidos< max_intentos:
        email = input("Email: ")
        contraseña = input("Contraseña: ")
    
    user = user_dao.get_email(email)
    
    if user:
        if  user.verificar_contraseña(contraseña):
            print(f"¡Bienvenido a BROKER ARG, {user.nombre} {user.apellido}!")
            return user
        else:
            print("Contraseña incorrecta")
            intentos_fallidos += 1
    else:
        print("Email no registrado")
        intentos_fallidos += 1
        
    if intentos_fallidos >= max_intentos:
            print("Demasiados intentos fallidos. Tu cuenta ha sido bloqueada temporalmente.") 
        
    return None