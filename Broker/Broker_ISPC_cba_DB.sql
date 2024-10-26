CREATE DATABASE IF NOT EXISTS Broker_ISPC_CBAA;
USE Broker_ISPC_CBAA;

CREATE TABLE IF NOT EXISTS perfil_inversor (
    id_perfil_inversor INT AUTO_INCREMENT,
    tipo_inversor VARCHAR(20),
    PRIMARY KEY (id_perfil_inversor) 
);

CREATE TABLE IF NOT EXISTS inversor (
    id_inversor INT AUTO_INCREMENT,
    cuil VARCHAR(11) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(320) NOT NULL UNIQUE,
    contraseña VARCHAR(255) NOT NULL,
    saldo_pesos DECIMAL (10,2) NOT NULL,
    perfil_inversor_id INT,  
    PRIMARY KEY (id_inversor),
    CONSTRAINT fk_perfil_inversor FOREIGN KEY (perfil_inversor_id) 
        REFERENCES perfil_inversor(id_perfil_inversor)
        ON DELETE SET NULL  
);

CREATE TABLE IF NOT EXISTS tipo_operacion (
    id_tipo_operacion INT AUTO_INCREMENT,
    tipo VARCHAR(10),
    PRIMARY KEY (id_tipo_operacion)
);

CREATE TABLE IF NOT EXISTS sector (
    id_sector INT AUTO_INCREMENT,
    sector VARCHAR(30),
    PRIMARY KEY (id_sector)
);

CREATE TABLE IF NOT EXISTS  empresa (
id_empresa INT AUTO_INCREMENT,
nombre VARCHAR(30),
cuit VARCHAR(16),
domicilio VARCHAR(100),
sector_id INT NOT NULL,
	PRIMARY KEY (id_empresa),
CONSTRAINT fk_sector FOREIGN KEY (sector_id)
	REFERENCES sector(id_sector) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS acciones (
    id_accion INT AUTO_INCREMENT,
    ticker VARCHAR(10) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    empresa_id INT NOT NULL,
        PRIMARY KEY (id_accion),
    CONSTRAINT fk_empresa FOREIGN KEY (empresa_id)
        REFERENCES empresa(id_empresa) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS cotizacion (
    id_cotizacion INT AUTO_INCREMENT,
    fecha DATETIME NOT NULL,
    accion_id INT,
    precio_apertura DECIMAL(10, 2) NOT NULL CHECK (precio_apertura >= 0),
    minimo_diario DECIMAL(10, 2) NOT NULL CHECK (minimo_diario >= 0),
    maximo_diario DECIMAL(10, 2) NOT NULL CHECK (maximo_diario >= 0),
    precio_compra_actual DECIMAL(10, 2) NOT NULL CHECK (precio_compra_actual >= 0),
    precio_venta_actual DECIMAL(10, 2) NOT NULL CHECK (precio_venta_actual >= 0),
    ultimo_precio_cierre DECIMAL(10, 2) NOT NULL CHECK (ultimo_precio_cierre >= 0),
    cantidad_compra_diaria INT NOT NULL CHECK (cantidad_compra_diaria >= 0),
    cantidad_venta_diaria INT NOT NULL CHECK (cantidad_venta_diaria >= 0),
    PRIMARY KEY (id_cotizacion),
    CONSTRAINT fk_accion_cotizacion FOREIGN KEY (accion_id)
        REFERENCES acciones(id_accion) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS operacion (
    id_operacion INT AUTO_INCREMENT,
    fecha DATETIME NOT NULL,
    precio_operado DECIMAL(10, 2) NOT NULL CHECK (precio_operado > 0), 
    cantidad_operada INT NOT NULL CHECK (cantidad_operada > 0),
    cotizacion_id INT,
    tipo_operacion_id INT,
    inversor_id INT, 
    comision INT,
    id_accion INT,  -- Añadir el campo id_accion
    PRIMARY KEY (id_operacion),
    CONSTRAINT fk_cotizacion_operacion FOREIGN KEY (cotizacion_id)
        REFERENCES cotizacion(id_cotizacion) ON DELETE CASCADE,
    CONSTRAINT fk_tipo_operacion_operacion FOREIGN KEY (tipo_operacion_id)
        REFERENCES tipo_operacion(id_tipo_operacion) ON DELETE CASCADE,
    CONSTRAINT fk_inversor_operacion FOREIGN KEY (inversor_id)
        REFERENCES inversor(id_inversor) ON DELETE CASCADE,
    CONSTRAINT fk_accion_operacion FOREIGN KEY (id_accion)
        REFERENCES acciones(id_accion) ON DELETE CASCADE  
);


CREATE TABLE IF NOT EXISTS portafolio (
    id_portafolio INT AUTO_INCREMENT,
    total_invertido DECIMAL (10,2) NOT NULL,
    id_inversor INT NOT NULL,
    PRIMARY KEY (id_portafolio),
    CONSTRAINT fk_portafolio_inversor FOREIGN KEY (id_inversor)
        REFERENCES inversor(id_inversor) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS portafolio_acciones (
    id_portafolio_acciones INT AUTO_INCREMENT,
    portafolio_id INT NOT NULL,
    accion_id INT NOT NULL,
    cantidad_tenencia INT NOT NULL CHECK (cantidad_tenencia >= 0),
    PRIMARY KEY (id_portafolio_acciones),
    CONSTRAINT fk_portafolio_acciones FOREIGN KEY (portafolio_id)
        REFERENCES portafolio(id_portafolio) ON DELETE CASCADE,
    CONSTRAINT fk_accion_portafolio FOREIGN KEY (accion_id)
        REFERENCES acciones(id_accion) ON DELETE CASCADE
);
