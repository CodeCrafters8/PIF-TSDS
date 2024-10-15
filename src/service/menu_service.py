from model.user import User
from model.portafolio import Portafolio

class Menu:
    def __init__(self, user: User):
        """Inicializa el menú con el usuario y su portafolio."""
        self.user = user
        self.portafolio = Portafolio(self.user.id_portafolio)  # Inicializa el portafolio

    def mostrar_menu(self):
        """Muestra el menú principal y gestiona las opciones del usuario."""
        while True:
            print("Menú Principal")
            print("1. Mostrar datos de la cuenta")
            print("2. Listar activos del portafolio")
            print("3. Realizar operaciones")
            print("4. Salir")

            opcion = input("Ingrese una opción: ")

            try:
                opcion = int(opcion)
                if opcion == 4:
                    print("Saliendo del sistema...")
                    break
                elif opcion == 1:
                    self.mostrar_datos_cuenta()  # Muestra los datos de la cuenta
                elif opcion == 2:
                    self.listar_activos()  # Lista los activos
                elif opcion == 3:
                    self.realizar_operaciones()  # Realiza operaciones
                else:
                    print("Opción inválida.")
            except ValueError:
                print("Por favor, ingrese un número válido.")

    def mostrar_datos_cuenta(self):
        """Muestra los detalles de la cuenta del usuario."""
        try:
            print(f"Saldo: ${self.portafolio.saldo}")
            print(f"Inversión total: ${self.portafolio.inversion_total}")
            print(f"Rendimiento total: {self.portafolio.rendimiento}%")
        except AttributeError:
            print("Error al obtener datos del portafolio.")

    def listar_activos(self):
        """Lógica para realizar listar activos del portafolio."""
        pass  # Implementar lógica según sea necesario


    def realizar_operaciones(self):
        """Lógica para realizar operaciones de compra/venta."""
        pass  # Implementar lógica según sea necesario

# # Ejemplo de uso:
# if __name__ == "__main__":
#     usuario = User()  # Crea una instancia de Usuario (debe estar inicializada adecuadamente)
#     menu = Menu(usuario)  # Pasa la instancia de Usuario al menú
#     menu.mostrar_menu()
