from service.user_service import UserService
from database.data_base_conection import DBConn

import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)  # Inicializa colorama para usar colores automáticamente

def mostrar_menu():
    print(Fore.CYAN + Style.BRIGHT + "===========================")
    print(Fore.YELLOW + "Bienvenido al Sistema ARG. Broker")
    print(Fore.CYAN + "===========================")
    print(Fore.GREEN + "1. Registrar nuevo inversor")
    print(Fore.GREEN + "2. Iniciar sesión")
    print(Fore.GREEN + "3. Recuperar contraseña")
    print(Fore.GREEN + "4. Salir")
    print(Fore.CYAN + "===========================")

def main():
    db_conn = DBConn()  # Inicializa la clase de conexión a la base de datos
    service = UserService(db_conn)  # Pasa la instancia de DBConn a UserService

    while True:
        mostrar_menu()
        opcion = input(Fore.WHITE + "Seleccione una opción: ")

        if opcion == "1":
            cuil = input(Fore.WHITE + "Ingrese su CUIL: ")
            nombre = input(Fore.WHITE + "Ingrese su nombre: ")
            apellido = input(Fore.WHITE + "Ingrese su apellido: ")
            email = input(Fore.WHITE + "Ingrese su email: ")
            contraseña = input(Fore.WHITE + "Ingrese su contraseña: ")
            saldo_pesos = 1000000.00  
            tipo_inversor = input(Fore.WHITE + "Ingrese tipo de perfil (conservador, moderado, agresivo): ")

            if service.registrar_inversor(cuil, nombre, apellido, email, contraseña, saldo_pesos, tipo_inversor):
                print(Fore.GREEN + "Registro exitoso.")
            else:
                print(Fore.RED + "Error en el registro.")

        elif opcion == "2":
            email = input(Fore.WHITE + "Ingrese su email: ")
            contraseña = input(Fore.WHITE + "Ingrese su contraseña: ")
            id_inversor = service.iniciar_sesion(email, contraseña)
            if id_inversor:  # Si la sesión fue exitosa
                # Obtener y mostrar información del inversor
                informacion_inversores = service.obtener_informacion_inversores(id_inversor)
                print(Fore.CYAN + "\nNombre | Apellido | Email | Tipo de Perfil | Total Invertido | Saldo Pesos")
                print(Fore.CYAN + "----------------------------------------------------------------------")
                for fila in informacion_inversores:
                    print(Fore.WHITE + f"{fila[0]:<10} | {fila[1]:<10} | {fila[2]:<20} | {fila[3]:<15} | ${fila[4]:<15,.2f} | ${fila[5]:<15,.2f}")
            else:
                print(Fore.RED + "Credenciales incorrectas. Intente nuevamente.")

        elif opcion == "3":
            email = input(Fore.WHITE + "Ingrese su email: ")
            service.recuperar_contraseña(email)

        elif opcion == "4":
            print(Fore.YELLOW + "Saliendo del sistema...")
            break

        else:
            print(Fore.RED + "Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()