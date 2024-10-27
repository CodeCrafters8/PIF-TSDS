![Alt Text](../src/texto.png)


# Informe de Funcionalidades de Base de Datos

Este informe describe las funcionalidades y mecanismos de base de datos implementados en el sistema **ArgBroker**. El sistema se conecta a una base de datos **MySQL** y utiliza varias funciones para gestionar la seguridad, autenticación, y operaciones de inversión para los usuarios.

## 1. Conexión y Configuración de la Base de Datos
La conexión se establece a través de una instancia de `DBConn`, la cual representa el enlace entre la aplicación y la base de datos **MySQL**. Esta instancia permite ejecutar consultas SQL y manejar transacciones, asegurando así la persistencia de los datos y la integridad en cada operación.

## 2. Registro y Autenticación de Usuarios
- **Función `encriptar_contraseña`**: Se utiliza para encriptar las contraseñas antes de guardarlas en la base de datos, empleando la librería `bcrypt`. Este método convierte la contraseña en texto cifrado, protegiendo la información sensible del usuario.
- **Función `verificar_contraseña`**: Compara la contraseña ingresada con la versión encriptada almacenada en la base de datos, validando que el usuario es quien dice ser.
- **Proceso de Registro**: Durante el registro, los datos del usuario (nombre, apellido, email, CUIL, contraseña encriptada, perfil de inversión) se envían a `registrar_inversor` de `UserService`. Este método ejecuta consultas SQL para insertar los datos en la base de datos de forma segura.
- **Inicio de Sesión**: La autenticación de usuario se realiza mediante el método `iniciar_sesion`, que compara el email y la contraseña encriptada contra los registros en la base de datos. Si la validación es exitosa, se retorna el ID del inversor.

## 3. Recuperación de Contraseña
La función `recuperar_contraseña` permite a los usuarios solicitar una nueva contraseña en caso de pérdida. Esta función verifica la identidad del usuario usando el email registrado y lanza un proceso de restablecimiento de contraseña, que potencialmente incluye el envío de un correo de restablecimiento, aunque este último detalle no se implementa en el código, por lo que se realiza una simulacion del mismo.

## 4. Gestión de Portafolio e Inversiones
- **Consulta de Saldo**: `obtener_saldo_usuario` en `PortafolioService` ejecuta una consulta SQL que recupera el saldo disponible del usuario en la base de datos.
- **Portafolio de Inversiones**: El sistema permite que los usuarios visualicen su portafolio, mostrando todas las acciones en posesión y los detalles asociados (nombre, ticker, cantidad, precio de compra). Las consultas SQL para esta funcionalidad están implementadas en `PortafolioDAOImpl` y `PortafolioService`.
- **Realización de Inversiones**: La compra y venta de acciones se gestionan a través de `TransaccionService`, el cual actualiza el saldo y el portafolio del usuario, realizando las siguientes acciones:
  - Reducción o incremento del saldo disponible del usuario.
  - Actualización de las acciones en el portafolio del usuario.

## 5. Visualización y Operación de Acciones Disponibles
La función `listar_acciones` en `AccionDAOImpl` muestra las acciones disponibles para su compra, permitiendo que el usuario elija entre una lista de acciones del **Merval**. La información se extrae de la base de datos y se presenta en una tabla con detalles como ID de la acción, ticker, nombre y empresa.

## Seguridad en la Base de Datos
- **Encriptación de Contraseñas**: La encriptación mediante `bcrypt` protege las contraseñas de los usuarios, manteniendo la seguridad de los datos sensibles.
- **Consultas Parametrizadas**: Todas las consultas SQL deberían ser parametrizadas para evitar inyecciones SQL; sin embargo, no se muestra explícitamente en el código proporcionado.
- **Integridad de Transacciones**: `TransaccionService` asegura la integridad de cada transacción de compra y venta, actualizando los saldos de los usuarios y las cantidades de acciones sin inconsistencias.

Este conjunto de funcionalidades garantiza que el sistema mantenga los datos de los usuarios seguros, proporcione acceso a sus inversiones de manera controlada y gestione cada transacción de forma confiable.