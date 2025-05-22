USE enchufes;

-- Crear tabla usuarios
CREATE TABLE usuarios (
  id SERIAL PRIMARY KEY,
  nombre_usuario TEXT NOT NULL UNIQUE,
  contrasena TEXT NOT NULL
);

-- Crear tabla registros_acceso
CREATE TABLE registros_acceso (
  id SERIAL PRIMARY KEY,
  nombre_usuario TEXT NOT NULL,
  ip_contenedor TEXT NOT NULL,
  accion TEXT NOT NULL,
  fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  ip_publica_usuario TEXT NOT NULL
);

-- Crear tabla enchufes_integrados
CREATE TABLE enchufes_integrados (
  id SERIAL PRIMARY KEY,
  nombre TEXT NOT NULL,
  id_tuya TEXT NOT NULL,
  clave_local TEXT NOT NULL,
  ip_local TEXT NOT NULL
);

-- Insertar enchufes actuales manualmente
INSERT INTO enchufes_integrados (id, nombre, id_tuya, clave_local, ip_local) VALUES
(1, 'Tele', 'xxx', 'xxx', '192.168.0.xx'), -- Ajusta los datos al tuyo
(2, 'Luz', 'xxx', 'xxx', '192.168.0.xx');  -- Ajusta los datos al tuyo