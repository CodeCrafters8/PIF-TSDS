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
        if self.conexion is None:
            try:
                self.conexion = mysql.connector.connect(**self.config)
                self.cursor = self.conexion.cursor()
                print("Conexión a la base de datos establecida.")
            except mysql.connector.Error as error:
                print(f"Error al conectar a la base de datos: {error}")
                return None
        return self.conexion

    def ejecutar_query(self, query, params=None):
        self.conectar()
        try:
            self.cursor.execute(query, params)
            self.conexion.commit()
            return self.cursor
        except mysql.connector.Error as error:
            print(f"Error al ejecutar la consulta: {error}")
            return None

    def cerrar_conexion(self):
        if self.conexion:
            self.cursor.close()
            self.conexion.close()
            self.conexion = None
            print("Conexión a la base de datos cerrada.")

# Ejemplo de uso:
if __name__ == "__main__":
    db = ConexionDB()
    conexion = db.conectar()
    
    if conexion:
        # Modificar la consulta según la nueva tabla Usuario
        cursor = db.ejecutar_query("SELECT * FROM Usuario")
        resultados = cursor.fetchall()
        
        for fila in resultados:
            print(fila)

    db.cerrar_conexion()