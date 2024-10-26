from service.user_service import UserService
from service.portafolio_service import PortafolioService
from service.transaccion_service import TransaccionService
from DAO.portafolio_dao_imp import PortafolioDAOImpl
from DAO.user_dao_imp import UserDAOImpl
from DAO.cotizacion_dao_imp import CotizacionDAOImp
from DAO.accion_dao_imp import AccionDAOImpl  
from DAO.transaccion_dao_imp import TransaccionDAOImp
from database.data_base_conection import DBConn
import bcrypt 
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

def encriptar_contraseña(contraseña):
    salt = bcrypt.gensalt()
    contraseña_encriptada = bcrypt.hashpw(contraseña.encode('utf-8'), salt)
    return contraseña_encriptada

def verificar_contraseña(contraseña, contraseña_encriptada):
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
    saldo_pesos = 1000000.00
    tipo_inversor = input(Fore.WHITE + "Ingrese tipo de perfil (conservador, moderado, agresivo): ")

    while tipo_inversor.lower() not in ["conservador", "moderado", "agresivo"]:
        print(Fore.RED + "Tipo de perfil no válido. Intente con: conservador, moderado o agresivo.")
        tipo_inversor = input(Fore.WHITE + "Ingrese tipo de perfil (conservador, moderado, agresivo): ")

    if service.registrar_inversor(cuil, nombre, apellido, email, contraseña_encriptada, saldo_pesos, tipo_inversor):
        print(Fore.GREEN + "Registro exitoso. Bienvenido!")
    else:
        print(Fore.RED + "Error en el registro. Verifique los datos e intente nuevamente.")

def submenu_iniciar_sesion(service, portafolio_service, transaccion_service, accion_dao):
    print(Fore.CYAN + "---------------------------")
    print(Fore.YELLOW + "Iniciar Sesión")
    print(Fore.CYAN + "---------------------------")
    email = input(Fore.WHITE + "Ingrese su email: ")
    contraseña = input(Fore.WHITE + "Ingrese su contraseña: ")

    id_inversor = service.iniciar_sesion(email, contraseña)
    if id_inversor:
        print(Fore.GREEN + "Inicio de sesión exitoso.")
        
        informacion_inversores = service.obtener_informacion_inversores(id_inversor)
        print(Fore.CYAN + "\nDatos del Inversor:")
        print(Fore.CYAN + "Nombre | Apellido | Email | Tipo de Perfil | Total Invertido | Saldo Pesos")
        print(Fore.CYAN + "----------------------------------------------------------------------")
        for fila in informacion_inversores:
            print(Fore.WHITE + f"{fila[0]:<10} | {fila[1]:<10} | {fila[2]:<20} | {fila[3]:<15} | ${fila[4]:<15,.2f} | ${fila[5]:<15,.2f}")

        while True:
            print(Fore.CYAN + "\n===========================")
            print(Fore.YELLOW + "Opciones del Inversor")
            print(Fore.CYAN + "===========================")
            print(Fore.GREEN + "1. Consultar saldo")
            print(Fore.GREEN + "2. Portafolio")
            print(Fore.GREEN + "3. Realizar inversión")
            print(Fore.GREEN + "4. Cerrar sesión")
            print(Fore.CYAN + "===========================")
            opcion = input(Fore.WHITE + "Seleccione una opción: ")

            if opcion == "1":
                saldo = portafolio_service.obtener_saldo_usuario(id_inversor)
                print(Fore.CYAN + f"\nSu saldo disponible es: ${saldo:,.2f}")

            elif opcion == "2":
                portafolio_service.mostrar_portafolio(id_inversor)

            elif opcion == "3":
                print(Fore.GREEN + "1. Compra")
                print(Fore.GREEN + "2. Venta")
                tipo_operacion = input("Seleccione el Tipo de Operación: ")
                
                if tipo_operacion == "1":  # Compra
                    acciones_disponibles = accion_dao.listar_acciones()
                    if acciones_disponibles:
                        print(Fore.CYAN + "Acciones Disponibles:")
                        print(Fore.CYAN + "ID | Ticker | Nombre | Empresa ID")
                        for accion in acciones_disponibles:
                            print(Fore.WHITE + f"{accion.id_accion} | {accion.ticker} | {accion.nombre} | {accion.empresa_id}")

                        accion_id = input(Fore.WHITE + "Ingrese el ID de la acción que desea comprar: ")
                        cantidad = int(input(Fore.WHITE + "Ingrese la cantidad que desea comprar: "))
                        
                        resultado = transaccion_service.comprar_accion(id_inversor, accion_id, cantidad)
                        
                        if resultado:
                            print(Fore.GREEN + "Compra realizada con éxito.")
                        else:
                            print(Fore.RED + "Error al realizar la compra. Verifique su saldo o la disponibilidad de acciones.")
                    else:
                        print(Fore.RED + "No hay acciones disponibles.")

                elif tipo_operacion == "2":
                    # Mostrar acciones en portafolio
                    portafolio_service.mostrar_portafolio(id_inversor)  
                    
                    accion_id = input(Fore.WHITE + "Ingrese el ID de la acción que desea vender: ")
                    cantidad = int(input(Fore.WHITE + "Ingrese la cantidad que desea vender: "))
                    resultado = transaccion_service.vender_accion(id_inversor, accion_id, cantidad)
            elif opcion == "4":
                print(Fore.YELLOW + "Cerrando sesión...")
                break
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
    db_conn = DBConn()  # Conexión a la base de datos
    service = UserService(db_conn)

    # Instancias de los DAOs con la conexión de base de datos
    user_dao = UserDAOImpl(db_conn)
    portafolio_dao = PortafolioDAOImpl(db_conn)
    cotizacion_dao = CotizacionDAOImp(db_conn)
    accion_dao = AccionDAOImpl(db_conn)
    transaccion_dao = TransaccionDAOImp(db_conn) 

    # Crear los servicios necesarios con los DAOs correspondientes
    transaccion_service = TransaccionService(db_conn, user_dao, accion_dao, 
                                        cotizacion_dao, portafolio_dao, transaccion_dao)
    portafolio_service = PortafolioService(db_conn, portafolio_dao, cotizacion_dao,
                                        user_dao,transaccion_service)

    while True:
        mostrar_menu()
        opcion = input(Fore.WHITE + "Seleccione una opción: ")

        if opcion == "1":
            submenu_registro(service)

        elif opcion == "2":
            submenu_iniciar_sesion(service, portafolio_service, transaccion_service, accion_dao)

        elif opcion == "3":
            submenu_recuperar_contraseña(service)

        elif opcion == "4":
            print(Fore.YELLOW + "Saliendo del sistema...")
            break

        else:
            print(Fore.RED + "Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()