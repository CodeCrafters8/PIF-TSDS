class Transaccion:
    def __init__(self, id_operacion, fecha, hora, precio_operado, cantidad_operada, cotizacion_id,
                    tipo_operacion_id, inversor_id, accion_id, nombre_accion: None, precio_actual: None):
        self.id_operacion = id_operacion
        self.fecha = fecha
        self.hora = hora
        self.precio_operado = precio_operado
        self.cantidad_operada = cantidad_operada
        self.cotizacion_id = cotizacion_id
        self.tipo_operacion = tipo_operacion_id
        self.inversor_id = inversor_id
        self.accion_id = accion_id
        self.nombre_accion = nombre_accion
        self.precio_actual = precio_actual

    def __str__(self):
        tipo_operacion = self.get_tipo_operacion()
        return (f"Operación: {tipo_operacion}\n"
                f"Fecha: {self.fecha}, Hora: {self.hora}\n"
                f"Cantidad Operada: {self.cantidad_operada}\n"
                f"Acción: {self.nombre_accion}, Precio de Compra Actual: ${self.precio_compra_actual:.2f}")
    

    def get_tipo_operacion(self):
        """Método para obtener el tipo de operación como texto."""
        tipo_operacion_dict = {
            1: "Compra",
            2: "Venta"
        }
        return tipo_operacion_dict.get(self.tipo_operacion_id, "Desconocido")


    def calculate_total_value(self):
        """Calcular el valor total de la operación usando el precio actual de compra."""
        if self.precio_compra_actual is not None:
            return self.precio_compra_actual * self.cantidad_operada
        return None

    def validate(self):
        """Valida la operación."""
        return self.cantidad_operada > 0