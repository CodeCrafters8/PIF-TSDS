from database.data_base_conection import ConexionDB

db = ConexionDB()
if db.conectar:
    print("Conexión exitosa a la base de datos.")
else:
    print("No se pudo conectar a la base de datos.")