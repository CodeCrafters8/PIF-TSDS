import mysql.connector
from model.Transaccion import Transaccion
from DAO.Transaccion_dao import Transaccion_dao

class Transaccion_dao_imp(Transaccion_dao):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def create(self, Transaccion: Transaccion):
        try:
            cursor = self.db_conn.cursor()
            query = """
                INSERT INTO operacion (fecha, hora, cantidad_operada, cotizacion_id, tipo_operacion_id, inversor_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (Transaccion.fecha, Transaccion.hora, Transaccion.cantidad_operada,
                                   Transaccion.cotizacion_id, Transaccion.tipo_operacion_id, Transaccion.inversor_id))
            self.db_conn.commit()
        finally:
            cursor.close()

    def get_stock_quantity_in_portfolio(self, inversor_id, accion_id):
        try:
            cursor = self.db_conn.cursor()
            query = """
                SELECT pa.cantidad_tenencia
                FROM portafolio p
                JOIN portafolio_acciones pa ON p.id_portafolio = pa.portafolio_id
                WHERE p.id_inversor = %s AND pa.accion_id = %s
            """
            cursor.execute(query, (inversor_id, accion_id))
            row = cursor.fetchone()
            if row:
                return row[0]  # Retorna la cantidad de tenencia
            return 0  # Retorna 0 si no hay acciones
        finally:
            cursor.close()

    def get(self, transaccion_id):
        try:
            cursor = self.db_conn.cursor()
            query = """
                SELECT o.id_operacion, o.fecha, o.hora, o.cantidad_operada, 
                    c.precio_compra_actual, a.nombre
                FROM operacion o
                JOIN cotizacion c ON o.cotizacion_id = c.id_cotizacion
                JOIN acciones a ON c.accion_id = a.id_accion
                WHERE o.id_operacion = %s
            """
            cursor.execute(query, (transaccion_id,))
            row = cursor.fetchone()
            if row:
                return {
                    "id_operacion": row[0],
                    "fecha": row[1],
                    "hora": row[2],
                    "cantidad_operada": row[3],
                    "precio_compra_actual": row[4],
                    "accion_nombre": row[5]
                }
            return None
        finally:
            cursor.close()
           