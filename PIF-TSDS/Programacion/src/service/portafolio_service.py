# portafolio_service.py

from DAO.portafolio_dao_imp import PortafolioDAOImpl
from DAO.user_dao_imp import UserDAOImpl
from DAO.cotizacion_dao_imp import CotizacionDAOImp
from service.transaccion_service import TransaccionService
from model.portafolio import Portafolio
from database.data_base_conection import DBConn
from rich.console import Console
from rich.table import Table

class PortafolioService:
    def __init__(self, db_conn, portafolio_dao, cotizacion_dao, user_dao, transaccion_service):
        self.db_conn = db_conn
        self.portafolio_dao = portafolio_dao
        self.cotizacion_dao = cotizacion_dao
        self.user_dao = user_dao
        self.transaccion_service = transaccion_service

    def mostrar_portafolio(self, id_inversor):
        portafolio = self.portafolio_dao.obtener_portafolio_por_id_inversor(id_inversor)
        console = Console()  # Inicializa el objeto Console para imprimir en la consola
        
        if not portafolio:
            console.print("No se encontró el portafolio para el inversor especificado.", style="bold red")
            return
        
        acciones = portafolio.acciones
        saldo = self.obtener_saldo_usuario(id_inversor)
        total_invertido = 0
        rendimiento_total = 0  # Inicializamos el rendimiento total
        
        console.print(f"Saldo actual: [bold green]{saldo:.2f}[/bold green]")
        
        # Crear la tabla
        table = Table(title="Portafolio del Inversor")
        
        table.add_column("ID", style="cyan", justify="right")
        table.add_column("Ticker", style="magenta")
        table.add_column("Empresa", style="yellow")
        table.add_column("Cantidad Total", style="green", justify="right")
        table.add_column("Precio Promedio Compra", style="blue", justify="right")
        table.add_column("Precio Actual", style="blue", justify="right")
        table.add_column("Rendimiento", style="red", justify="right")
        
        for accion_con_tenencia in acciones:
            accion = accion_con_tenencia.accion  # Obtén el objeto Accion
            cantidad_tenencia = accion_con_tenencia.cantidad_tenencia  # Obtén la cantidad en tenencia
            
            # Obtener las transacciones para el inversor y la acción
            transacciones = self.transaccion_service.obtener_transacciones_por_accion_y_inversor(id_inversor, accion.id_accion)
            
            # Calcular la sumatoria de precio_operado * cantidad_operada y la cantidad total
            suma_precio_operado = sum(t.precio_operado * t.cantidad_operada for t in transacciones)
            suma_cantidad_operada = sum(t.cantidad_operada for t in transacciones)

            # Calcular el precio promedio de compra
            precio_promedio_compra = suma_precio_operado / suma_cantidad_operada if suma_cantidad_operada > 0 else 0

            # Obtener el precio actual usando el método existente
            precio_actual = self.cotizacion_dao.obtener_precio_reciente_compra(accion.id_accion)
            precio_venta = self.cotizacion_dao.obtener_precio_reciente_venta(accion.id_accion)
            
            # Calcular rendimiento
            rendimiento = (precio_actual - precio_promedio_compra) * cantidad_tenencia if cantidad_tenencia > 0 else 0

            # Agregar una fila a la tabla
            table.add_row(
                str(accion.id_accion),
                accion.ticker,
                accion.nombre,
                str(cantidad_tenencia),
                f"{precio_promedio_compra:.2f}",
                f"{precio_actual:.2f}",
                f"{rendimiento:.2f}"
                )
            
            total_invertido += suma_precio_operado 
            rendimiento_total += rendimiento  # Sumar el rendimiento de la acción al rendimiento total
            
        console.print(table)
        console.print(f"Total invertido: [bold blue]{total_invertido:.2f}[/bold blue]")
        console.print(f"Rendimiento total del portafolio: [bold red]{rendimiento_total:.2f}[/bold red]")  # Mostrar el rendimiento total

    def obtener_portafolio(self, id_inversor):
        return self.portafolio_dao.obtener_portafolio(id_inversor)

    def obtener_saldo_usuario(self, id_inversor):
        usuario = self.user_dao.obtener_usuario_por_id(id_inversor)
        return usuario.saldo_pesos

    def actualizar_saldo_usuario(self, id_inversor, nuevo_saldo):
        self.user_dao.actualizar_saldo(id_inversor, nuevo_saldo)

    def calcular_rendimiento_accion(self, id_inversor, id_accion):
        # Paso 1: Obtener las transacciones del inversor para la acción
        transacciones = self.transaccion_service.obtener_transacciones_por_accion_y_inversor(id_inversor, id_accion)
        print(transacciones)
        if not transacciones:
            print("No se encontraron transacciones para esta acción.")
            return 0.0  # O el valor que consideres adecuado para no tener datos
        
        # Paso 2: Calcular la sumatoria de precio_operado * cantidad_operada y la suma de cantidad_operada
        suma_precio_operado_cantidad = sum(t.precio_operado * t.cantidad_operada for t in transacciones)
        suma_cantidad_operada = sum(t.cantidad_operada for t in transacciones)

        # Paso 3: Calcular el precio promedio de compra
        if suma_cantidad_operada == 0:
            print("No hay cantidad operada, no se puede calcular el precio promedio.")
            return 0.0

        precio_promedio_compra = suma_precio_operado_cantidad / suma_cantidad_operada

        # Paso 4: Obtener el precio actual
        precio_actual = self.cotizacion_dao.obtener_precio_reciente_compra(id_accion)

        if precio_actual is None:
            print("No se pudo obtener el precio actual de la acción.")
            return 0.0

        # Paso 5: Calcular el rendimiento
        rendimiento = (precio_actual - precio_promedio_compra) * suma_cantidad_operada

        # Retorna el rendimiento calculado
        return rendimiento
    
    def vender_acciones(self, id_inversor, ticker, cantidad, precio_venta):
        acciones = self.portafolio_dao.obtener_acciones_por_usuario(id_inversor)
        
        accion = self.buscar_accion_por_ticker(acciones, ticker)

        if accion and accion['cantidad'] >= cantidad:
            total_venta = cantidad * precio_venta
            self.portafolio_dao.reducir_o_eliminar_accion(id_inversor, ticker, cantidad)
            nuevo_saldo = self.obtener_saldo_usuario(id_inversor) + total_venta
            self.actualizar_saldo_usuario(id_inversor, nuevo_saldo)
            print(f"Venta exitosa. Nuevo saldo: {nuevo_saldo:.2f}")
        else:
            print("No tienes suficientes acciones para vender.")

    def buscar_accion_por_ticker(self, acciones, ticker):
        for accion in acciones:
            if accion['ticker'] == ticker:
                return accion
        return None
