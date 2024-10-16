class PerfilInversor:
    def __init__(self, id_perfil_inversor, tipo_perfil):
        self.id_perfil_inversor = id_perfil_inversor
        self.tipo_perfil = tipo_perfil

    def __str__(self):
        return f"PerfilInversor({self.id_perfil_inversor}, {self.tipo_perfil})"