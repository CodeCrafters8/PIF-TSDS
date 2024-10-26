# from DAO.portafolio_dao_imp import PortafolioDAOImp
# from database.data_base_conection import DBConn

# def mostrar_menu():
#     print("==== Menú de Gestión de Portafolio ====")
#     print("1. Ver Portafolio")
#     print("2. Agregar Acción al Portafolio")
#     print("3. Actualizar Acción en el Portafolio")
#     print("4. Eliminar Acción del Portafolio")
#     print("5. Ver Cotizaciones")
#     print("0. Salir")

# def obtener_input_int(mensaje):
#     try:
#         return int(input(mensaje))
#     except ValueError:
#         print("Error: Por favor ingresa un número válido.")
#         return obtener_input_int(mensaje)

# def main():
#     db = DBConn()  # Instancia de conexión a la base de datos
#     portafolio_dao = PortafolioDAOImp(db)  # Instancia de PortafolioDAOImp

#     while True:
#         mostrar_menu()
#         opcion = obtener_input_int("Selecciona una opción: ")

#         if opcion == 1:
#             # Ver Portafolio
#             user_id = obtener_input_int("Ingresa el ID del usuario: ")
#             portafolio = portafolio_dao.obtener_portafolio(user_id)
#             if portafolio:
#                 print(f"Portafolio del Usuario {user_id}:")
#                 print(f"Total invertido: {portafolio.total_invertido}")
#                 print(f"Saldo en pesos: {portafolio.saldo_pesos}")
#                 print("Acciones en el Portafolio:")
#                 for accion, cantidad in portafolio.acciones.items():
#                     print(f"{accion.ticker}: {cantidad}")
#             else:
#                 print("No se encontró portafolio para este usuario.")
        
#         elif opcion == 2:
#             # Agregar Acción al Portafolio
#             portafolio_id = obtener_input_int("Ingresa el ID del portafolio: ")
#             accion_id = obtener_input_int("Ingresa el ID de la acción: ")
#             cantidad = obtener_input_int("Ingresa la cantidad de la acción: ")
#             portafolio_dao.agregar_accion(portafolio_id, accion_id, cantidad)
#             print("Acción agregada con éxito.")
        
#         elif opcion == 3:
#             # Actualizar Acción en el Portafolio
#             portafolio_id = obtener_input_int("Ingresa el ID del portafolio: ")
#             accion_id = obtener_input_int("Ingresa el ID de la acción a actualizar: ")
#             nueva_cantidad = obtener_input_int("Ingresa la nueva cantidad de la acción: ")
#             portafolio_dao.actualizar_accion(portafolio_id, accion_id, nueva_cantidad)
#             print("Acción actualizada con éxito.")
        
#         elif opcion == 4:
#             # Eliminar Acción del Portafolio
#             portafolio_id = obtener_input_int("Ingresa el ID del portafolio: ")
#             accion_id = obtener_input_int("Ingresa el ID de la acción a eliminar: ")
#             portafolio_dao.eliminar_accion(portafolio_id, accion_id)
#             print("Acción eliminada con éxito.")
        
#         elif opcion == 5:
#             # Ver Cotizaciones
#             cotizaciones = portafolio_dao.obtener_cotizaciones()
#             print("Cotizaciones actuales:")
#             for ticker, precios in cotizaciones.items():
#                 print(f"{ticker} - Precio Venta: {precios['precio_venta_actual']}, Precio Compra: {precios['precio_compra_actual']}")
        
#         elif opcion == 0:
#             print("Saliendo del programa...")
#             break
        
#         else:
#             print("Opción no válida. Por favor, selecciona una opción correcta.")

# if __name__ == "__main__":
#     main()
# menu.py

from database.data_base_conection import DBConn
from DAO.user_dao_imp import UserDAOImp
from DAO.portafolio_dao_imp import PortafolioDAOImp

def mostrar_menu():
    print("\n--- Menú del Broker ---")
    print("1. Ver Portafolio")
    print("2. Comprar Acciones")
    print("3. Vender Acciones")
    print("4. Ver Saldo")
    print("5. Salir")

def ver_portafolio(usuario_id, portafolio_dao):
    acciones = portafolio_dao.obtener_acciones_por_usuario(usuario_id)
    if acciones:
        print("\n--- Portafolio ---")
        print(f"{'Ticker':<10} {'Empresa':<20} {'Cantidad':<10} {'Precio Compra':<15} {'Precio Venta':<15} {'Rendimiento':<15}")
        for accion in acciones:
            # Suponiendo que tienes acceso a la cotización actual, puedes agregarla aquí.
            # Simulación de precios actuales
            precio_actual_compra = 100  # Simulación
            precio_actual_venta = 105  # Simulación
            
            rendimiento = (precio_actual_venta - accion['precio_compra']) * accion['cantidad']
            print(f"{accion['ticker']:<10} {accion['empresa']:<20} {accion['cantidad']:<10} {accion['precio_compra']:<15} {precio_actual_venta:<15} {rendimiento:<15}")

    else:
        print("No tienes acciones en tu portafolio.")

def comprar_acciones(usuario_id, usuario_dao, portafolio_dao):
    ticker = input("Ingrese el ticker de la acción: ")
    cantidad = int(input("Ingrese la cantidad de acciones a comprar: "))
    precio_compra = float(input("Ingrese el precio de compra por acción: "))

    # Actualizar el saldo del usuario
    usuario = usuario_dao.obtener_usuario_por_id(usuario_id)
    nuevo_saldo = usuario['saldo'] - (cantidad * precio_compra)

    if nuevo_saldo < 0:
        print("No tienes suficiente saldo para realizar esta compra.")
        return

    usuario_dao.actualizar_saldo(usuario_id, nuevo_saldo)
    portafolio_dao.agregar_o_actualizar_accion(usuario_id, ticker, cantidad, precio_compra)
    print("Compra realizada con éxito.")

def vender_acciones(usuario_id, portafolio_dao, usuario_dao):
    ticker = input("Ingrese el ticker de la acción: ")
    cantidad = int(input("Ingrese la cantidad de acciones a vender: "))
    
    # Verificar si el usuario tiene suficientes acciones
    acciones = portafolio_dao.obtener_acciones_por_usuario(usuario_id)
    accion_en_portafolio = next((a for a in acciones if a['ticker'] == ticker), None)

    if not accion_en_portafolio or accion_en_portafolio['cantidad'] < cantidad:
        print("No tienes suficientes acciones para vender.")
        return

    # Suponiendo un precio de venta simulado
    precio_venta = 110  # Simulación
    ganancia = cantidad * precio_venta

    portafolio_dao.reducir_o_eliminar_accion(usuario_id, ticker, cantidad)
    usuario = usuario_dao.obtener_usuario_por_id(usuario_id)
    nuevo_saldo = usuario['saldo'] + ganancia
    usuario_dao.actualizar_saldo(usuario_id, nuevo_saldo)

    print("Venta realizada con éxito.")

def ver_saldo(usuario_id, usuario_dao):
    usuario = usuario_dao.obtener_usuario_por_id(usuario_id)
    print(f"Tu saldo actual es: {usuario['saldo']}")

def main():
    db_connection = DBConn().connect_to_mysql()
    usuario_dao = UserDAOImp(db_connection)
    portafolio_dao = PortafolioDAOImp(db_connection)

    usuario_id = 1  # Aquí deberías obtener el ID del usuario que ha iniciado sesión
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            ver_portafolio(usuario_id, portafolio_dao)
        elif opcion == '2':
            comprar_acciones(usuario_id, usuario_dao, portafolio_dao)
        elif opcion == '3':
            vender_acciones(usuario_id, portafolio_dao, usuario_dao)
        elif opcion == '4':
            ver_saldo(usuario_id, usuario_dao)
        elif opcion == '5':
            print("Saliendo del menú...")
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

if __name__ == "__main__":
    db_connection = DBConn().connect()
    main()
