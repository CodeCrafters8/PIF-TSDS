import mysql.connector
from DAO.perfil_Inversor_dao import PerfilInversorDAO
from database.data_base_conection import DBConn
from model.perfil_inversor import PerfilInversor


class PerfilInversorDAOImpl(PerfilInversorDAO):
    def __init__(self, db_conn: DBConn):
        self.db_conn = db_conn

    def obtener_perfil(self, tipo_inversor):
        conn = self.db_conn.connect_to_mysql()
        with conn:
            try:
                cursor = conn.cursor()
                query = f"SELECT id_perfil_inversor FROM {self.db_conn.get_data_base_name()}.perfil_inversor WHERE tipo_inversor = %s"
                cursor.execute(query, (tipo_inversor,))
                resultado = cursor.fetchone()
                if resultado:
                    return resultado[0]  # Devuelve solo el id_perfil_inversor
                return None
            except mysql.connector.Error as err:
                raise err
