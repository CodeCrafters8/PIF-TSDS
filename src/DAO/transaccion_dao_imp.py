from model.transaccion import Transaccion
from DAO.transaccion_dao import TransaccionDAO
from database.data_base_conection import DBConn

class TransaccionDAOImp(TransaccionDAO):
    def __init__(self, db: DBConn):
        self.db = db

    def crear(self, transaccion: Transaccion):
        conn = self.db.connect_to_mysql()
        if conn is None:
            raise Exception("No se pudo establecer la conexión a la base de datos.")

        # Consulta para verificar que el inversor tiene un portafolio asociado
        verificar_portafolio = "SELECT id_portafolio FROM Portafolio WHERE id_inversor = %s"
        cursor = conn.cursor()
        
        try:
            # Verificar el portafolio del inversor
            cursor.execute(verificar_portafolio, (transaccion.inversor_id,))
            resultado = cursor.fetchone()
            if not resultado:
                raise Exception(f"No se encontró un portafolio para el inversor con id {transaccion.inversor_id}")

            portafolio_id = resultado[0]

            # Crear la transacción en la tabla Operacion
            consulta = """INSERT INTO Operacion
                        (fecha, precio_operado, cantidad_operada, cotizacion_id, tipo_operacion_id, 
                        inversor_id, comision, id_accion) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            
            valores = (transaccion.fecha, transaccion.precio_operado, transaccion.cantidad_operada, 
                    transaccion.cotizacion_id, transaccion.tipo_operacion_id, 
                    transaccion.inversor_id, transaccion.comision, transaccion.id_accion)

            cursor.execute(consulta, valores)
            conn.commit()
            print("Transacción creada exitosamente.")

            # Actualizar el saldo en el portafolio (ejemplo)
            actualizar_total_operado = """UPDATE Portafolio 
                                            SET total_invertido = total_invertido + %s 
                                            WHERE id_portafolio = %s"""
            cursor.execute(actualizar_total_operado, (transaccion.precio_operado * transaccion.cantidad_operada, portafolio_id))
            conn.commit()
            print("Total Operado Actualizado")

            
        except Exception as e:
            conn.rollback()
            print(f"Error al crear la transacción o actualizar el portafolio: {e}")
        finally:
            cursor.close()

    def consultar(self, id_operacion: int) -> Transaccion:
        conn = self.db.connect_to_mysql()
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
        conn = self.db.connect_to_mysql()
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
        conn = self.db.connect_to_mysql()
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
        conn = self.db.connect_to_mysql()
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

    def obtener_transacciones_por_accion_y_inversor(self, id_inversor, id_accion):
        conn = self.db.connect_to_mysql()
        if conn is None:
            raise Exception("No se pudo establecer la conexión a la base de datos.")

        query = """
            SELECT id_operacion, fecha, precio_operado, cantidad_operada, cotizacion_id,
                tipo_operacion_id, inversor_id, comision, id_accion
            FROM operacion
            WHERE inversor_id = %s AND id_accion = %s AND tipo_operacion_id = 2
        """
        parametros = (id_inversor, id_accion)
        transacciones = []
        
        cursor = conn.cursor()
        try:
            cursor.execute(query, parametros)
            resultados = cursor.fetchall()

            for fila in resultados:
                transaccion = Transaccion(
                    id_operacion=fila[0],
                    fecha=fila[1],
                    precio_operado=fila[2],
                    cantidad_operada=fila[3],
                    cotizacion_id=fila[4],
                    tipo_operacion_id=fila[5],
                    inversor_id=fila[6],
                    comision=fila[7],
                    id_accion=fila[8]
                )
                transacciones.append(transaccion)
        except Exception as e:
            print(f"Error al obtener transacciones: {e}")
        finally:
            cursor.close()  # Cerrar el cursor
            conn.close()  # Cerrar la conexión

        return transacciones
