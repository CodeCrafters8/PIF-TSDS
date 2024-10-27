from DAO.user_dao_imp import UserDAOImpl  
from DAO.accion_dao_imp import AccionDAOImpl  
from DAO.transaccion_dao_imp import TransaccionDAOImp  
from DAO.cotizacion_dao_imp import CotizacionDAOImp  
from service.transacion_service import TransaccionService
from database.data_base_conection import DBConn

def main():
    # Conexión a la base de datos
    db_conn = DBConn()
    db_conn.connect_to_mysql()

    try:
        # Inicializar los DAOs
        user_dao = UserDAOImpl(db_conn)
        accion_dao = AccionDAOImpl(db_conn)
        transaccion_dao = TransaccionDAOImp(db_conn)
        cotizacion_dao = CotizacionDAOImp(db_conn)

        # Crear la instancia del servicio de transacciones
        transaccion_service = TransaccionService(transaccion_dao, user_dao, cotizacion_dao)

        # Definir el usuario que realizará la compra (suponiendo que el id_inversor es 1)
        user = user_dao.obtener_por_id(1) 

        # Definir la acción que se comprará (suponiendo que el id_accion es 1)
        accion = accion_dao.obtener_accion(1) 

        # Especificar la cantidad de acciones a comprar
        cantidad_a_vender = 5

        # Intentar comprar la acción
        if transaccion_service.vender_accion(user, accion, cantidad_a_vender):
            print(f"Venta exitosa: {cantidad_a_vender} acciones de {accion.ticker}")
        else:
            print("Error al realizar la compra.")
    
    except Exception as e:
        print(f"Ocurrió un error: {e}")


if __name__ == "__main__":
    main()
