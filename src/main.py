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
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

def encriptar_contraseña(contraseña):
    salt = bcrypt.gensalt()
    contraseña_encriptada = bcrypt.hashpw(contraseña.encode('utf-8'), salt)
    return contraseña_encriptada

def verificar_contraseña(contraseña, contraseña_encriptada):
    return bcrypt.checkpw(contraseña.encode('utf-8'), contraseña_encriptada)

def mostrar_menu():
    titulo = Panel("[yellow bold]ArgBroker by CodeCrafter8[/]", style="cyan", expand=False)
    opciones_menu = (
        "[green]1.[/] Registrar nuevo inversor\n"
        "[green]2.[/] Iniciar sesión\n"
        "[green]3.[/] Recuperar contraseña\n"
        "[green]4.[/] Salir"
    )
    console.print(titulo)
    console.print(Panel(opciones_menu, title="Menú Principal", style="bright_cyan", border_style="cyan"))

def submenu_registro(service):
    console.print(Panel("[yellow bold]Registro de Nuevo Inversor[/]", style="cyan"))
    cuil = Prompt.ask("Ingrese su CUIL", default="")
    nombre = Prompt.ask("Ingrese su nombre", default="")
    apellido = Prompt.ask("Ingrese su apellido", default="")
    email = Prompt.ask("Ingrese su email", default="")
    contraseña = Prompt.ask("Ingrese su contraseña", default="")
    contraseña_encriptada = encriptar_contraseña(contraseña)
    saldo_pesos = 1000000.00
    tipo_inversor = Prompt.ask("Ingrese tipo de perfil (conservador, moderado, agresivo)", default="")

    while tipo_inversor.lower() not in ["conservador", "moderado", "agresivo"]:
        console.print("[red]Tipo de perfil no válido. Intente con: conservador, moderado o agresivo.[/]")
        tipo_inversor = Prompt.ask("Ingrese tipo de perfil (conservador, moderado, agresivo)", default="")

    if service.registrar_inversor(cuil, nombre, apellido, email, contraseña_encriptada, saldo_pesos, tipo_inversor):
        console.print("[green]Registro exitoso. Bienvenido![/]")
    else:
        console.print("[red]Error en el registro. Verifique los datos e intente nuevamente.[/]")

def submenu_iniciar_sesion(service, portafolio_service, transaccion_service, accion_dao):
    console.print(Panel("[yellow bold]Iniciar Sesión[/]", style="cyan"))
    email = Prompt.ask("Ingrese su email", default="")
    contraseña = Prompt.ask("Ingrese su contraseña", default="")

    id_inversor = service.iniciar_sesion(email, contraseña)
    if id_inversor:
        console.print("[green]Inicio de sesión exitoso.[/]")
        
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
            console.print(Panel("[yellow bold]Opciones del Inversor[/]", style="cyan"))
            console.print("[green]1.[/] Consultar saldo\n[green]2.[/] Portafolio\n[green]3.[/] Realizar inversión\n[green]4.[/] Cerrar sesión")
            opcion = Prompt.ask("Seleccione una opción", default="")

            if opcion == "1":
                saldo = portafolio_service.obtener_saldo_usuario(id_inversor)
                saldo_panel = Panel(
                    f"[bold cyan]Su saldo disponible es:[/] ${saldo:,.2f}",
                    title="[bold yellow]Consulta de Saldo[/]",
                    border_style="cyan"
                    )
                console.print(saldo_panel)

            elif opcion == "2":
                portafolio_service.mostrar_portafolio(id_inversor)
                
            elif opcion == "3":
                operacion_panel = Panel(
                    "[bold green]1.[/] Compra\n[bold green]2.[/] Venta",
                    title="[bold yellow]Tipo de Operación[/]",
                    border_style="green"
                    )
                console.print(operacion_panel)
                tipo_operacion = Prompt.ask("Seleccione el Tipo de Operación", default="")
                
                if tipo_operacion == "1":  # Compra
                    acciones_disponibles = accion_dao.listar_acciones()
                    if acciones_disponibles:
                        acciones_table = Table(show_header=True, header_style="bold cyan")
                        acciones_table.add_column("ID de Acción")
                        acciones_table.add_column("Ticker")
                        acciones_table.add_column("Nombre")
                        acciones_table.add_column("ID de Empresa")
                        
                        for accion in acciones_disponibles:
                            acciones_table.add_row(str(accion.id_accion), accion.ticker, accion.nombre, str(accion.empresa_id))
                            acciones_panel = Panel(acciones_table, title="[bold yellow]Acciones Disponibles para Compra[/]", border_style="blue")
                            console.print(acciones_panel)
                            
                            accion_id = Prompt.ask("Ingrese el ID de la acción que desea comprar", default="")
                            cantidad = int(Prompt.ask("Ingrese la cantidad que desea comprar", default=""))
                            resultado = transaccion_service.comprar_accion(id_inversor, accion_id, cantidad)
                            
                            if resultado:
                                console.print(Panel("[green]Compra realizada con éxito.[/]", border_style="green"))
                            else:
                                console.print(Panel("[red]Error en la compra. Verifique su saldo o disponibilidad de acciones.[/]", border_style="red"))
                                
                    else:
                        console.print(Panel("[red]No hay acciones disponibles en este momento.[/]", border_style="red"))
                    
                elif tipo_operacion == "2":  # Venta
                    portafolio_service.mostrar_portafolio(id_inversor)
                    accion_id = Prompt.ask("Ingrese el ID de la acción que desea vender", default="")
                    cantidad = int(Prompt.ask("Ingrese la cantidad que desea vender", default=""))
                    resultado = transaccion_service.vender_accion(id_inversor, accion_id, cantidad)
                    
                    if resultado:
                        console.print(Panel("[green]Venta realizada con éxito.[/]", border_style="green"))
                    else:
                        console.print(Panel("[red]Error al realizar la venta. Verifique la cantidad disponible.[/]", border_style="red"))

            elif opcion == "4":
                console.print("[yellow]Cerrando sesión...[/]")
                break
    else:
        console.print("[red]Credenciales incorrectas. Intente nuevamente.[/]")

def submenu_recuperar_contraseña(service):
    console.print(Panel("[yellow bold]Recuperar Contraseña[/]", style="cyan"))
    email = Prompt.ask("Ingrese su email registrado", default="")
    if service.recuperar_contraseña(email):
        console.print("[green]Se ha enviado un correo para restablecer su contraseña.[/]")
    else:
        console.print("[red]El email no está registrado. Verifique e intente nuevamente.[/]")

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
                                           user_dao, transaccion_service)

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
            console.print("[yellow]Saliendo del sistema...[/]")
            break

        else:
            console.print("[red]Opción no válida. Intente nuevamente.[/]")

if __name__ == "__main__":
    main()