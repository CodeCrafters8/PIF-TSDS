USE Broker_ISPC_cba;

-- Insertar datos de prueba en perfil_inversor
INSERT INTO perfil_inversor (tipo_inversor) 
VALUES ('Conservador'), ('Moderado'), ('Agresivo');

-- Insertar datos de prueba en inversor
INSERT INTO inversor (cuil, nombre, apellido, email, contraseña, saldo_pesos, perfil_inversor_id)
VALUES 
('12345678901', 'Juan', 'Pérez', 'juan.perez@example.com', 'hashed_password', 2000000.00,
    (SELECT id_perfil_inversor FROM perfil_inversor WHERE tipo_inversor = 'Conservador')),
('23456789012', 'Ana', 'López', 'ana.lopez@example.com', 'hashed_password', 4500000.00,
    (SELECT id_perfil_inversor FROM perfil_inversor WHERE tipo_inversor = 'Moderado')),
('34567890123', 'Luis', 'Martínez', 'luis.martinez@example.com', 'hashed_password', 1000000.00,
    (SELECT id_perfil_inversor FROM perfil_inversor WHERE tipo_inversor = 'Agresivo'));

-- Insertar datos de prueba en portafolio
INSERT INTO portafolio (id_inversor, total_invertido)
VALUES 
((SELECT id_inversor FROM inversor WHERE email = 'juan.perez@example.com'), 5000000.00),
((SELECT id_inversor FROM inversor WHERE email = 'ana.lopez@example.com'), 2300000.00),
((SELECT id_inversor FROM inversor WHERE email = 'luis.martinez@example.com'), 1200000.00);

-- Insertar datos de prueba en sector
INSERT INTO sector (sector) VALUES ('Tecnología'), ('Energía'), ('Finanzas');

-- Insertar datos de prueba en empresa
INSERT INTO empresa (nombre, cuit, domicilio, sector_id)
VALUES
('Apple Inc.', '30-71234567-1', 'Av. Corrientes 1234, Piso 5, CABA, Buenos Aires, Argentina', 
	(SELECT id_sector FROM sector WHERE sector = 'Tecnología')),
('Tesla Inc.', '30-63456789-3', 'Calle San Martín 567, Rosario, Santa Fe, Argentina',
	(SELECT id_sector FROM sector WHERE sector = 'Energía')),
('JP Morgan Chase', '30-82901234-8', 'Ruta Nacional 9, Km 315, Córdoba, Argentina',
	(SELECT id_sector FROM sector WHERE sector = 'Finanzas')),
('Amazon', '20-12345678-9', 'Amazon.com S.A., Avenida Ficticia 1234, Ciudad Imaginaria, CABA, Argentina', 
	(SELECT id_sector FROM sector WHERE sector = 'Tecnología'));

-- Insertar datos de prueba en acciones
INSERT INTO acciones (ticker, nombre, empresa_id)
VALUES 
('AAPL', 'Apple', (SELECT id_empresa FROM empresa WHERE nombre = 'Apple Inc.')),
('TSLA', 'Tesla', (SELECT id_empresa FROM empresa WHERE nombre = 'Tesla Inc.')),
('JPM', 'JP Morgan', (SELECT id_empresa FROM empresa WHERE nombre = 'JP Morgan Chase'));

-- Insertar datos de prueba en cotización
INSERT INTO cotizacion (fecha, accion_id, precio_apertura, minimo_diario, maximo_diario, precio_compra_actual, precio_venta_actual, ultimo_precio_cierre, cantidad_compra_diaria, cantidad_venta_diaria, cantidad_acciones_mercado)
VALUES 
(CURDATE(), (SELECT id_accion FROM acciones WHERE ticker = 'AAPL'), 145.00, 140.00, 150.00, 148.00, 149.00, 147.00, 1000, 900, 100),
(CURDATE(), (SELECT id_accion FROM acciones WHERE ticker = 'TSLA'), 750.00, 720.00, 780.00, 760.00, 770.00, 740.00, 2000, 1800, 200),
(CURDATE(), (SELECT id_accion FROM acciones WHERE ticker = 'JPM'), 120.00, 115.00, 125.00, 122.00, 123.00, 119.00, 1500, 1300, 300);

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
INSERT INTO operacion (fecha, precio_operado, cantidad_operada, cotizacion_id, tipo_operacion_id, inversor_id, id_accion) 
VALUES 
(CURDATE(), 148.00, 10, (SELECT id_cotizacion FROM cotizacion WHERE accion_id = (SELECT id_accion FROM acciones WHERE ticker = 'AAPL')), 
 (SELECT id_tipo_operacion FROM tipo_operacion WHERE tipo = 'compra'), 
 (SELECT id_inversor FROM inversor WHERE email = 'juan.perez@example.com'),
 (SELECT id_accion FROM acciones WHERE ticker = 'AAPL')),
(CURDATE(), 760.00, 5, (SELECT id_cotizacion FROM cotizacion WHERE accion_id = (SELECT id_accion FROM acciones WHERE ticker = 'TSLA')), 
 (SELECT id_tipo_operacion FROM tipo_operacion WHERE tipo = 'compra'), 
 (SELECT id_inversor FROM inversor WHERE email = 'ana.lopez@example.com'),
 (SELECT id_accion FROM acciones WHERE ticker = 'TSLA')),
(CURDATE(), 123.00, 20, (SELECT id_cotizacion FROM cotizacion WHERE accion_id = (SELECT id_accion FROM acciones WHERE ticker = 'JPM')), 
 (SELECT id_tipo_operacion FROM tipo_operacion WHERE tipo = 'compra'), 
 (SELECT id_inversor FROM inversor WHERE email = 'luis.martinez@example.com'),
 (SELECT id_accion FROM acciones WHERE ticker = 'JPM'));
