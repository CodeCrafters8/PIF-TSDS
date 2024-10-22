class Accion:
    def __init__(self, id_accion, simbolo, id_empresa):
        self.id_accion = id_accion
        self.simbolo = simbolo
        self.id_empresa = id_empresa

    def __repr__(self):
        return f"Accion(id_accion={self.id_accion}, simbolo='{self.simbolo}', id_empresa={self.id_empresa})"