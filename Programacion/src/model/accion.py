class Accion:
    def __init__(self, id_accion, ticker, nombre, empresa_id):
        self.id_accion = id_accion
        self.ticker = ticker
        self.nombre = nombre
        self.empresa_id = empresa_id

    def __repr__(self):
        return f"Accion(id_accion={self.id_accion}, ticker='{self.ticker}', nombre='{self.nombre}', empresa_id={self.empresa_id})"

class AccionConTenencia:
    def __init__(self, accion:Accion, cantidad_tenencia):
        self.accion = accion
        self.cantidad_tenencia = cantidad_tenencia

    def __repr__(self):
        return f"AccionConTenencia(accion={self.accion}, cantidad_tenencia={self.cantidad_tenencia})"
