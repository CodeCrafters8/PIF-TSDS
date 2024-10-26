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
