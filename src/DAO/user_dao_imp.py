import mysql.connector
from model.user import User
from user_dao import user_dao

class user_dao_imp(user_dao):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def get(self, id: int) -> User:
        try:
            cursor = self.db_conn.cursor()
            query = """
            SELECT id_inversor, cuit, nombre, apellido, email, contraseña, p.saldo_cuenta, p.total_invertido
            FROM inversor i
            JOIN portafolio p ON i.id_inversor = p.id_inversor
            WHERE i.id_inversor = %s
            """
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            if row:
                return User(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            return None
        finally:
            cursor.close()

    def get_by_email(self, email: str) -> User:
        try:
            cursor = self.db_conn.cursor()
            query = """
            SELECT id_inversor, cuit, nombre, apellido, email, contraseña, p.saldo_cuenta, p.total_invertido
            FROM inversor i
            JOIN portafolio p ON i.id_inversor = p.id_inversor
            WHERE i.email = %s
            """
            cursor.execute(query, (email,))
            row = cursor.fetchone()
            if row:
                return User(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            return None
        finally:
            cursor.close()

    def create(self, user: User):
        try:
            cursor = self.db_conn.cursor()
            query = """
            INSERT INTO inversor (cuit, nombre, apellido, email, contraseña)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (user.cuit, user.nombre, user.apellido, user.email, user.contraseña))
            self.db_conn.commit()

            # Después de crear el inversor, también se puede crear un portafolio
            portafolio_query = "INSERT INTO portafolio (saldo_cuenta, total_invertido, id_inversor) VALUES (0.00, 0.00, LAST_INSERT_ID())"
            cursor.execute(portafolio_query)
            self.db_conn.commit()
        finally:
            cursor.close()

    def update(self, user: User):
        try:
            cursor = self.db_conn.cursor()
            query = """
            UPDATE inversor
            SET cuit = %s, nombre = %s, apellido = %s, email = %s, contraseña = %s
            WHERE id_inversor = %s
            """
            cursor.execute(query, (user.cuit, user.nombre, user.apellido, user.email, user.contraseña, user.id))
            self.db_conn.commit()
        finally:
            cursor.close()

    def delete(self, id: int):
        try:
            cursor = self.db_conn.cursor()
            query = "DELETE FROM inversor WHERE id_inversor = %s"
            cursor.execute(query, (id,))
            self.db_conn.commit()
        finally:
            cursor.close()
