-- mostrar datos de la cuenta de un inversor

SELECT 
    p.saldo_cuenta, 
    COALESCE(SUM(o.precio_operado * o.cantidad_operada), 0) AS total_invertido, 
    (COALESCE(SUM(o.precio_operado * o.cantidad_operada), 0) - p.saldo_cuenta) AS rendimiento_total
FROM 
    portafolio p
LEFT JOIN 
    operacion o ON p.id_inversor = o.inversor_id
WHERE 
    p.id_inversor = (SELECT id_inversor FROM inversor WHERE email = 'juan.perez@example.com') -- Cambiar el email según el inversor
GROUP BY 
    p.saldo_cuenta;

-- Listar activos en el portafolio
SELECT 
    a.nombre AS nombre_activo, 
    pa.cantidad_tenencia, 
    c.precio_compra_actual, 
    c.precio_venta_actual,
    (c.precio_compra_actual - (SELECT precio_operado FROM operacion o 
                               WHERE o.cotizacion_id = c.id_cotizacion 
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
    p.id_inversor = (SELECT id_inversor FROM inversor WHERE email = 'juan.perez@example.com'); -- Cambiar el email según el inversor

-- listar el historial de operaciones
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
    o.inversor_id = (SELECT id_inversor FROM inversor WHERE email = 'juan.perez@example.com') -- Cambiar el email según el inversor
ORDER BY 
    o.fecha DESC, o.hora DESC;

-- obtener precios actuales de compra y venta de un activo
SELECT 
    precio_compra_actual, 
    precio_venta_actual 
FROM 
    cotizacion 
WHERE 
    accion_id = (SELECT id_accion FROM acciones WHERE ticker = 'AAPL'); -- Cambiar el ticker según la acción deseada

-- Mostrar todos los inversores con sus saldos en cuenta
SELECT 
    i.nombre, 
    i.apellido, 
    p.saldo_cuenta 
FROM 
    inversor i
JOIN 
    portafolio p ON i.id_inversor = p.id_inversor;

