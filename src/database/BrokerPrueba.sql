CREATE DATABASE IF NOT EXISTS Broker_Prueba;
USE Broker_Prueba;

CREATE TABLE IF NOT EXISTS PerfilInversor (
    IdPerfilInversor INT AUTO_INCREMENT PRIMARY KEY,
    TipoPerfil ENUM('conservador', 'medio', 'agresivo') NOT NULL
);

CREATE TABLE IF NOT EXISTS Usuario (
    ID_Usuario INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Apellido VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Contrasena VARCHAR(255) NOT NULL,
    Cuil VARCHAR(20) NOT NULL UNIQUE,  -- Nuevo campo Cuil
    Saldo_Inicial DECIMAL(10, 2) DEFAULT 1000000.00,
    IdPerfilInversor INT,  -- Nueva referencia al perfil del inversor
    FOREIGN KEY (IdPerfilInversor) REFERENCES PerfilInversor(IdPerfilInversor)  -- Relación con PerfilInversor
);

-- Insertar perfiles de inversores (opcional, pero recomendado)
INSERT INTO PerfilInversor (TipoPerfil) VALUES ('conservador'), ('medio'), ('agresivo');


select * from usuario;

