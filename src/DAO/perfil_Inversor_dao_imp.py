from DAO.perfil_Inversor_dao import PerfilInversorDAO
from database.data_base_conection import ConexionDB
from model.perfil_Inversor import PerfilInversor

class PerfilInversorDAOImpl(PerfilInversorDAO):
    def __init__(self, db: ConexionDB):
        self.db = db

        
    def obtener_perfil(self, tipo_perfil: str):
       conexion = self.db.conectar()
       try:
           cursor = conexion.cursor()
           cursor.execute("SELECT IdPerfilInversor FROM PerfilInversor WHERE TipoPerfil = %s", (tipo_perfil,))
           resultado = cursor.fetchone()
           if resultado:
               return resultado[0]  # Retorna el Id
           return None
       except Exception as e:
           print(f"Error al obtener perfil: {e}")
           return None
       finally:
           self.db.cerrar_conexion()