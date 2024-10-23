from model.transaccion import Transaccion
from DAO.transaccion_dao import TransaccionDAO
from database.data_base_conection import DBConn

class TransaccionDAOImp(TransaccionDAO):
    def __init__(self, db_conn: DBConn):
        self._conexion_db = db_conn

    def crear(self, transaccion: Transaccion):
        conn = self._conexion_db.connect_to_mysql()
        if conn is None:
            raise Exception("No se pudo establecer la conexión a la base de datos.")

        consulta = """INSERT INTO Operacion
                    (fecha, precio_operado, cantidad_operada, cotizacion_id, tipo_operacion_id, 
                     inversor_id, comision, id_accion) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        
        valores = (transaccion.fecha, transaccion.precio_operado, transaccion.cantidad_operada, 
                   transaccion.cotizacion_id, transaccion.tipo_operacion_id, 
                   transaccion.inversor_id, transaccion.comision, transaccion.id_accion)
        
        cursor = conn.cursor()
        try:
            cursor.execute(consulta, valores)
            conn.commit()
            print("Transacción creada exitosamente.")
        except Exception as e:
            print(f"Error al crear la transacción: {e}")
        finally:
            cursor.close()
         

    def consultar(self, id_operacion: int) -> Transaccion:
        conn = self._conexion_db.connect_to_mysql()
        if conn is None:
            raise Exception("No se pudo establecer la conexión a la base de datos.")

        consulta = "SELECT * FROM Operacion WHERE id_operacion = %s"
        cursor = conn.cursor()
        try:
            cursor.execute(consulta, (id_operacion,))
            resultado = cursor.fetchone()
            if resultado:
                return Transaccion(*resultado)
        except Exception as e:
            print(f"Error al obtener la transacción: {e}")
        finally:
            cursor.close()
       

    def consultar_por_inversor(self, inversor_id: int) -> list[Transaccion]:
        conn = self._conexion_db.connect_to_mysql()
        if conn is None:
            raise Exception("No se pudo establecer la conexión a la base de datos.")

        consulta = "SELECT * FROM Operacion WHERE inversor_id = %s"
        cursor = conn.cursor()
        try:
            cursor.execute(consulta, (inversor_id,))
            resultados = cursor.fetchall()
            return [Transaccion(*resultado) for resultado in resultados]
        except Exception as e:
            print(f"Error al obtener transacciones del inversor: {e}")
        finally:
            cursor.close()
          
    def actualizar(self, transaccion: Transaccion):
        conn = self._conexion_db.connect_to_mysql()
        if conn is None:
            raise Exception("No se pudo establecer la conexión a la base de datos.")

        consulta = """UPDATE Operacion 
                      SET fecha = %s, precio_operado = %s, cantidad_operada = %s, 
                          cotizacion_id = %s, tipo_operacion_id = %s, 
                          comision = %s, id_accion = %s 
                      WHERE id_operacion = %s"""
        valores = (transaccion.fecha, transaccion.precio_operado, transaccion.cantidad_operada, 
                   transaccion.cotizacion_id, transaccion.tipo_operacion_id, 
                   transaccion.comision, transaccion.id_accion, transaccion.id_operacion)
        
        cursor = conn.cursor()
        try:
            cursor.execute(consulta, valores)
            conn.commit()
            print("Transacción actualizada exitosamente.")
        except Exception as e:
            print(f"Error al actualizar la transacción: {e}")
        finally:
            cursor.close()
          

    def eliminar(self, id_operacion: int):
        conn = self._conexion_db.connect_to_mysql()
        if conn is None:
            raise Exception("No se pudo establecer la conexión a la base de datos.")

        consulta = "DELETE FROM Operacion WHERE id_operacion = %s"
        cursor = conn.cursor()
        try:
            cursor.execute(consulta, (id_operacion,))
            conn.commit()
            print("Transacción eliminada exitosamente.")
        except Exception as e:
            print(f"Error al eliminar la transacción: {e}")
        finally:
            cursor.close()
         
