from datetime import date

class Transaccion:
    def __init__(self, id_operacion: int, fecha: date, precio_operado: float, 
                cantidad_operada: int, cotizacion_id: int, 
                tipo_operacion_id: int, inversor_id: int, 
                comision: int, id_accion: int):
        self.id_operacion = id_operacion  # INT AUTO_INCREMENT, puede ser None al crear
        self.fecha = fecha  # DATE NOT NULL
        self.precio_operado = precio_operado  # DECIMAL(10, 2) NOT NULL
        self.cantidad_operada = cantidad_operada  # INT NOT NULL
        self.cotizacion_id = cotizacion_id  # INT, puede ser None
        self.tipo_operacion_id = tipo_operacion_id  # INT, puede ser None
        self.inversor_id = inversor_id  # INT
        self.comision = comision  # INT
        self.id_accion = id_accion  # INT, para unir con la tabla acciones

    def __repr__(self):
        return (f"Transaccion(id_operacion={self.id_operacion}, fecha={self.fecha}, "
                f"precio_operado={self.precio_operado}, cantidad_operada={self.cantidad_operada}, "
                f"cotizacion_id={self.cotizacion_id}, tipo_operacion_id={self.tipo_operacion_id}, "
                f"inversor_id={self.inversor_id}, comision={self.comision}, id_accion={self.id_accion})")
