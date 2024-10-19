from service.user_service import UserService
from database.data_base_conection import DBConn

def mostrar_bienvenida():
    print("********************************")
    print("  Bienvenidos al Sistema ARG. Broker  ")
    print("********************************")

def mostrar_menu_principal():
    print("1. Registrar nuevo inversor")
    print("2. Iniciar sesión")
    print("3. Recuperar contraseña")
    print("4. Salir")

def mostrar_submenu_registro():
    print("\n--- Registro de Inversor ---")
    cuil = input("Ingrese su CUIL: ")
    nombre = input("Ingrese su nombre: ")
    apellido = input("Ingrese su apellido: ")
    email = input("Ingrese su email: ")
    contraseña = input("Ingrese su contraseña: ")
    saldo_pesos = 1000000.00  
    tipo_inversor = input("Ingrese tipo de perfil (conservador, moderado, agresivo): ").lower()
    
    # Validaciones
    if tipo_inversor not in ["conservador", "moderado", "agresivo"]:
        print("Tipo de perfil no válido. Por favor, elija entre conservador, moderado o agresivo.")
        return
    
    if service.registrar_inversor(cuil, nombre, apellido, email, contraseña, saldo_pesos, tipo_inversor):
        print("Registro exitoso.")
    else:
        print("Error en el registro. Por favor, intente nuevamente.")

def mostrar_submenu_login():
    print("\n--- Iniciar Sesión ---")
    email = input("Ingrese su email: ")
    contraseña = input("Ingrese su contraseña: ")
    
    if service.iniciar_sesion(email, contraseña):
        print("Inicio de sesión exitoso.")
        # Aquí podrías redirigir a la página de usuario o mostrar datos
    else:
        print("Error en el inicio de sesión. Verifique su email y contraseña.")

def mostrar_submenu_recuperar_contrasena():
    print("\n--- Recuperar Contraseña ---")
    email = input("Ingrese su email: ")
    
    if service.recuperar_contraseña(email):
        print("Instrucciones para recuperar la contraseña han sido enviadas a su email.")
    else:
        print("Error en la recuperación de contraseña. Verifique su email.")

def main():
    print("")

if __name__ == "__main__":
    main()    
    
    db_conn = DBConn()  # Inicializa la clase de conexión a la base de datos
    service = UserService(db_conn)  # Pasa la instancia de DBConn a UserService

    mostrar_bienvenida()

    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mostrar_submenu_registro()

        elif opcion == "2":
            mostrar_submenu_login()

        elif opcion == "3":
            mostrar_submenu_recuperar_contrasena()

        elif opcion == "4":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción no válida. Intente nuevamente.")

