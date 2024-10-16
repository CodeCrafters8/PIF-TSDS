import os
import configparser
import mysql.connector

class ConexionDB:
    def __init__(self):
        self.config = self.leer_configuracion()
        self.conexion = None
        self.cursor = None

    def leer_configuracion(self, archivo_config="config.ini"):
        ruta_actual = os.path.dirname(__file__)
        ruta_config = os.path.join(ruta_actual, archivo_config)

        config = configparser.ConfigParser()
        config.read(ruta_config)

        return config['mysql']

    def conectar(self):
        try:
            self.conexion = mysql.connector.connect(**self.config)
            self.cursor = self.conexion.cursor()
            print("Conexión a la base de datos establecida.")
            return self.conexion
        except mysql.connector.Error as error:
            print(f"Error al conectar a la base de datos: {error}")
            return None

    def cerrar_conexion(self):
        if self.conexion:
            self.cursor.close()
            self.conexion.close()
            print("Conexión a la base de datos cerrada.")

#Ejemplo de uso:
if __name__ == "__main__":
    db = ConexionDB()
    conexion = db.conectar()
    if conexion:
        cursor = conexion.cursor()
        # Modificar la consulta según la nueva tabla Usuario
        cursor.execute("SELECT * FROM Usuario")
        resultados = cursor.fetchall()
        for fila in resultados:
            print(fila)
        db.cerrar_conexion()
    else:
        print("Error al establecer la conexión")