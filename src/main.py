from service.user_service import UserService
from database.data_base_conection import DBConn
import bcrypt 
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)  # Inicializa colorama para usar colores automáticamente
def encriptar_contraseña(contraseña):
    # Genera un salt y encripta la contraseña
    salt = bcrypt.gensalt()
    contraseña_encriptada = bcrypt.hashpw(contraseña.encode('utf-8'), salt)
    return contraseña_encriptada

def verificar_contraseña(contraseña, contraseña_encriptada):
    # Verifica si la contraseña ingresada coincide con la encriptada
    return bcrypt.checkpw(contraseña.encode('utf-8'), contraseña_encriptada)


def mostrar_menu():
    print(Fore.CYAN + Style.BRIGHT + "===========================")
    print(Fore.YELLOW + "Bienvenido al Sistema ARG. Broker")
    print(Fore.CYAN + "===========================")
    print(Fore.GREEN + "1. Registrar nuevo inversor")
    print(Fore.GREEN + "2. Iniciar sesión")
    print(Fore.GREEN + "3. Recuperar contraseña")
    print(Fore.GREEN + "4. Salir")
    print(Fore.CYAN + "===========================")

def submenu_registro(service):
    print(Fore.CYAN + "---------------------------")
    print(Fore.YELLOW + "Registro de Nuevo Inversor")
    print(Fore.CYAN + "---------------------------")
    cuil = input(Fore.WHITE + "Ingrese su CUIL: ")
    nombre = input(Fore.WHITE + "Ingrese su nombre: ")
    apellido = input(Fore.WHITE + "Ingrese su apellido: ")
    email = input(Fore.WHITE + "Ingrese su email: ")
    contraseña = input(Fore.WHITE + "Ingrese su contraseña: ")
    contraseña_encriptada = encriptar_contraseña(contraseña)
    saldo_pesos = 1000000.00  # Saldo inicial predeterminado
    tipo_inversor = input(Fore.WHITE + "Ingrese tipo de perfil (conservador, moderado, agresivo): ")

    # Validaciones adicionales
    while tipo_inversor.lower() not in ["conservador", "moderado", "agresivo"]:
        print(Fore.RED + "Tipo de perfil no válido. Intente con: conservador, moderado o agresivo.")
        tipo_inversor = input(Fore.WHITE + "Ingrese tipo de perfil (conservador, moderado, agresivo): ")

    if service.registrar_inversor(cuil, nombre, apellido, email, contraseña, saldo_pesos, tipo_inversor):
        print(Fore.GREEN + "Registro exitoso. Bienvenido!")
    else:
        print(Fore.RED + "Error en el registro. Verifique los datos e intente nuevamente.")

def submenu_iniciar_sesion(service):
    print(Fore.CYAN + "---------------------------")
    print(Fore.YELLOW + "Iniciar Sesión")
    print(Fore.CYAN + "---------------------------")
    email = input(Fore.WHITE + "Ingrese su email: ")
    contraseña = input(Fore.WHITE + "Ingrese su contraseña: ")

    id_inversor = service.iniciar_sesion(email, contraseña)
    if id_inversor:  # Si la sesión fue exitosa
        print(Fore.GREEN + "Inicio de sesión exitoso.")

        # Obtener y mostrar información del inversor automáticamente
        informacion_inversores = service.obtener_informacion_inversores(id_inversor)
        print(Fore.CYAN + "\nDatos del Inversor:")
        print(Fore.CYAN + "Nombre | Apellido | Email | Tipo de Perfil | Total Invertido | Saldo Pesos")
        print(Fore.CYAN + "----------------------------------------------------------------------")
        for fila in informacion_inversores:
            print(Fore.WHITE + f"{fila[0]:<10} | {fila[1]:<10} | {fila[2]:<20} | {fila[3]:<15} | ${fila[4]:<15,.2f} | ${fila[5]:<15,.2f}")

        # Mostrar opciones adicionales después de mostrar los datos
        # while True:
        #     print(Fore.CYAN + "\n===========================")
        #     print(Fore.YELLOW + "Opciones del Inversor")
        #     print(Fore.CYAN + "===========================")
        #     print(Fore.GREEN + "1. Consultar saldo")
        #     print(Fore.GREEN + "2. Realizar inversión")
        #     print(Fore.GREEN + "3. Cerrar sesión")
        #     print(Fore.CYAN + "===========================")
        #     opcion = input(Fore.WHITE + "Seleccione una opción: ")

        #     if opcion == "1":
        #         # Mostrar saldo
        #         saldo = service.consultar_saldo(id_inversor)
        #         print(Fore.CYAN + f"\nSu saldo disponible es: ${saldo:,.2f}")

        #     elif opcion == "2":
        #         # Realizar una inversión
        #         monto = float(input(Fore.WHITE + "Ingrese el monto a invertir: "))
        #         if service.realizar_inversion(id_inversor, monto):
        #             print(Fore.GREEN + "Inversión realizada con éxito.")
        #         else:
        #             print(Fore.RED + "Error en la inversión. Verifique su saldo.")

        #     elif opcion == "3":
        #         print(Fore.YELLOW + "Cerrando sesión...")
        #         break
        #     else:
        #         print(Fore.RED + "Opción no válida. Intente nuevamente.")

    else:
        print(Fore.RED + "Credenciales incorrectas. Intente nuevamente.")

def submenu_recuperar_contraseña(service):
    print(Fore.CYAN + "---------------------------")
    print(Fore.YELLOW + "Recuperar Contraseña")
    print(Fore.CYAN + "---------------------------")
    email = input(Fore.WHITE + "Ingrese su email registrado: ")
    if service.recuperar_contraseña(email):
        print(Fore.GREEN + "Se ha enviado un correo para restablecer su contraseña.")
    else:
        print(Fore.RED + "El email no está registrado. Verifique e intente nuevamente.")

def main():
    db_conn = DBConn()  # Inicializa la clase de conexión a la base de datos
    service = UserService(db_conn)  # Pasa la instancia de DBConn a UserService

    while True:
        mostrar_menu()
        opcion = input(Fore.WHITE + "Seleccione una opción: ")

        if opcion == "1":
            submenu_registro(service)

        elif opcion == "2":
            submenu_iniciar_sesion(service)

        elif opcion == "3":
            submenu_recuperar_contraseña(service)

        elif opcion == "4":
            print(Fore.YELLOW + "Saliendo del sistema...")
            break

        else:
            print(Fore.RED + "Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()