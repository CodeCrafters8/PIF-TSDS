import re

class user:
    def __init__(self, id: int, nombre: str, apellido: str, cuil: str, email: str, contraseña: str, saldo: float = 0.0, total_invertido: float = 0.0):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.cuil = cuil
        self.email = email
        self.contraseña = contraseña
        self.saldo = saldo
        self.total_invertido = total_invertido

    def __str__(self):
        return f"Inversor: {self.nombre} {self.apellido}, CUIT: {self.cuit}, Email: {self.email}, Saldo: {self.saldo_cuenta}, Total Invertido: {self.total_invertido}"
    
    def verificar_email(self):
        regrex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(regrex, self.email) is not None
    
    def verificar_contraseña(self, contraseña_proporcionada: str) -> bool:
        return self.contraseña == contraseña_proporcionada 