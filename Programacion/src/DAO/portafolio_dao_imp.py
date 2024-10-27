from DAO.portafolio_dao import PortafolioDAO
from database.data_base_conection import DBConn
from model.portafolio import Portafolio
from model.user import User
from model.accion import Accion, AccionConTenencia
from mysql.connector import Error
from DAO.logger_config import configurar_logger
import logging

configurar_logger()

class PortafolioDAOImpl(PortafolioDAO):
    def __init__(self, db: DBConn):
        self.db = db

    def obtener_portafolio_id_por_inversor(self, id_inversor):
        try:
            with self.db.connect_to_mysql() as conexion:
                cursor = conexion.cursor()
                
                # Consulta para obtener el id_portafolio del inversor
                cursor.execute("""
                    SELECT id_portafolio 
                    FROM portafolio 
                    WHERE id_inversor = %s
                """, (id_inversor,))
                
                # Obtener el resultado de la consulta
                portafolio_id_result = cursor.fetchone()
                
                if portafolio_id_result:
                    return portafolio_id_result[0]  # Retorna el id_portafolio
                else:
                    logging.error(f"No se encontró el portafolio para el id_inversor: {id_inversor}")
                    return None  # Retorna None si no se encuentra el portafolio

        except Error as e:
            logging.error(f"Error SQL al obtener el id_portafolio: {e}")
            return None
        except Exception as e:
            logging.error(f"Error inesperado al obtener el id_portafolio: {e}")
            return None
    
    def obtener_portafolio_por_id_inversor(self, id_inversor):
        try:
            with self.db.connect_to_mysql() as conexion:
                cursor = conexion.cursor()
                
                # Obtener información del usuario y total invertido
                cursor.execute("""
                    SELECT u.id_inversor, u.nombre, u.apellido, u.email, u.saldo_pesos, u.perfil_inversor_id, p.total_invertido
                    FROM inversor u
                    LEFT JOIN portafolio p ON u.id_inversor = p.id_inversor
                    WHERE u.id_inversor = %s
                """, (id_inversor,))
                
                resultado = cursor.fetchone()

                if resultado:
                    user = User(
                        id_inversor=resultado[0], 
                        nombre=resultado[1],
                        apellido=resultado[2],
                        email=resultado[3],
                        saldo_pesos=resultado[4],
                        perfil_inversor_id=resultado[5],
                        cuil='',  # Manejar según corresponda
                        contraseña=''  # Manejar según corresponda
                    )
                    
                    # Obtener acciones del portafolio
                    cursor.execute("""
                        SELECT pa.accion_id, pa.cantidad_tenencia, a.ticker, a.nombre, a.empresa_id
                        FROM portafolio_acciones pa
                        JOIN acciones a ON pa.accion_id = a.id_accion
                        WHERE pa.portafolio_id = (SELECT id_portafolio FROM portafolio WHERE id_inversor = %s)
                    """, (id_inversor,))

                    acciones = []
                    for row in cursor.fetchall():
                        # Crear objeto Accion
                        accion = Accion(
                            id_accion=row[0],
                            ticker=row[2],
                            nombre=row[3],
                            empresa_id=row[4],
                        )
                        # Añadir la acción con su cantidad en tenencia a la lista
                        acciones.append(AccionConTenencia(accion, row[1]))  

                    # Crear el portafolio con el usuario y sus acciones fuera del bucle
                    portafolio = Portafolio(user=user, acciones=acciones)
                    return portafolio
                else:
                    logging.error(f"No se encontró el portafolio para el id_inversor: {id_inversor}")
                    return None

        except Error as e:
            logging.error(f"Error SQL al obtener portafolio: {e}")
        except Exception as e:
            logging.error(f"Error inesperado al obtener portafolio: {e}")

    def existe_accion_en_portafolio(self, portafolio_id: int, accion_id: int):
        try:
            with self.db.connect_to_mysql() as conexion:
                with conexion.cursor() as cursor:
                    cursor.execute("""
                        SELECT COUNT(*) FROM portafolio_acciones
                        WHERE portafolio_id = %s AND accion_id = %s
                    """, (portafolio_id, accion_id))
                    resultado = cursor.fetchone()
                    return resultado[0] > 0  # Devuelve True si existe
        except Error as e:
            logging.error(f"Error SQL al verificar acción en el portafolio: {e}")
            return False
        except Exception as e: 
            logging.error(f"Error inesperado al verificar acción en el portafolio: {e}")
            return False

    def obtener_cantidad_tenencia(self, portafolio_id: int, accion_id: int) -> int:
        try:
            with self.db.connect_to_mysql() as conexion:
                with conexion.cursor() as cursor:
                    cursor.execute("""
                        SELECT cantidad_tenencia FROM portafolio_acciones
                        WHERE portafolio_id = %s AND accion_id = %s
                    """, (portafolio_id, accion_id))
                    resultado = cursor.fetchone()
                    return resultado[0] if resultado else 0  # Devuelve la cantidad o 0 si no existe
        except Error as e:
            logging.error(f"Error SQL al obtener cantidad en el portafolio: {e}")
            return 0
        except Exception as e: 
            logging.error(f"Error inesperado al obtener cantidad en el portafolio: {e}")
            return 0

    def agregar_accion(self, portafolio_id: int, accion_id: int, cantidad: int) -> None:
        try:
            with self.db.connect_to_mysql() as conexion:
                with conexion.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO portafolio_acciones (portafolio_id, accion_id, cantidad_tenencia)
                        VALUES (%s, %s, %s)
                    """, (portafolio_id, accion_id, cantidad))
                    conexion.commit()
        except Error as e:
            logging.error(f"Error SQL al agregar acción al Portafolio: {e}")
        except Exception as e: 
            logging.error(f"Error inesperado al agregar acción al Portafolio: {e}")

    def eliminar_accion(self, portafolio_id: int, id_accion: int) -> None:
        try:
            with self.db.connect_to_mysql() as conexion:
                with conexion.cursor() as cursor:
                    cursor.execute("""
                        DELETE FROM portafolio_acciones
                        WHERE portafolio_id = %s AND accion_id = %s
                    """, (portafolio_id, id_accion))
                    conexion.commit()
        except Error as e:
            logging.error(f"Error SQL al eliminar acción del Portafolio: {e}") 
        except Exception as e:    
            logging.error(f"Error inesperado al eliminar acción del Portafolio: {e}")

    def actualizar_accion(self, portafolio_id: int, id_accion: int, nueva_cantidad: int) -> None:
        try:
            with self.db.connect_to_mysql() as conexion:
                with conexion.cursor() as cursor:
                    cursor.execute("""
                        UPDATE portafolio_acciones
                        SET cantidad_tenencia = %s
                        WHERE portafolio_id = %s AND accion_id = %s
                    """, (nueva_cantidad, portafolio_id, id_accion))
                    conexion.commit()
        except Error as e:
            logging.error(f"Error SQL al actualizar acción en el portafolio: {e}")
        except Exception as e: 
            logging.error(f"Error inesperado al actualizar acción en el portafolio: {e}")

    def obtener_cotizaciones(self) -> dict:
        try:
            with self.db.connect_to_mysql() as conexion:
                with conexion.cursor() as cursor:
                    sql = "SELECT ticker, precio_venta_actual, precio_compra_actual FROM cotizacion"
                    cursor.execute(sql)
                    cotizaciones = cursor.fetchall()
                    return {row[0]: {'precio_venta_actual': row[1],
                                    'precio_compra_actual': row[2]}
                            for row in cotizaciones}
        except Exception as e:
            logging.error(f'Error al obtener cotizaciones: {e}')
