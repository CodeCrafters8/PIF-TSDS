<<<<<<< HEAD
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

# # Ejemplo de uso:
# if __name__ == "__main__":
#     db = ConexionDB()
#     conexion = db.conectar()
#     if conexion:
#         cursor = conexion.cursor()
#         cursor.execute("SELECT * FROM inversor")
#         resultados = cursor.fetchall()
#         print(resultados)
#         db.cerrar_conexion()
#     else:
#         print("Error al establecer la conexión")
=======
import mysql.connector
from mysql.connector import errorcode
import configparser
import pathlib


class DBConn:
    def __init__(self, config_file="config.ini"):
        self.config_file=config_file
        
        if (self.config_file!=""):
            # Crear una instancia de ConfigParser
            config=configparser.ConfigParser()
            # Configurar la ruta
            config_path = pathlib.Path(__file__).parent.absolute() /config_file
            
            # Leer el archivo
            config.read(config_path)
            
            # Definir una variable db_config que contiene los datos de la sección [database] del archivo.
            self.db_config=config['database']
        
    def get_data_base_name(self):
         return self.db_config.get('database')   
     
    
    def connect_to_mysql(self):
        # Conectar a una base de datos MySQL Server
        try:
            return mysql.connector.connect(
                user=self.db_config.get('user'),
                password=self.db_config.get('password'),
                host=self.db_config.get('host'),
                database=self.get_data_base_name()  # Agrega la base de datos aquí
                )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                raise Exception("Usuario o Password no válido")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                raise Exception("La base de datos no existe.")
            else:
                raise err         


       


>>>>>>> romina
