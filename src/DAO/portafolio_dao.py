from abc import ABC, abstractmethod

class PortafolioDAO(ABC):
    @abstractmethod
    def obtener_portafolio_id_por_inversor(self, user_id: int):
        pass
    
    @abstractmethod 
    def agregar_accion(self, portafolio_id: int, stock_id: int, cantidad: int):
        pass
    
    @abstractmethod
    def eliminar_accion(self, portafolio_id: int, stock_id: int, cantidad: int):
        pass
    
    @abstractmethod 
    def actualizar_accion(self, portafolio_id : int, stock_id: int, nueva_cantidad: int):
        pass

    @abstractmethod
    def obtener_cotizaciones(self):
        pass

