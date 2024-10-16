from DAO.user_dao_imp import UserDAOImpl
from DAO.perfil_Inversor_dao_imp import PerfilInversorDAOImpl
from model.user import User
from model.perfil_Inversor import PerfilInversor


if __name__ == "__main__":
    # Prueba con Usuario
    usuario_dao = UserDAOImpl()
    nuevo_usuario = User(None, "Juan", "Pérez", "juan.perez@gmail.com", "1234pass", "20123456789", 1000000.00, 1)
    usuario_dao.insertar_usuario(nuevo_usuario)

    usuarios = usuario_dao.obtener_todos()
    for usuario in usuarios:
        print(usuario)

    # Prueba con PerfilInversor
    perfil_inversor_dao = PerfilInversorDAOImpl()
    perfiles = perfil_inversor_dao.obtener_todos()
    for perfil in perfiles:
        print(perfil)