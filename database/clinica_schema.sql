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

