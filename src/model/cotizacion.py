class Cotizacion:
    def __init__(self, id_cotizacion, fecha, hora, accion_id, precio_apertura, minimo_diario, maximo_diario,
                precio_compra_actual, precio_venta_actual, ultimo_precio_cierre,
                cantidad_compra_diaria, cantidad_venta_diaria):
        self.id_cotizacion = id_cotizacion
        self.fecha = fecha
        self.hora = hora
        self.accion_id = accion_id
        self.precio_apertura = precio_apertura
        self.minimo_diario = minimo_diario
        self.maximo_diario = maximo_diario
        self.precio_compra_actual = precio_compra_actual
        self.precio_venta_actual = precio_venta_actual
        self.ultimo_precio_cierre = ultimo_precio_cierre
        self.cantidad_compra_diaria = cantidad_compra_diaria
        self.cantidad_venta_diaria = cantidad_venta_diaria

    def __repr__(self):
        return (f"Cotizacion(id_cotizacion={self.id_cotizacion}, fecha='{self.fecha}', hora='{self.hora}', "
                f"accion_id={self.accion_id}, precio_apertura={self.precio_apertura}, "
                f"minimo_diario={self.minimo_diario}, maximo_diario={self.maximo_diario}, "
                f"precio_compra_actual={self.precio_compra_actual}, precio_venta_actual={self.precio_venta_actual}, "
                f"ultimo_precio_cierre={self.ultimo_precio_cierre}, "
                f"cantidad_compra_diaria={self.cantidad_compra_diaria}, cantidad_venta_diaria={self.cantidad_venta_diaria})")
