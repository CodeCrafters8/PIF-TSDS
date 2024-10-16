# from DAO.user_dao_imp import UserDAOImpl
# from DAO.perfil_Inversor_dao_imp import PerfilInversorDAOImpl
# from model.user import User
# from model.perfil_Inversor import PerfilInversor


from service.user_service import UserService

def mostrar_menu():
    print("Bienvenido al sistema de Broker")
    print("1. Registrar nuevo inversor")
    print("2. Iniciar sesión")
    print("3. Recuperar contraseña")
    print("4. Salir")

def main():
    service = UserService()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Ingrese su nombre: ")
            apellido = input("Ingrese su apellido: ")
            cuil = input("Ingrese su CUIL: ")
            email = input("Ingrese su email: ")
            contrasena = input("Ingrese su contraseña: ")
            saldo_inicial = 1000000.00
            tipo_perfil = input("Ingrese tipo de perfil (conservador, medio, agresivo): ")

            if service.registrar_inversor(nombre, apellido, cuil, email, contrasena, saldo_inicial, tipo_perfil):
                print("Registro exitoso.")
            else:
                print("Error en el registro.")

        elif opcion == "2":
            email = input("Ingrese su email: ")
            contrasena = input("Ingrese su contraseña: ")
            service.iniciar_sesion(email, contrasena)

        elif opcion == "3":
            email = input("Ingrese su email: ")
            service.recuperar_contrasena(email)

        elif opcion == "4":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()