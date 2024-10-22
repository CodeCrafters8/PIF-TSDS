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
                tipo_operacion_id=1,  # 1 indica compra
                inversor_id=user.id_inversor,
                comision=comision,
                id_accion=accion.id_accion  
            )
            
            # Insertar la transacción en la base de datos
            try:
                self.transaccion_dao.crear(transaccion)
            except Exception as e:
                print(f"Error al crear la transacción: {e}")
            
            # Actualizar el saldo del usuario en la base de datos
            self.user_dao.actualizar_saldo(user, total_a_restar)
            
            print("Compra exitosa.")
            return True
        else:
            print("Fondos insuficientes para realizar la compra.")
            return False
