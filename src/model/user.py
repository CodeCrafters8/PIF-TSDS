class User:
    def __init__(self, id_usuario, nombre, apellido, email, contrasena, cuil, saldo_inicial, id_perfil_inversor):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.contrasena = contrasena
        self.cuil = cuil
        self.saldo_inicial = saldo_inicial
        self.id_perfil_inversor = id_perfil_inversor

    def __str__(self):
        return f"Usuario({self.id_usuario}, {self.nombre}, {self.apellido}, {self.email}, {self.cuil}, {self.saldo_inicial})"