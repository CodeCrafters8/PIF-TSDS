from DAO.transaccion_dao_imp import Transaccion_dao_imp
from model.transaccion import Transaccion


class TransaccionService:
    def __init__(self, Transaccion_dao: Transaccion_dao_imp, user_service):
        self.Transaccion_dao = Transaccion_dao
        self.user_service = user_service  # Para acceder a los datos del usuario

    def create_Transaccion(self, fecha, hora, cantidad_operada, cotizacion_id, tipo_operacion_id, inversor_id):
        # Obtener detalles de la cotización
        cotizacion_detalle = self.Transaccion_dao.get(cotizacion_id)

        if not cotizacion_detalle:
            print("Error: No se pudo obtener la cotización.")
            return

        # Validaciones
        if not self.validar_transaccion(cantidad_operada, cotizacion_detalle, inversor_id, tipo_operacion_id):
            print("Error: La transacción no es válida.")
            return
        
        # Crear la transacción
        Transaccion = Transaccion(None, fecha, hora, cantidad_operada, cotizacion_id, tipo_operacion_id, inversor_id)

        if Transaccion.validate():
            self.Transaccion_dao.create(Transaccion)
            print(f"Transacción creada: {Transaccion}")
        else:
            print("Error: Operación inválida.")

    def validar_transaccion(self, cantidad_operada, cotizacion_detalle, inversor_id, tipo_operacion_id):
        """Valida las condiciones para la compra o venta de acciones."""
        # Verifica que la cantidad sea positiva
        if cantidad_operada <= 0:
            print("Error: La cantidad de acciones debe ser mayor a cero.")
            return False

        # Verificar que el precio de compra actual sea válido
        precio_compra_actual = cotizacion_detalle['precio_compra_actual']
        if precio_compra_actual <= 0:
            print("Error: El precio de compra debe ser mayor a cero.")
            return False

        # Verificar el saldo para compra
        if tipo_operacion_id == 1:  # Suponiendo que 1 es "Compra"
            usuario = self.user_service.get_user(inversor_id)
            total_compra = cantidad_operada * precio_compra_actual
            if usuario.saldo_cuenta < total_compra:
                print("Error: No tienes suficiente saldo para realizar esta compra.")
                return False

        # Verificar las existencias para venta
        if tipo_operacion_id == 2:  # Suponiendo que 2 es "Venta"
            acciones_disponibles = self.Transaccion_dao.get_stock_quantity_in_portfolio(inversor_id, cotizacion_detalle['accion_id'])
            if acciones_disponibles < cantidad_operada:
                print("Error: No tienes suficientes acciones para vender.")
                return False

        return True
