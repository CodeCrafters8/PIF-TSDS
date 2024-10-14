import mysql.connector

class Conexionbd:
    def __init__(self):
        """Inicializa la clase de conexión a MySQL sin una conexión activa."""
        self.conexion = None
        self.cursor = None

    def ConexionBaseDeDatos(self, user, password):
        """
        Conecta a MySQL y crea la base de datos 'Broker_ISPC_cba' si no existe.

        :param user: Nombre de usuario para la conexión a MySQL.
        :param password: Contraseña para la conexión a MySQL.
        """
        try:
            # Conexión a MySQL sin especificar la base de datos
            self.conexion = mysql.connector.connect(
                user=user,
                password=password,
                host='localhost',
                port='3306'
            )
            
            if self.conexion.is_connected():
                print("¡Conectado exitosamente a MySQL!")

                # Crear la base de datos si no existe
                self.cursor = self.conexion.cursor()
                self.cursor.execute("CREATE DATABASE IF NOT EXISTS Broker_ISPC_cba;")
                print("Base de datos 'Broker_ISPC_cba' creada o ya existe.")

                # Conectar a la base de datos específica
                self.conexion.database = 'Broker_ISPC_cba'  # Selecciona la base de datos
                print("Conectado a la base de datos 'Broker_ISPC_cba'.")

        except mysql.connector.Error as e:
            print(f"Error al conectar con MySQL: {e}")

    def cerrar_conexion(self):
        """
        Cierra el cursor y la conexión a la base de datos, si están abiertas.
        """
        if self.cursor:
            self.cursor.close()  # Cierra el cursor
        if self.conexion and self.conexion.is_connected():
            self.conexion.close()  # Cierra la conexión
            print("Conexión cerrada.")


# # Ejemplo de uso
# if __name__ == "__main__":
#     conexion = Conexionbd()
    
#     # Aquí se pasan el usuario y la contraseña como argumentos
#     conexion.ConexionBaseDeDatos(user='root', password='admin')  # Llama al método para crear la base de datos

#     # Cierra la conexión cuando termines
#     conexion.cerrar_conexion()
