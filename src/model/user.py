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

    def verificar_contraseña(self, contraseña_proporcionada: str) -> bool:
        return self.contraseña == contraseña_proporcionada
