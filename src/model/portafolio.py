from model.user import User
from model.accion import Accion

class Portafolio:
    def __init__(self, user: User, acciones: list = None):
        self.portafolio_id = 0  # O algún valor predeterminado
        self.user = user  # Guarda la instancia del objeto User
        self.total_invertido = 0.0  # Inicializa el total invertido
        self.saldo_pesos = user.saldo_pesos  # Obtiene el saldo del usuario
        self.acciones = acciones if acciones is not None else {}
    
    def obtener_cotizaciones(self):
        """Obtiene todas las cotizaciones de la base de datos usando el DAO."""
        return self.cotizacion_dao.obtener_cotizaciones()
