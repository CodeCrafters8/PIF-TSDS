-- Insertar datos de prueba en perfil_inversor 
INSERT INTO perfil_inversor (tipo_inversor) 
VALUES ('Conservador'), ('Moderado'), ('Agresivo');

-- Insertar datos de prueba en inversor
INSERT INTO inversor (cuit, nombre, apellido, email, contraseña, perfil_inversor_id)
VALUES 
('12345678901', 'Juan', 'Pérez', 'juan.perez@example.com', 'hashed_password', 
    (SELECT id_perfil_inversor FROM perfil_inversor WHERE tipo_inversor = 'Conservador')),
('23456789012', 'Ana', 'López', 'ana.lopez@example.com', 'hashed_password', 
    (SELECT id_perfil_inversor FROM perfil_inversor WHERE tipo_inversor = 'Moderado')),
('34567890123', 'Luis', 'Martínez', 'luis.martinez@example.com', 'hashed_password', 
    (SELECT id_perfil_inversor FROM perfil_inversor WHERE tipo_inversor = 'Agresivo'));

-- Insertar datos de prueba en portafolio 
INSERT INTO portafolio (saldo_cuenta, id_inversor)
VALUES 
(10000.00, (SELECT id_inversor FROM inversor WHERE email = 'juan.perez@example.com')),
(15000.00, (SELECT id_inversor FROM inversor WHERE email = 'ana.lopez@example.com')),
(20000.00, (SELECT id_inversor FROM inversor WHERE email = 'luis.martinez@example.com'));

-- Insertar datos de prueba en sector
INSERT INTO sector (sector) VALUES ('Tecnología'), ('Energía'), ('Finanzas');

-- Insertar datos de prueba en acciones 
INSERT INTO acciones (ticker, nombre, empresa, sector_id)
VALUES 
('AAPL', 'Apple', 'Apple Inc.', (SELECT id_sector FROM sector WHERE sector = 'Tecnología')),
('TSLA', 'Tesla', 'Tesla Inc.', (SELECT id_sector FROM sector WHERE sector = 'Energía')),
('JPM', 'JP Morgan', 'JP Morgan Chase', (SELECT id_sector FROM sector WHERE sector = 'Finanzas'));

-- Insertar datos de prueba en cotización 
INSERT INTO cotizacion (fecha, hora, accion_id, precio_apertura, minimo_diario, maximo_diario, precio_compra_actual, precio_venta_actual, ultimo_precio_cierre, cantidad_compra_diaria, cantidad_venta_diaria)
VALUES 
(CURDATE(), CURTIME(), (SELECT id_accion FROM acciones WHERE ticker = 'AAPL'), 145.00, 140.00, 150.00, 148.00, 149.00, 147.00, 1000, 900),
(CURDATE(), CURTIME(), (SELECT id_accion FROM acciones WHERE ticker = 'TSLA'), 750.00, 720.00, 780.00, 760.00, 770.00, 740.00, 2000, 1800),
(CURDATE(), CURTIME(), (SELECT id_accion FROM acciones WHERE ticker = 'JPM'), 120.00, 115.00, 125.00, 122.00, 123.00, 119.00, 1500, 1300);

-- Insertar datos de prueba en tipo_operacion
INSERT INTO tipo_operacion (tipo) VALUES ('compra'), ('venta');

-- Insertar datos de prueba en portafolio_acciones 
INSERT INTO portafolio_acciones (portafolio_id, accion_id, cantidad_tenencia)
VALUES 
((SELECT id_portafolio FROM portafolio WHERE id_inversor = (SELECT id_inversor FROM inversor WHERE email = 'juan.perez@example.com')), 
 (SELECT id_accion FROM acciones WHERE ticker = 'AAPL'), 50),
((SELECT id_portafolio FROM portafolio WHERE id_inversor = (SELECT id_inversor FROM inversor WHERE email = 'ana.lopez@example.com')), 
 (SELECT id_accion FROM acciones WHERE ticker = 'TSLA'), 30);

-- Insertar operaciones de prueba en la tabla operacion
INSERT INTO operacion (fecha, hora, precio_operado, cantidad_operada, cotizacion_id, tipo_operacion_id, inversor_id) 
VALUES 
(CURDATE(), CURTIME(), 148.00, 10, (SELECT id_cotizacion FROM cotizacion WHERE accion_id = (SELECT id_accion FROM acciones WHERE ticker = 'AAPL')), 
 (SELECT id_tipo_operacion FROM tipo_operacion WHERE tipo = 'compra'), 
 (SELECT id_inversor FROM inversor WHERE email = 'juan.perez@example.com')),
(CURDATE(), CURTIME(), 760.00, 5, (SELECT id_cotizacion FROM cotizacion WHERE accion_id = (SELECT id_accion FROM acciones WHERE ticker = 'TSLA')), 
 (SELECT id_tipo_operacion FROM tipo_operacion WHERE tipo = 'compra'), 
 (SELECT id_inversor FROM inversor WHERE email = 'ana.lopez@example.com')),
(CURDATE(), CURTIME(), 123.00, 20, (SELECT id_cotizacion FROM cotizacion WHERE accion_id = (SELECT id_accion FROM acciones WHERE ticker = 'JPM')), 
 (SELECT id_tipo_operacion FROM tipo_operacion WHERE tipo = 'compra'), 
 (SELECT id_inversor FROM inversor WHERE email = 'luis.martinez@example.com'));

-- Insertar datos de prueba en historial_operaciones
INSERT INTO historial_operaciones (operacion_id, precio_operado, cantidad_operada, tipo_operacion_id) 
VALUES 
((SELECT id_operacion FROM operacion WHERE cotizacion_id = (SELECT id_cotizacion FROM cotizacion WHERE accion_id = (SELECT id_accion FROM acciones WHERE ticker = 'AAPL')) AND inversor_id = (SELECT id_inversor FROM inversor WHERE email = 'juan.perez@example.com') LIMIT 1),
 148.00, 10, (SELECT id_tipo_operacion FROM tipo_operacion WHERE tipo = 'compra')),
  
((SELECT id_operacion FROM operacion WHERE cotizacion_id = (SELECT id_cotizacion FROM cotizacion WHERE accion_id = (SELECT id_accion FROM acciones WHERE ticker = 'TSLA')) AND inversor_id = (SELECT id_inversor FROM inversor WHERE email = 'ana.lopez@example.com') LIMIT 1),
 760.00, 5, (SELECT id_tipo_operacion FROM tipo_operacion WHERE tipo = 'compra')),

((SELECT id_operacion FROM operacion WHERE cotizacion_id = (SELECT id_cotizacion FROM cotizacion WHERE accion_id = (SELECT id_accion FROM acciones WHERE ticker = 'JPM')) AND inversor_id = (SELECT id_inversor FROM inversor WHERE email = 'luis.martinez@example.com') LIMIT 1),
 123.00, 20, (SELECT id_tipo_operacion FROM tipo_operacion WHERE tipo = 'compra'));
