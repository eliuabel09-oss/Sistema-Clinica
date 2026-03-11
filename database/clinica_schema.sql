-- ============================================================
--  Sistema de Gestión Clínica — Script SQL para phpMyAdmin
--  Motor: MySQL 8.x | Charset: utf8mb4 | Collation: utf8mb4_unicode_ci
--  Ejecutar en orden para respetar las FK
-- ============================================================

CREATE DATABASE IF NOT EXISTS clinica_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE clinica_db;

-- ------------------------------------------------------------
-- 1. PACIENTES
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS pacientes (
    id                    INT UNSIGNED     NOT NULL AUTO_INCREMENT,
    nombres               VARCHAR(100)     NOT NULL,
    apellidos             VARCHAR(100)     NOT NULL,
    fecha_nacimiento      DATE             NOT NULL,
    sexo                  CHAR(1)          NOT NULL COMMENT 'M=Masculino F=Femenino O=Otro',
    curp                  VARCHAR(18)      NULL UNIQUE,
    tipo_sangre           VARCHAR(3)       NOT NULL DEFAULT '',
    telefono              VARCHAR(15)      NOT NULL,
    email                 VARCHAR(254)     NULL,
    direccion             TEXT             NOT NULL DEFAULT '',
    alergias              TEXT             NOT NULL DEFAULT '',
    antecedentes          TEXT             NOT NULL DEFAULT '',
    enfermedades_cronicas TEXT             NOT NULL DEFAULT '',
    activo                TINYINT(1)       NOT NULL DEFAULT 1,
    fecha_registro        DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion   DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_nombre      (apellidos, nombres),
    INDEX idx_curp        (curp),
    CONSTRAINT chk_sexo   CHECK (sexo IN ('M','F','O'))
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Tabla maestra de pacientes';

-- ------------------------------------------------------------
-- 2. ARCHIVOS CLÍNICOS
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS archivos_clinicos (
    id            INT UNSIGNED     NOT NULL AUTO_INCREMENT,
    paciente_id   INT UNSIGNED     NOT NULL,
    tipo          VARCHAR(10)      NOT NULL COMMENT 'PDF|IMG|LAB|RX|OTRO',
    nombre        VARCHAR(200)     NOT NULL,
    archivo       VARCHAR(255)     NOT NULL COMMENT 'Ruta relativa en MEDIA_ROOT',
    descripcion   TEXT             NOT NULL DEFAULT '',
    fecha_carga   DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_paciente (paciente_id),
    CONSTRAINT fk_archivo_paciente
        FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT chk_tipo_archivo CHECK (tipo IN ('PDF','IMG','LAB','RX','OTRO'))
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 3. DOCTORES
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS doctores (
    id            INT UNSIGNED     NOT NULL AUTO_INCREMENT,
    nombres       VARCHAR(100)     NOT NULL,
    apellidos     VARCHAR(100)     NOT NULL,
    especialidad  VARCHAR(100)     NOT NULL,
    cedula        VARCHAR(20)      NOT NULL UNIQUE,
    telefono      VARCHAR(15)      NOT NULL DEFAULT '',
    email         VARCHAR(254)     NOT NULL DEFAULT '',
    activo        TINYINT(1)       NOT NULL DEFAULT 1,
    PRIMARY KEY (id),
    INDEX idx_doctor_nombre (apellidos, nombres)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 4. CITAS
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS citas (
    id                  INT UNSIGNED     NOT NULL AUTO_INCREMENT,
    paciente_id         INT UNSIGNED     NOT NULL,
    doctor_id           INT UNSIGNED     NOT NULL,
    fecha_hora          DATETIME         NOT NULL,
    duracion_min        SMALLINT UNSIGNED NOT NULL DEFAULT 30,
    tipo                VARCHAR(20)      NOT NULL DEFAULT 'PRIMERA_VEZ',
    estado              VARCHAR(15)      NOT NULL DEFAULT 'PENDIENTE',
    motivo              TEXT             NOT NULL DEFAULT '',
    notas_admin         TEXT             NOT NULL DEFAULT '',
    fecha_creacion      DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_fecha_estado  (fecha_hora, estado),
    INDEX idx_paciente_cita (paciente_id, estado),
    INDEX idx_doctor_fecha  (doctor_id, fecha_hora),
    CONSTRAINT fk_cita_paciente
        FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_cita_doctor
        FOREIGN KEY (doctor_id) REFERENCES doctores(id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT chk_estado_cita
        CHECK (estado IN ('PENDIENTE','CONFIRMADA','CANCELADA','COMPLETADA','NO_ASISTIO')),
    CONSTRAINT chk_tipo_cita
        CHECK (tipo IN ('PRIMERA_VEZ','SEGUIMIENTO','URGENCIA','REVISION'))
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 5. CONSULTAS
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS consultas (
    id                  INT UNSIGNED     NOT NULL AUTO_INCREMENT,
    cita_id             INT UNSIGNED     NULL UNIQUE,
    paciente_id         INT UNSIGNED     NOT NULL,
    doctor_id           INT UNSIGNED     NOT NULL,
    fecha               DATETIME         NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -- Signos vitales
    peso_kg             DECIMAL(5,2)     NULL,
    talla_cm            DECIMAL(5,2)     NULL,
    presion_arterial    VARCHAR(10)      NOT NULL DEFAULT '',
    frecuencia_cardiaca SMALLINT UNSIGNED NULL,
    temperatura         DECIMAL(4,1)     NULL,
    saturacion_o2       TINYINT UNSIGNED NULL,
    -- Nota SOAP
    subjetivo           TEXT             NOT NULL,
    objetivo            TEXT             NOT NULL,
    diagnostico         TEXT             NOT NULL,
    plan                TEXT             NOT NULL,
    evolucion           TEXT             NOT NULL DEFAULT '',
    proxima_cita        DATE             NULL,
    PRIMARY KEY (id),
    INDEX idx_consulta_paciente (paciente_id, fecha),
    CONSTRAINT fk_consulta_cita
        FOREIGN KEY (cita_id) REFERENCES citas(id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_consulta_paciente
        FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_consulta_doctor
        FOREIGN KEY (doctor_id) REFERENCES doctores(id)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 6. RECETAS
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS recetas (
    id            INT UNSIGNED     NOT NULL AUTO_INCREMENT,
    consulta_id   INT UNSIGNED     NOT NULL,
    medicamento   VARCHAR(200)     NOT NULL,
    dosis         VARCHAR(100)     NOT NULL,
    frecuencia    VARCHAR(100)     NOT NULL,
    duracion      VARCHAR(100)     NOT NULL,
    indicaciones  TEXT             NOT NULL DEFAULT '',
    orden         TINYINT UNSIGNED NOT NULL DEFAULT 1,
    PRIMARY KEY (id),
    INDEX idx_receta_consulta (consulta_id),
    CONSTRAINT fk_receta_consulta
        FOREIGN KEY (consulta_id) REFERENCES consultas(id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- MIGRACION SQL — Ejecutar en phpMyAdmin / MySQL
-- NO borra ninguna tabla existente
-- Agrega campos nuevos a tablas existentes
-- ============================================================

-- 1. Agregar campo 'usuario_id' a tabla doctores (vincula con auth_user)
ALTER TABLE doctores
  ADD COLUMN usuario_id INT NULL DEFAULT NULL,
  ADD COLUMN foto VARCHAR(100) NULL DEFAULT NULL,
  ADD COLUMN biografia TEXT NULL DEFAULT NULL,
  ADD COLUMN horario_atencion VARCHAR(200) NULL DEFAULT NULL,
  ADD CONSTRAINT fk_doctor_usuario
    FOREIGN KEY (usuario_id) REFERENCES auth_user(id)
    ON DELETE SET NULL;

-- 2. Agregar campo 'informe_doctor' a tabla citas
ALTER TABLE citas
  ADD COLUMN informe_doctor LONGTEXT NULL DEFAULT NULL,
  ADD COLUMN informe_fecha DATETIME NULL DEFAULT NULL;


ALTER TABLE pacientes
  ADD COLUMN dni VARCHAR(8) NULL DEFAULT NULL
  AFTER curp;

-- ============================================================
-- VERIFICAR que todo quedó bien:
-- SHOW COLUMNS FROM doctores;
-- SHOW COLUMNS FROM citas;
-- DESCRIBE perfiles_usuario;
-- ============================================================

-- ============================================================
-- Datos de ejemplo para desarrollo
-- ============================================================
INSERT INTO doctores (nombres, apellidos, especialidad, cedula, telefono, email) VALUES
('Ana Lucía', 'Ramírez Torres',  'Medicina General',    'MG-001234', '555-1001', 'a.ramirez@clinica.mx'),
('Carlos',    'Mendoza Herrera', 'Cardiología',          'CA-005678', '555-1002', 'c.mendoza@clinica.mx');

INSERT INTO pacientes (nombres, apellidos, fecha_nacimiento, sexo, curp, tipo_sangre, telefono, email) VALUES
('Juan Pablo', 'García López',   '1985-03-12', 'M', 'GALJ850312HDFRZN01', 'O+', '555-2001', 'jp.garcia@email.com'),
('María Elena','Soto Vargas',    '1992-07-25', 'F', 'SOVM920725MDFTRR02', 'A+', '555-2002', 'm.soto@email.com');

--- ============================================================
-- PASO 1: Eliminar tabla si quedó a medias (ejecutar primero)
-- ============================================================
DROP TABLE IF EXISTS `doctores_horarios`;

-- ============================================================
-- PASO 2: Crear tabla sin CONSTRAINT (más compatible con XAMPP)
-- ============================================================
CREATE TABLE `doctores_horarios` (
  `id`          INT      NOT NULL AUTO_INCREMENT,
  `doctor_id`   INT      NOT NULL,
  `dia_semana`  TINYINT  NOT NULL COMMENT '0=Lun 1=Mar 2=Mie 3=Jue 4=Vie 5=Sab 6=Dom',
  `hora_inicio` TIME     NOT NULL,
  `hora_fin`    TIME     NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `horario_unico` (`doctor_id`, `dia_semana`),
  KEY `idx_doctor_id` (`doctor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ============================================================
-- PASO 3: Horarios Lun-Vie 8am-6pm para los 4 doctores reales
-- Doctor 1: Ana Lucía Ramírez Torres     — Medicina General
-- Doctor 2: Carlos Mendoza Herrera       — Cardiología
-- Doctor 3: abel diaz                    — General
-- Doctor 4: Josias Diaz                  — Soporte
-- ============================================================
INSERT INTO `doctores_horarios` (`doctor_id`, `dia_semana`, `hora_inicio`, `hora_fin`) VALUES
-- Dr. Ana Lucía Ramírez — Medicina General
(1, 0, '08:00:00', '18:00:00'),
(1, 1, '08:00:00', '18:00:00'),
(1, 2, '08:00:00', '18:00:00'),
(1, 3, '08:00:00', '18:00:00'),
(1, 4, '08:00:00', '18:00:00'),

-- Dr. Carlos Mendoza — Cardiología
(2, 0, '08:00:00', '18:00:00'),
(2, 1, '08:00:00', '18:00:00'),
(2, 2, '08:00:00', '18:00:00'),
(2, 3, '08:00:00', '18:00:00'),
(2, 4, '08:00:00', '18:00:00'),

-- Dr. abel diaz — General
(3, 0, '08:00:00', '18:00:00'),
(3, 1, '08:00:00', '18:00:00'),
(3, 2, '08:00:00', '18:00:00'),
(3, 3, '08:00:00', '18:00:00'),
(3, 4, '08:00:00', '18:00:00'),

-- Dr. Josias Diaz — Soporte
(4, 0, '08:00:00', '18:00:00'),
(4, 1, '08:00:00', '18:00:00'),
(4, 2, '08:00:00', '18:00:00'),
(4, 3, '08:00:00', '18:00:00'),
(4, 4, '08:00:00', '18:00:00');

-- ============================================================
-- PASO 4: Verificar que quedó bien
-- ============================================================
SELECT
  d.id,
  d.nombres,
  d.apellidos,
  d.especialidad,
  h.dia_semana,
  CASE h.dia_semana
    WHEN 0 THEN 'Lunes'
    WHEN 1 THEN 'Martes'
    WHEN 2 THEN 'Miércoles'
    WHEN 3 THEN 'Jueves'
    WHEN 4 THEN 'Viernes'
    WHEN 5 THEN 'Sábado'
    WHEN 6 THEN 'Domingo'
  END AS dia_nombre,
  h.hora_inicio,
  h.hora_fin
FROM doctores_horarios h
JOIN doctores d ON h.doctor_id = d.id
ORDER BY d.id, h.dia_semana;

-- ============================================================
-- CORREGIR horarios a Lun-Vie 8am-6pm para los 3 doctores
-- Ejecutar en phpMyAdmin → clinica_db → SQL
-- ============================================================

-- Limpiar los registros actuales que quedaron mal
DELETE FROM `doctores_horarios`;

-- Reinsertar correctamente (solo doctores 1, 2, 3 que existen)
INSERT INTO `doctores_horarios` (`doctor_id`, `dia_semana`, `hora_inicio`, `hora_fin`) VALUES
-- Dr. Ana Lucía Ramírez (id=1) — Medicina General
(1, 0, '08:00:00', '18:00:00'),
(1, 1, '08:00:00', '18:00:00'),
(1, 2, '08:00:00', '18:00:00'),
(1, 3, '08:00:00', '18:00:00'),
(1, 4, '08:00:00', '18:00:00'),

-- Dr. Carlos Mendoza (id=2) — Cardiología
(2, 0, '08:00:00', '18:00:00'),
(2, 1, '08:00:00', '18:00:00'),
(2, 2, '08:00:00', '18:00:00'),
(2, 3, '08:00:00', '18:00:00'),
(2, 4, '08:00:00', '18:00:00'),

-- Dr. abel diaz (id=3) — General
(3, 0, '08:00:00', '18:00:00'),
(3, 1, '08:00:00', '18:00:00'),
(3, 2, '08:00:00', '18:00:00'),
(3, 3, '08:00:00', '18:00:00'),
(3, 4, '08:00:00', '18:00:00');

-- También activar al Dr. abel diaz que estaba inactivo
UPDATE `doctores` SET `activo` = 1 WHERE `id` = 3;

-- Verificar resultado
SELECT d.id, d.nombres, d.apellidos, d.especialidad, d.activo,
       COUNT(h.id) as dias_configurados
FROM doctores d
LEFT JOIN doctores_horarios h ON h.doctor_id = d.id
GROUP BY d.id;

UPDATE `doctores` SET `activo` = 1 WHERE `id` = 3;