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
from colorama import Fore, Style
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()

def encriptar_contraseña(contraseña):
    salt = bcrypt.gensalt()
    contraseña_encriptada = bcrypt.hashpw(contraseña.encode('utf-8'), salt)
    return contraseña_encriptada

def verificar_contraseña(contraseña, contraseña_encriptada):
    return bcrypt.checkpw(contraseña.encode('utf-8'), contraseña_encriptada)

def mostrar_menu():
    console.print("===========================", style="cyan bold")
    console.print("Bienvenido al Sistema ARG. Broker", style="yellow")
    console.print("===========================", style="cyan")
    console.print("1. Registrar nuevo inversor", style="green")
    console.print("2. Iniciar sesión", style="green")
    console.print("3. Recuperar contraseña", style="green")
    console.print("4. Salir", style="green")
    console.print("===========================", style="cyan")

def submenu_registro(service):
    console.print("---------------------------", style="cyan")
    console.print("Registro de Nuevo Inversor", style="yellow")
    console.print("---------------------------", style="cyan")
    cuil = Prompt.ask("Ingrese su CUIL", default="")
    nombre = Prompt.ask("Ingrese su nombre", default="")
    apellido = Prompt.ask("Ingrese su apellido", default="")
    email = Prompt.ask("Ingrese su email", default="")
    contraseña = Prompt.ask("Ingrese su contraseña", default="")
    contraseña_encriptada = encriptar_contraseña(contraseña)
    saldo_pesos = 1000000.00
    tipo_inversor = Prompt.ask("Ingrese tipo de perfil (conservador, moderado, agresivo)", default="")

    while tipo_inversor.lower() not in ["conservador", "moderado", "agresivo"]:
        console.print("Tipo de perfil no válido. Intente con: conservador, moderado o agresivo.", style="red")
        tipo_inversor = Prompt.ask("Ingrese tipo de perfil (conservador, moderado, agresivo)", default="")

    if service.registrar_inversor(cuil, nombre, apellido, email, contraseña_encriptada, saldo_pesos, tipo_inversor):
        console.print("Registro exitoso. Bienvenido!", style="green")
    else:
        console.print("Error en el registro. Verifique los datos e intente nuevamente.", style="red")

def submenu_iniciar_sesion(service, portafolio_service, transaccion_service, accion_dao):
    console.print("---------------------------", style="cyan")
    console.print("Iniciar Sesión", style="yellow")
    console.print("---------------------------", style="cyan")
    email = Prompt.ask("Ingrese su email", default="")
    contraseña = Prompt.ask("Ingrese su contraseña", default="")

    id_inversor = service.iniciar_sesion(email, contraseña)
    if id_inversor:
        console.print("Inicio de sesión exitoso.", style="green")
        
        informacion_inversores = service.obtener_informacion_inversores(id_inversor)
        
        table = Table(show_header=True, header_style="cyan")
        table.add_column("Nombre", style="white")
        table.add_column("Apellido", style="white")
        table.add_column("Email", style="white")
        table.add_column("Tipo de Perfil", style="white")
        table.add_column("Total Invertido", style="white")
        table.add_column("Saldo Pesos", style="white")

        for fila in informacion_inversores:
            table.add_row(fila[0], fila[1], fila[2], fila[3], f"${fila[4]:,.2f}", f"${fila[5]:,.2f}")

        console.print(table)

        while True:
            console.print("===========================", style="cyan")
            console.print("Opciones del Inversor", style="yellow")
            console.print("===========================", style="cyan")
            console.print("1. Consultar saldo", style="green")
            console.print("2. Portafolio", style="green")
            console.print("3. Realizar inversión", style="green")
            console.print("4. Cerrar sesión", style="green")
            console.print("===========================", style="cyan")
            opcion = Prompt.ask("Seleccione una opción", default="")

            if opcion == "1":
                saldo = portafolio_service.obtener_saldo_usuario(id_inversor)
                console.print(f"\nSu saldo disponible es: ${saldo:,.2f}", style="cyan")

            elif opcion == "2":
                portafolio_service.mostrar_portafolio(id_inversor)

            elif opcion == "3":
                console.print("1. Compra", style="green")
                console.print("2. Venta", style="green")
                tipo_operacion = Prompt.ask("Seleccione el Tipo de Operación", default="")
                
                if tipo_operacion == "1":  # Compra
                    acciones_disponibles = accion_dao.listar_acciones()
                    if acciones_disponibles:
                        console.print("Acciones Disponibles:", style="cyan")
                        table = Table(show_header=True, header_style="cyan")
                        table.add_column("ID")
                        table.add_column("Ticker")
                        table.add_column("Nombre")
                        table.add_column("Empresa ID")

                        for accion in acciones_disponibles:
                            table.add_row(str(accion.id_accion), accion.ticker, accion.nombre, str(accion.empresa_id))

                        console.print(table)

                        accion_id = Prompt.ask("Ingrese el ID de la acción que desea comprar", default="")
                        cantidad = int(Prompt.ask("Ingrese la cantidad que desea comprar", default=""))

                        resultado = transaccion_service.comprar_accion(id_inversor, accion_id, cantidad)
                        
                        if resultado:
                            console.print("Compra realizada con éxito.", style="green")
                        else:
                            console.print("Error al realizar la compra. Verifique su saldo o la disponibilidad de acciones.", style="red")
                    else:
                        console.print("No hay acciones disponibles.", style="red")

                elif tipo_operacion == "2":
                    portafolio_service.mostrar_portafolio(id_inversor)  
                    
                    accion_id = Prompt.ask("Ingrese el ID de la acción que desea vender", default="")
                    cantidad = int(Prompt.ask("Ingrese la cantidad que desea vender", default=""))
                    resultado = transaccion_service.vender_accion(id_inversor, accion_id, cantidad)
            elif opcion == "4":
                console.print("Cerrando sesión...", style="yellow")
                break
    else:
        console.print("Credenciales incorrectas. Intente nuevamente.", style="red")

def submenu_recuperar_contraseña(service):
    console.print("---------------------------", style="cyan")
    console.print("Recuperar Contraseña", style="yellow")
    console.print("---------------------------", style="cyan")
    email = Prompt.ask("Ingrese su email registrado", default="")
    if service.recuperar_contraseña(email):
        console.print("Se ha enviado un correo para restablecer su contraseña.", style="green")
    else:
        console.print("El email no está registrado. Verifique e intente nuevamente.", style="red")

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
        opcion = Prompt.ask("Seleccione una opción", default="")

        if opcion == "1":
            submenu_registro(service)

        elif opcion == "2":
            submenu_iniciar_sesion(service, portafolio_service, transaccion_service, accion_dao)

        elif opcion == "3":
            submenu_recuperar_contraseña(service)

        elif opcion == "4":
            console.print(Fore.YELLOW + "Saliendo del sistema...")
            break

        else:
            print(Fore.RED + "Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()