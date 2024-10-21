from DAO.portafolio_dao import PortafolioDAO
from database.data_base_conection import Conexionbd
from model.portafolio import Portafolio
from model.user import User
from model.stock import Stock
from mysql.connector import Error
from logger_config import configurar_logger
import logging

configurar_logger()

class PortafolioDAOImp(PortafolioDAO):
    def __init__(self, bd:Conexionbd):
        self.bd = bd
    
    def obtener_portafolio(self, user_id: int):
        portafolio = Portafolio()
        try:
            with self.db.conectar() as conexion:
                with conexion.cursor() as cursor:
                    cursor.execute("""
                        SELECT p.id_portafolio, p.saldo_cuenta, p.total_invertido, 
                               u.saldo_pesos, pa.accion_id, pa.cantidad_tenencia
                        FROM portafolio p
                        JOIN usuario u ON p.id_usuario = u.id_usuario
                        LEFT JOIN portafolio_acciones pa ON p.id_portafolio = pa.portafolio_id
                        WHERE p.id_usuario = %s
                    """, (user_id,))
                    resultados= cursor.fetchall()
                    for resultado in resultados:
                        portafolio.id_portafolio = resultado[0]
                        portafolio.saldo_cuenta = resultado[1]
                        portafolio.total_invertido = resultado[2]
                        portafolio.saldo_pesos = resultado[3]
                        portafolio.accion_id = resultado [4]
                        portafolio.cantidad_tenencia = resultado[5]
        except Error as e:
            logging.error(f"Error SQL al obtener el portafolio: {e}")
        except Exception as e:
            logging.error(f"Error inesperado al obtener el portafolio: {e}")
        return portafolio
    
    def agregar_accion(self, portafolio_id: int, stock_id: int, cantidad: int):
        try:
            with self.db.conectar() as conexion:
                with conexion.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO portafolio_acciones (portafolio_id, accion_id, cantidad_tenencia)
                        VALUES (%, %, %) 
                    """, (portafolio_id, stock_id, cantidad))
                    conexion.commit()
        except Error as e:
            logging.error(f"Error SQL al agregar accion al Portafolio: {e}")
        except Exception as e: 
            logging.error(f"Error inesperado al agergar acción al Portafolio: {e}")
    
    def eliminar_accion(self, portafolio_id: int, stock_id: int, cantidad: int):
        try:
            with self.db.conectar() as conexion:
                with conexion.cursor() as cursor:
                    cursor.execute("""
                        DELETE FROM portafolio_acciones
                        WHERE portafolio_id = %s AND accion_id = %s
                """, (portafolio_id, stock_id))
                conexion.commit()
        except Error as e:
            logging.error(f"Error SQL al eliminar accion del Portafolio: {e}") 
        except Error as e:    
            logging.error(f"Error inesperado al actualizar accion en el portafolio")      
    
    def actualizar_accion(self, portafolio_id: int, stock_id: int, nueva_cantidad: int):
        try:
            with self.db.conectar() as conexion:
                with conexion.cursor() as cursor:
                    cursor.execute("""
                        UPDATE portafolio_acciones
                        SET cantidad_tenencia = %s
                        WHERE portafolio_id %s AND accion_id = %s
                    """, (nueva_cantidad, portafolio_id, stock_id))
                    conexion.commit()
        except Error as e:
            logging.error(f"Eror SQL al actualizar accion en el portafolio: {e}")
        except Error as e: 
            logging.error(f"Error inesperado al actualizar accion en el portafolio: {e}")                 