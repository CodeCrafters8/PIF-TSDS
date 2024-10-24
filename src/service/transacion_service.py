from decimal import Decimal
from datetime import datetime
from DAO.transaccion_dao import TransaccionDAO
from DAO.user_dao import UserDAO  
from DAO.cotizacion_dao import CotizacionDAO  
from model.transaccion import Transaccion

class TransaccionService:
    def __init__(self, transaccion_dao: TransaccionDAO, user_dao: UserDAO, cotizacion_dao: CotizacionDAO):
        self.transaccion_dao = transaccion_dao
        self.user_dao = user_dao  # DAO para actualizar el saldo del usuario
        self.cotizacion_dao = cotizacion_dao  # DAO para obtener el precio de la acción

    def comprar_accion(self, user, accion, cantidad):
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
                tipo_operacion_id=2,  # 2 indica compra
                inversor_id=user.id_inversor,
                comision=comision,
                id_accion=accion.id_accion  
            )
            
            # Insertar la transacción en la base de datos
            try:
                self.transaccion_dao.crear(transaccion)
            except Exception as e:
                print(f"Error al crear la transacción: {e}")
            
            # Actualizar el saldo del usuario en la base de datos (con id_operacion)
            self.user_dao.actualizar_saldo(user, total_a_restar, id_operacion=2)
            
            print("Compra exitosa.")
            return True
        else:
            print("Fondos insuficientes para realizar la compra.")
            return False
        
    def vender_accion(self, user, accion, cantidad):
        # Obtener el precio actual de venta de la acción
        precio_venta = self.cotizacion_dao.obtener_precio_reciente_venta(accion.id_accion)
        total_venta = precio_venta * cantidad
        comision = total_venta * Decimal('0.01')  # 1% de comisión
        total_a_sumar = total_venta - comision  # Total que se sumará al saldo

        # Verificar si el usuario tiene suficientes acciones para vender
        if True:  # Aquí puedes añadir la lógica de validación de acciones
            # Crear la transacción de venta
            transaccion = Transaccion(
                id_operacion=None,  # Cambia 'id_transaccion' por 'id_operacion'
                fecha=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Fecha actual con formato
                precio_operado=precio_venta,
                cantidad_operada=cantidad,
                cotizacion_id=accion.id_accion,  # Suponiendo que este es el ID correcto para cotización
                tipo_operacion_id=1,  # 1 indica venta
                inversor_id=user.id_inversor,
                comision=comision,
                id_accion=accion.id_accion  # Esto sigue siendo relevante
            )
            
            # Insertar la transacción en la base de datos
            try:
                self.transaccion_dao.crear(transaccion)
            except Exception as e:
                print(f"Error al crear la transacción: {e}")
            
            # Actualizar el saldo del usuario en la base de datos (con id_operacion)
            self.user_dao.actualizar_saldo(user, total_a_sumar, id_operacion=1)

            print("Venta exitosa.")
            return True
        else:
            print("No tiene suficientes acciones para vender.")
            return False
