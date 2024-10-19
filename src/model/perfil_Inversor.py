class PerfilInversor:
    def __init__(self, id_perfil_inversor, tipo_inversor):
        self.id_perfil_inversor = id_perfil_inversor
        self.tipo_inversor = tipo_inversor

    def __str__(self):
        return f"PerfilInversor({self.id_perfil_inversor}, {self.tipo_inversor})"