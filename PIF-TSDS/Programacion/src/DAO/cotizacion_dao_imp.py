# cotizacion_dao_imp.py (implementación)
from DAO.cotizacion_dao import CotizacionDAO  # Importar la interfaz
import mysql.connector
from database.data_base_conection import DBConn

class CotizacionDAOImp(CotizacionDAO):
    def __init__(self, db_conn:DBConn):
        self.db_conn = db_conn



    def obtener_precio_reciente_compra(self, id_accion):
        conn = self.db_conn.connect_to_mysql()
        try:
            cursor = conn.cursor()
            query = """
                SELECT Precio_Compra_Actual 
                FROM Cotizacion 
                WHERE accion_id = %s 
                ORDER BY ID_Cotizacion DESC LIMIT 1
            """
            cursor.execute(query, (id_accion,))
            resultado = cursor.fetchone()
            if resultado:
                return resultado[0]
            else:
                return None  
        except Exception as e:
            print(f"Error al obtener cotización: {e}")
        finally:
            cursor.close()

    def obtener_precio_reciente_venta(self, id_accion):
        conn = self.db_conn.connect_to_mysql()
        try:
            cursor = conn.cursor()
            query = """
                SELECT Precio_Venta_Actual 
                FROM Cotizacion 
                WHERE accion_id = %s 
                ORDER BY ID_Cotizacion DESC LIMIT 1
            """
            cursor.execute(query, (id_accion,))
            resultado = cursor.fetchone()
            if resultado:
                return resultado[0]
            else:
                return None  
        except Exception as e:
            print(f"Error al obtener cotización: {e}")
        finally:
            cursor.close()

    def obtener_cantidad_disponible(self, id_accion):
        conn = self.db_conn.connect_to_mysql()
        try:
            cursor = conn.cursor()
            query = """
                SELECT cantidad_acciones_mercado
                FROM cotizacion
                WHERE accion_id = %s
            """
            cursor.execute(query, (id_accion,))
            resultado = cursor.fetchone()
            if resultado:
                return resultado[0]  # Retorna la cantidad de acciones disponibles
            else:
                return None  
        except Exception as e:
            print(f"Error al obtener cotización: {e}")
        finally:
            cursor.close()


    def actualizar_cantidad_disponible(self, cantidad, id_accion, id_operacion):

        conn = self.db_conn.connect_to_mysql()
        try:
            cursor = conn.cursor()

            if id_operacion == 1:
                # Si es una compra, se resta la cantidad de acciones del mercado
                query = """
                    UPDATE Cotizacion
                    SET cantidad_acciones_mercado = cantidad_acciones_mercado - %s
                    WHERE accion_id = %s
                """
            elif id_operacion == 2:
                # Si es una venta, se suma la cantidad de acciones al mercado
                query = """
                    UPDATE Cotizacion
                    SET cantidad_acciones_mercado = cantidad_acciones_mercado + %s
                    WHERE accion_id = %s
                """
            else:
                raise ValueError("Tipo de operación no válido. Debe ser '1: Compra' o '2: Venta'.")

            cursor.execute(query, (cantidad, id_accion))
            conn.commit()

        except Exception as e:
            print(f"Error al actualizar cantidad: {e}")
        finally:
            cursor.close()
        