-- MOSTRAR PERFIL DE INVERSOR
SELECT * FROM perfil_inversor;

-- LISTAR TODOS LOS INVERSORES
SELECT * FROM inversor;

-- MOSTRAR SALDO Y TOTAL INVERTIDO DE UN INVERSOR
SELECT 
    p.saldo_cuenta, 
    SUM(o.precio_operado * o.cantidad_operada) AS total_invertido, 
    (SUM(o.precio_operado * o.cantidad_operada) - p.saldo_cuenta) AS rendimiento_total
FROM 
    portafolio p
JOIN 
    operacion o ON p.id_inversor = o.inversor_id
WHERE 
    p.id_inversor = (SELECT id_inversor FROM inversor WHERE email = 'juan.perez@example.com') -- Cambiar email según el inversor
GROUP BY 
    p.saldo_cuenta;

-- LISTAR ACTIVOS EN EL PORTAFOLIO DE UN INVERSOR
SELECT 
    a.nombre AS nombre_activo, 
    pa.cantidad_tenencia, 
    c.precio_compra_actual, 
    c.precio_venta_actual,
    (c.precio_compra_actual - 
    (SELECT precio_operado FROM operacion o WHERE o.cotizacion_id = c.id_cotizacion 
     AND o.inversor_id = (SELECT id_inversor FROM inversor WHERE email = 'juan.perez@example.com') 
     ORDER BY o.fecha DESC LIMIT 1)) AS rendimiento
FROM 
    portafolio_acciones pa
JOIN 
    acciones a ON pa.accion_id = a.id_accion
JOIN 
    portafolio p ON pa.portafolio_id = p.id_portafolio
JOIN 
    cotizacion c ON c.accion_id = a.id_accion
WHERE 
    p.id_inversor = (SELECT id_inversor FROM inversor WHERE email = 'juan.perez@example.com'); -- Cambiar email según el inversor

-- GUARDAR OPERACIONES DE COMPRA/VENTA
INSERT INTO operacion (fecha, hora, precio_operado, cantidad_operada, cotizacion_id, tipo_operacion_id, inversor_id) 
VALUES (
    CURDATE(),
    CURTIME(),
    150.00,
    20,
    (SELECT id_cotizacion FROM cotizacion WHERE accion_id = (SELECT id_accion FROM acciones WHERE ticker = 'AAPL')), 
    (SELECT id_tipo_operacion FROM tipo_operacion WHERE tipo = 'compra'),
    (SELECT id_inversor FROM inversor WHERE email = 'juan.perez@example.com')
);

-- VALIDAR EXISTENCIAS ANTES DE COMPRA
SELECT cantidad_tenencia 
FROM portafolio_acciones 
WHERE portafolio_id = (SELECT id_portafolio FROM portafolio WHERE id_inversor = (SELECT id_inversor FROM inversor WHERE email = 'juan.perez@example.com')) 
AND accion_id = (SELECT id_accion FROM acciones WHERE ticker = 'AAPL');

-- ACTUALIZAR SALDO DESPUÉS DE COMPRA
UPDATE portafolio 
SET saldo_cuenta = saldo_cuenta - (148.00 * 10)
WHERE id_inversor = (SELECT id_inversor FROM inversor WHERE email = 'juan.perez@example.com');

-- ACTUALIZAR PORTAFOLIO DESPUÉS DE COMPRA
UPDATE portafolio_acciones 
SET cantidad_tenencia = cantidad_tenencia + 10
WHERE portafolio_id = (SELECT id_portafolio FROM portafolio WHERE id_inversor = (SELECT id_inversor FROM inversor WHERE email = 'juan.perez@example.com')) 
AND accion_id = (SELECT id_accion FROM acciones WHERE ticker = 'AAPL');

-- LISTAR HISTORIAL DE OPERACIONES DE UN INVERSOR
SELECT 
    o.fecha, 
    o.hora, 
    o.precio_operado, 
    o.cantidad_operada, 
    `to`.tipo AS tipo_operacion
FROM 
    operacion o
JOIN 
    tipo_operacion `to` ON o.tipo_operacion_id = `to`.id_tipo_operacion
WHERE 
    o.inversor_id = (SELECT id_inversor FROM inversor WHERE email = 'juan.perez@example.com') 
ORDER BY 
    o.fecha DESC, o.hora DESC;

-- OBTENER PRECIOS ACTUALES DE COMPRA Y VENTA DE UN ACTIVO
SELECT 
    precio_compra_actual, 
    precio_venta_actual 
FROM 
    cotizacion 
WHERE 
    accion_id = (SELECT id_accion FROM acciones WHERE ticker = 'AAPL'); -- Cambiar ticker según la acción que se requiera

-- MOSTRAR TODOS LOS INVERSORES CON SUS SALDOS EN CUENTA
SELECT 
    i.nombre, 
    i.apellido, 
    p.saldo_cuenta 
FROM 
    inversor i
JOIN 
    portafolio p ON i.id_inversor = p.id_inversor;

-- VERIFICAR INICIO DE SESIÓN
SELECT 
    inversor.id_inversor, 
    inversor.nombre, 
    inversor.apellido, 
    portafolio.saldo_cuenta
FROM 
    inversor
JOIN 
    portafolio ON inversor.id_inversor = portafolio.id_inversor
WHERE 
    inversor.email = 'juan.perez@example.com' AND inversor.contraseña = 'hashed_password'; -- Cambiar email y contraseña según corresponda

-- VALIDAR EXISTENCIAS ANTES DE REALIZAR UNA COMPRA
SELECT 
    cantidad_tenencia 
FROM 
    portafolio_acciones 
WHERE 
    portafolio_id = (SELECT id_portafolio FROM portafolio WHERE id_inversor = (SELECT id_inversor FROM inversor WHERE email = 'juan.perez@example.com')) 
    AND accion_id = (SELECT id_accion FROM acciones WHERE ticker = 'AAPL'); -- Cambiarticker según la acción que se requiera

-- OBTENER PRECIO DE COMPRA ACTUAL DE UNA ACCIÓN
SELECT 
    precio_compra_actual
FROM 
    cotizacion 
WHERE 
    accion_id = (SELECT id_accion FROM acciones WHERE ticker = 'AAPL'); -- Cambiar ticker según la acción que se requiera

-- OBTENER PRECIO DE VENTA ACTUAL DE UNA ACCIÓN
SELECT 
    precio_venta_actual 
FROM 
    cotizacion 
WHERE 
    accion_id = (SELECT id_accion FROM acciones WHERE ticker = 'AAPL'); -- Cambiar ticker según la acción que se requiera
