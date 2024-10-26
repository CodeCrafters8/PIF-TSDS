from decimal import Decimal
from datetime import datetime
from DAO.transaccion_dao import TransaccionDAO
from DAO.user_dao import UserDAO  
from DAO.cotizacion_dao import CotizacionDAO  
from DAO.accion_dao import AccionDAO
from DAO.portafolio_dao import PortafolioDAO
from DAO.transaccion_dao import TransaccionDAO
from model.transaccion import Transaccion

class TransaccionService:
    def __init__(self, db_conn, user_dao, accion_dao, cotizacion_dao, portafolio_dao, transaccion_dao):
        self.db_conn = db_conn
        self.user_dao = user_dao
        self.accion_dao = accion_dao
        self.cotizacion_dao = cotizacion_dao
        self.portafolio_dao = portafolio_dao
        self.transaccion_dao = transaccion_dao 
        
    def comprar_accion(self, id_inversor, accion_id, cantidad):
        user = self.user_dao.obtener_usuario_por_id(id_inversor)
        accion = self.accion_dao.obtener_accion_por_id(accion_id)

        if accion is None:
            print("La acción con el ID proporcionado no existe.")
            return False

        # Obtener el precio actual de la acción
        precio = self.cotizacion_dao.obtener_precio_reciente_compra(accion.id_accion)
        total_costo = precio * cantidad
        comision = total_costo * Decimal('0.01')  # 1% de comisión
        total_a_restar = total_costo + comision

        if user.saldo_pesos >= total_a_restar:
            # Crear la transacción
            transaccion = Transaccion(
                id_operacion=None,
                fecha=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Fecha actual con formato
                precio_operado=precio,
                cantidad_operada=cantidad,
                cotizacion_id=accion.id_accion,
                tipo_operacion_id=1,  # 2 indica compra
                inversor_id=user.id_inversor,
                comision=comision,
                id_accion=accion.id_accion
            )

            # Insertar la transacción en la base de datos
            try:
                self.transaccion_dao.crear(transaccion)
            except Exception as e:
                print(f"Error al crear la transacción: {e}")
                return False

            # Actualizar el saldo del usuario en la base de datos
            self.user_dao.actualizar_saldo(user, total_a_restar, id_operacion=2)

            # Actualizar el portafolio
            portafolio_id = self.portafolio_dao.obtener_portafolio_id_por_inversor(user.id_inversor)
            print(type(portafolio_id))
            print (portafolio_id)
            
            # Verificar si ya existe la acción en el portafolio
            if self.portafolio_dao.existe_accion_en_portafolio(portafolio_id, accion_id):
                # Obtener la cantidad actual de tenencia
                cantidad_actual = self.portafolio_dao.obtener_cantidad_tenencia(portafolio_id, accion_id)
                nueva_cantidad = cantidad_actual + cantidad
                self.portafolio_dao.actualizar_accion(portafolio_id, accion_id, nueva_cantidad)
            else:
                # Si no existe, agregar la acción al portafolio
                self.portafolio_dao.agregar_accion(portafolio_id, accion_id, cantidad)
            print("Compra exitosa.")
            return True
        else:
            print("Fondos insuficientes para realizar la compra.")
            return False
    
    def vender_accion(self, id_inversor, accion_id, cantidad):
        # Obtener el precio actual de venta de la acción
        precio_venta = self.cotizacion_dao.obtener_precio_reciente_venta(accion_id)
        user = self.user_dao.obtener_usuario_por_id(id_inversor)
        total_venta = precio_venta * cantidad
        comision = total_venta * Decimal('0.01')  # 1% de comisión
        total_a_sumar = total_venta - comision  # Total que se sumará al saldo

        # Obtener el ID del portafolio y verificar si el inversor tiene suficientes acciones
        portafolio_id = self.portafolio_dao.obtener_portafolio_id_por_inversor(id_inversor)
        cantidad_disponible = self.portafolio_dao.obtener_cantidad_tenencia(portafolio_id, accion_id)

        if cantidad_disponible >= cantidad:
            # Crear la transacción de venta
            transaccion = Transaccion(
                id_operacion=None,  
                fecha=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  
                precio_operado=precio_venta,
                cantidad_operada=cantidad,
                cotizacion_id=accion_id,  
                tipo_operacion_id=2,  
                inversor_id=user.id_inversor,
                comision=comision,
                id_accion=accion_id  
            )
            
            # Insertar la transacción en la base de datos
            try:
                self.transaccion_dao.crear(transaccion)
            except Exception as e:
                print(f"Error al crear la transacción: {e}")
                return False
            
            # Actualizar el saldo del usuario en la base de datos
            self.user_dao.actualizar_saldo(user, total_a_sumar, id_operacion=1)

            # Actualizar la cantidad de acciones en el portafolio
            nueva_cantidad = cantidad_disponible - cantidad
            self.portafolio_dao.actualizar_accion(portafolio_id, accion_id, nueva_cantidad)

            print("Venta exitosa.")
            return True
        else:
            print("No tiene suficientes acciones para vender.")
            return False

    def obtener_transacciones_por_accion_y_inversor(self, id_inversor, id_accion):
        return self.transaccion_dao.obtener_transacciones_por_accion_y_inversor(id_inversor, id_accion)