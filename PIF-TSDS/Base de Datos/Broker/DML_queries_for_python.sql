
-- REGISTRAR NUEVO PERFIL DE INVERSOR
INSERT INTO perfil_inversor (tipo_inversor) VALUES (%s);

-- CREAR UN NUEVO PORTAFOLIO
INSERT INTO portafolio (saldo_cuenta, id_inversor) 
VALUES (%s, (SELECT id_inversor FROM inversor WHERE email = %s));

-- REGISTRAR NUEVO INVERSOR
INSERT INTO inversor (cuit, nombre, apellido, email, contraseña, perfil_inversor_id) 
VALUES (%s, %s, %s, %s, %s, %s);

-- VERIFICAR INICIO DE SESIÓN
SELECT inversor.id_inversor, inversor.nombre, inversor.apellido, portafolio.saldo_cuenta
FROM inversor
JOIN portafolio ON inversor.id_inversor = portafolio.id_inversor
WHERE inversor.email = %s AND inversor.contraseña = %s;


-- MOSTRAR SALDO Y TOTAL INVERTIDO
SELECT p.saldo_cuenta, 
       SUM(o.precio_operado * o.cantidad_operada) AS total_invertido, 
       (SUM(o.precio_operado * o.cantidad_operada) - p.saldo_cuenta) AS rendimiento_total
FROM portafolio p
JOIN operacion o ON p.id_inversor = o.inversor_id
WHERE p.id_inversor = %s;


-- LISTAR ACTIVOS EN EL PORTAFOLIO
SELECT a.nombre AS nombre_activo, 
       pa.cantidad_tenencia, 
       c.precio_compra_actual, 
       c.precio_venta_actual,
       (c.precio_compra_actual - 
       (SELECT precio_operado FROM operacion o WHERE o.cotizacion_id = c.id_cotizacion 
        AND o.inversor_id = p.id_inversor LIMIT 1)) AS rendimiento
FROM portafolio_acciones pa
JOIN acciones a ON pa.accion_id = a.id_accion
JOIN portafolio p ON pa.portafolio_id = p.id_portafolio
JOIN cotizacion c ON c.accion_id = a.id_accion
WHERE p.id_inversor = %s;

-- GUARDAR OPERACIONES DE COMPRA/VENTA
INSERT INTO operacion (fecha, hora, precio_operado, cantidad_operada, cotizacion_id, tipo_operacion_id, inversor_id) 
VALUES (CURDATE(), CURTIME(), %s, %s, %s, (SELECT id_tipo_operacion FROM tipo_operacion WHERE tipo = %s), %s);

-- ACTUALIZAR SALDO DESPÚES DE REALIZAR UNA COMPRA
UPDATE portafolio 
SET saldo_cuenta = saldo_cuenta - (%s * %s)
WHERE id_inversor = %s;

-- ACTUALIZAR PORTAFOLIO DESPÚES DE REALIZAR UNA COMPRA
UPDATE portafolio_acciones 
SET cantidad_tenencia = cantidad_tenencia + %s
WHERE portafolio_id = %s AND accion_id = %s;

-- VALIDAD EXISTENCIAS ANTES DE REALIZAR UNA COMPRA
SELECT cantidad_tenencia 
FROM portafolio_acciones 
WHERE portafolio_id = %s AND accion_id = %s;

-- OBTENER PRECIO DE COMPRA ACTUAL DE UNA ACCIÓN
SELECT precio_compra_actual
FROM cotizacion 
WHERE accion_id = %s;

-- OBTENER PRECIO DE VENTA ACTUAL DE UNA ACCIÓN
SELECT precio_venta_actual 
FROM cotizacion 
WHERE accion_id = %s;

-- REGISTRAR HISTORIAL DE OPERACIONES
INSERT INTO historial_operaciones (operacion_id, precio_operado, cantidad_operada, tipo_operacion_id) 
VALUES (%s, %s, %s, %s);
