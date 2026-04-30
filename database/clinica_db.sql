-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 03-04-2026 a las 20:14:42
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `clinica_db`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `archivos_clinicos`
--

CREATE TABLE `archivos_clinicos` (
  `id` int(10) UNSIGNED NOT NULL,
  `paciente_id` int(10) UNSIGNED NOT NULL,
  `tipo` varchar(10) NOT NULL COMMENT 'PDF|IMG|LAB|RX|OTRO',
  `nombre` varchar(200) NOT NULL,
  `archivo` varchar(255) NOT NULL COMMENT 'Ruta relativa en MEDIA_ROOT',
  `descripcion` text NOT NULL DEFAULT '',
  `fecha_carga` datetime NOT NULL DEFAULT current_timestamp()
) ;

--
-- Volcado de datos para la tabla `archivos_clinicos`
--

INSERT INTO `archivos_clinicos` (`id`, `paciente_id`, `tipo`, `nombre`, `archivo`, `descripcion`, `fecha_carga`) VALUES
(1, 24, 'PDF', 'Eliu Diaz', 'archivos_clinicos/2026/03/61095087_Diaz.jpg', '', '2026-03-10 17:54:52');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add Paciente', 7, 'add_paciente'),
(26, 'Can change Paciente', 7, 'change_paciente'),
(27, 'Can delete Paciente', 7, 'delete_paciente'),
(28, 'Can view Paciente', 7, 'view_paciente'),
(29, 'Can add Archivo Clínico', 8, 'add_archivoclinico'),
(30, 'Can change Archivo Clínico', 8, 'change_archivoclinico'),
(31, 'Can delete Archivo Clínico', 8, 'delete_archivoclinico'),
(32, 'Can view Archivo Clínico', 8, 'view_archivoclinico'),
(33, 'Can add Doctor', 9, 'add_doctor'),
(34, 'Can change Doctor', 9, 'change_doctor'),
(35, 'Can delete Doctor', 9, 'delete_doctor'),
(36, 'Can view Doctor', 9, 'view_doctor'),
(37, 'Can add Cita', 10, 'add_cita'),
(38, 'Can change Cita', 10, 'change_cita'),
(39, 'Can delete Cita', 10, 'delete_cita'),
(40, 'Can view Cita', 10, 'view_cita'),
(41, 'Can add Consulta', 11, 'add_consulta'),
(42, 'Can change Consulta', 11, 'change_consulta'),
(43, 'Can delete Consulta', 11, 'delete_consulta'),
(44, 'Can view Consulta', 11, 'view_consulta'),
(45, 'Can add Receta', 12, 'add_receta'),
(46, 'Can change Receta', 12, 'change_receta'),
(47, 'Can delete Receta', 12, 'delete_receta'),
(48, 'Can view Receta', 12, 'view_receta'),
(49, 'Can add Perfil de Usuario', 13, 'add_perfilusuario'),
(50, 'Can change Perfil de Usuario', 13, 'change_perfilusuario'),
(51, 'Can delete Perfil de Usuario', 13, 'delete_perfilusuario'),
(52, 'Can view Perfil de Usuario', 13, 'view_perfilusuario'),
(53, 'Can add horario doctor', 14, 'add_horariodoctor'),
(54, 'Can change horario doctor', 14, 'change_horariodoctor'),
(55, 'Can delete horario doctor', 14, 'delete_horariodoctor'),
(56, 'Can view horario doctor', 14, 'view_horariodoctor');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$600000$QSccWSBpoPYEeWnmr9b4h7$YitH2/1+15eW7iYy4bw8Fa1k/rtmmRD+WascCLnaDVA=', '2026-03-20 03:46:46.008308', 1, 'abeld', 'Abel', 'Diaz', 'eliuabel09@gmail.com', 1, 1, '2026-03-10 00:16:29.629590'),
(2, 'pbkdf2_sha256$600000$LsNNA1vNufVCDubEMSGzmC$SLTjJb4TGwtQ0J9AHQWpthrcDyDKstS54c73If2si1Y=', '2026-03-30 21:50:38.164649', 0, 'eliu', 'abel', 'diaz', 'abel@gmail.com', 0, 1, '2026-03-10 16:06:54.284841'),
(5, 'pbkdf2_sha256$600000$MhWAIKkfd8z2bGQ0R8eYaN$npCSvy3fc/xDq4B9Y4x+YY7m/EOI96Jp0adZWM0az1w=', '2026-03-12 18:10:56.953265', 0, 'jostin', 'jostin', 'ruiz', 'jostin123@gmail.com', 0, 1, '2026-03-10 16:25:35.114554');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `citas`
--

CREATE TABLE `citas` (
  `id` int(10) UNSIGNED NOT NULL,
  `paciente_id` int(10) UNSIGNED NOT NULL,
  `doctor_id` bigint(20) DEFAULT NULL,
  `fecha_hora` datetime NOT NULL,
  `duracion_min` smallint(5) UNSIGNED NOT NULL DEFAULT 30,
  `tipo` varchar(20) NOT NULL DEFAULT 'PRIMERA_VEZ',
  `estado` varchar(15) NOT NULL DEFAULT 'PENDIENTE',
  `motivo` text NOT NULL DEFAULT '',
  `notas_admin` text NOT NULL DEFAULT '',
  `informe_doctor` longtext DEFAULT NULL,
  `informe_fecha` datetime DEFAULT NULL
) ;

--
-- Volcado de datos para la tabla `citas`
--

INSERT INTO `citas` (`id`, `paciente_id`, `doctor_id`, `fecha_hora`, `duracion_min`, `tipo`, `estado`, `motivo`, `notas_admin`, `informe_doctor`, `informe_fecha`) VALUES
(1, 1, NULL, '2026-03-06 11:25:00', 30, 'SEGUIMIENTO', 'CONFIRMADA', 'aa', 'paso algo', NULL, NULL),
(2, 1, 3, '2026-03-27 18:24:00', 50, 'SEGUIMIENTO', 'COMPLETADA', 'aaa', 'aa', '', NULL),
(6, 24, 3, '2026-03-12 01:35:00', 30, 'URGENCIA', 'COMPLETADA', 'dolor de cabeza', 'si', 'si', '2026-03-11 01:36:19'),
(7, 24, 3, '2026-03-12 13:17:00', 30, 'PRIMERA_VEZ', 'COMPLETADA', 'a', 'a', '', NULL),
(8, 24, NULL, '2026-03-12 13:00:00', 15, 'SEGUIMIENTO', 'CONFIRMADA', '', '', '', NULL),
(9, 23, NULL, '2026-03-12 13:00:00', 15, 'PRIMERA_VEZ', 'CONFIRMADA', '', '', '', NULL),
(10, 19, 3, '2026-03-12 13:00:00', 15, 'PRIMERA_VEZ', 'COMPLETADA', '', '', '', NULL),
(11, 21, 3, '2026-03-13 13:00:00', 15, 'PRIMERA_VEZ', 'CONFIRMADA', '', '', '', NULL),
(12, 19, NULL, '2026-03-13 17:20:00', 15, 'PRIMERA_VEZ', 'CONFIRMADA', '', '', '', NULL),
(13, 25, 3, '2026-03-19 13:00:00', 15, 'PRIMERA_VEZ', 'CONFIRMADA', '', '', '', NULL),
(14, 23, 3, '2026-03-20 13:00:00', 15, 'PRIMERA_VEZ', 'COMPLETADA', '', '', 'aa', '2026-03-19 21:47:18');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `consultas`
--

CREATE TABLE `consultas` (
  `id` int(10) UNSIGNED NOT NULL,
  `cita_id` int(10) UNSIGNED DEFAULT NULL,
  `paciente_id` int(10) UNSIGNED NOT NULL,
  `doctor_id` int(11) NOT NULL,
  `fecha` datetime NOT NULL DEFAULT current_timestamp(),
  `peso_kg` decimal(5,2) DEFAULT NULL,
  `talla_cm` decimal(5,2) DEFAULT NULL,
  `presion_arterial` varchar(10) NOT NULL DEFAULT '',
  `frecuencia_cardiaca` smallint(5) UNSIGNED DEFAULT NULL,
  `temperatura` decimal(4,1) DEFAULT NULL,
  `saturacion_o2` tinyint(3) UNSIGNED DEFAULT NULL,
  `subjetivo` text NOT NULL,
  `objetivo` text NOT NULL,
  `diagnostico` text NOT NULL,
  `plan` text NOT NULL,
  `evolucion` text NOT NULL DEFAULT '',
  `proxima_cita` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `consultas`
--

INSERT INTO `consultas` (`id`, `cita_id`, `paciente_id`, `doctor_id`, `fecha`, `peso_kg`, `talla_cm`, `presion_arterial`, `frecuencia_cardiaca`, `temperatura`, `saturacion_o2`, `subjetivo`, `objetivo`, `diagnostico`, `plan`, `evolucion`, `proxima_cita`) VALUES
(1, 1, 1, 0, '2026-03-10 04:24:02', 70.60, 172.00, '120/80', 70, 34.0, 99, 'a', 'a', 'aa', 'a', 'a', '2026-03-19'),
(2, 2, 1, 3, '2026-03-10 16:34:17', NULL, NULL, '', NULL, NULL, NULL, 'a', 'a', 'a', 'a', 'a', NULL),
(3, 7, 24, 3, '2026-03-11 09:15:18', NULL, NULL, '', NULL, NULL, NULL, 'a', 'zZ', 'A', 'A', '', NULL),
(4, 10, 19, 3, '2026-03-11 17:39:52', NULL, NULL, '', NULL, NULL, NULL, 'a', 'a', 'a', 'a', 'a', NULL),
(5, 6, 24, 3, '2026-03-11 17:43:30', NULL, NULL, '', NULL, NULL, NULL, 'dolor de cabeza', 'a', 'a', 'a', 'a', NULL),
(6, 14, 23, 3, '2026-03-19 21:47:30', NULL, NULL, '', NULL, NULL, NULL, 'a', 'a', 'a', 'a', 'a', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(10, 'citas', 'cita'),
(9, 'citas', 'doctor'),
(14, 'citas', 'horariodoctor'),
(11, 'consultas', 'consulta'),
(12, 'consultas', 'receta'),
(5, 'contenttypes', 'contenttype'),
(13, 'core', 'perfilusuario'),
(8, 'pacientes', 'archivoclinico'),
(7, 'pacientes', 'paciente'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2026-03-09 23:41:30.036307'),
(2, 'auth', '0001_initial', '2026-03-09 23:41:30.830398'),
(3, 'admin', '0001_initial', '2026-03-09 23:41:31.097243'),
(4, 'admin', '0002_logentry_remove_auto_add', '2026-03-09 23:41:31.107452'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2026-03-09 23:41:31.118055'),
(6, 'contenttypes', '0002_remove_content_type_name', '2026-03-09 23:41:31.292569'),
(7, 'auth', '0002_alter_permission_name_max_length', '2026-03-09 23:41:31.360884'),
(8, 'auth', '0003_alter_user_email_max_length', '2026-03-09 23:41:31.378884'),
(9, 'auth', '0004_alter_user_username_opts', '2026-03-09 23:41:31.388429'),
(10, 'auth', '0005_alter_user_last_login_null', '2026-03-09 23:41:31.447669'),
(11, 'auth', '0006_require_contenttypes_0002', '2026-03-09 23:41:31.452095'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2026-03-09 23:41:31.460676'),
(13, 'auth', '0008_alter_user_username_max_length', '2026-03-09 23:41:31.566186'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2026-03-09 23:41:31.599814'),
(15, 'auth', '0010_alter_group_name_max_length', '2026-03-09 23:41:31.624602'),
(16, 'auth', '0011_update_proxy_permissions', '2026-03-09 23:41:31.644239'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2026-03-09 23:41:31.662381'),
(18, 'sessions', '0001_initial', '2026-03-09 23:41:31.702285'),
(19, 'pacientes', '0001_initial', '2026-03-10 03:56:29.969150'),
(20, 'citas', '0001_initial', '2026-03-10 03:56:29.980572'),
(21, 'consultas', '0001_initial', '2026-03-10 03:56:29.993009'),
(22, 'core', '0001_initial', '2026-03-10 07:03:59.915611'),
(23, 'citas', '0002 citas fixed ', '2026-03-11 01:56:47.772650'),
(24, 'citas', '0003_remove_cita_citas_fecha_h_117be1_idx_and_more', '2026-03-11 01:57:38.806388'),
(25, 'citas', '0004_horariodoctor', '2026-03-11 16:09:29.108443'),
(26, 'citas', '0005_alter_cita_informe_doctor_and_more', '2026-03-11 16:09:29.115202'),
(27, 'pacientes', '0002_paciente_dni', '2026-03-11 16:11:05.221893'),
(28, 'citas', '0006_alter_cita_doctor', '2026-03-20 04:02:31.938321'),
(29, 'consultas', '0002_alter_consulta_doctor', '2026-03-20 04:07:34.107329');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('0jpg7zfvxnrk085m6s7ykqf10ld6wcil', '.eJxVjMsOwiAQAP-FsyE8XBY9eu83NMAuUjWQlPZk_HdD0oNeZybzFnPYtzLvndd5IXEVRpx-WQzpyXUIeoR6bzK1uq1LlCORh-1yasSv29H-DUroZWzBOtQMznqfFZrMBvWFFVmNTIwI0YC3kFLOZ-eS5gwIwEZR0Aq9-HwBvko3Jw:1w3LC6:l3KmpSgtMxhtDSgtyNDp7fBBw9g2wSlZdNkhKQ-ww9I', '2026-04-02 21:46:18.836432'),
('224wtbqu0cmmpb9mayb4lu4zn46a18xl', '.eJxVjMsOwiAQAP-FsyE8XBY9eu83NMAuUjWQlPZk_HdD0oNeZybzFnPYtzLvndd5IXEVRpx-WQzpyXUIeoR6bzK1uq1LlCORh-1yasSv29H-DUroZWzBOtQMznqfFZrMBvWFFVmNTIwI0YC3kFLOZ-eS5gwIwEZR0Aq9-HwBvko3Jw:1w3LA2:JMFP0Pz9Ueku3BHkBNRoShifNEazlDsHzlmum_EvNOM', '2026-04-02 21:44:10.709716'),
('75l827sltwyyn8s8ov0l8re9zgyuxxwu', '.eJxVjMsOwiAQAP-FsyE8XBY9eu83NMAuUjWQlPZk_HdD0oNeZybzFnPYtzLvndd5IXEVRpx-WQzpyXUIeoR6bzK1uq1LlCORh-1yasSv29H-DUroZWzBOtQMznqfFZrMBvWFFVmNTIwI0YC3kFLOZ-eS5gwIwEZR0Aq9-HwBvko3Jw:1w3LjQ:KQP_LXfXRDH5-1DkjNqIgx83k5l2r0PAF1dtB9Z1B9Q', '2026-04-02 22:20:44.111976'),
('87v3g7zmf1q05cpp5i1bazob9qk9pawz', '.eJxVjEEOgkAMAP_Ss9lAYcuWo3ffQFpaBDWQsHAy_t2QcNDrzGTe0Mm-jd2efe0mgxZKuPwylf7p8yHsIfN9Cf0yb-uk4UjCaXO4Leav69n-DUbJI7SgJMzRYkGckFKSVDQalZgHGrA0bKrSeDBlLiokFYw1opP3de0NOXy-wvk3Ng:1w3L9e:YLM6JmKxe4gkaBIVWPsj2M3nt6ZsW8j0cSFvgcelh0c', '2026-04-02 21:43:46.710066'),
('8vi4ococcvvcggvljazohpyb3trqegqz', '.eJxVjMsOwiAQAP-FsyE8XBY9eu83NMAuUjWQlPZk_HdD0oNeZybzFnPYtzLvndd5IXEVRpx-WQzpyXUIeoR6bzK1uq1LlCORh-1yasSv29H-DUroZWzBOtQMznqfFZrMBvWFFVmNTIwI0YC3kFLOZ-eS5gwIwEZR0Aq9-HwBvko3Jw:1w0s9R:X8d5lkzzjgJjSBGzjS6urE5q5Ipi9VbdNBn913uKj2w', '2026-03-27 02:21:21.682898'),
('bldygiz9ihgdukgdukh6y5lhl5kqrt09', '.eJxVjMsOwiAQAP-FsyE8XBY9eu83NMAuUjWQlPZk_HdD0oNeZybzFnPYtzLvndd5IXEVRpx-WQzpyXUIeoR6bzK1uq1LlCORh-1yasSv29H-DUroZWzBOtQMznqfFZrMBvWFFVmNTIwI0YC3kFLOZ-eS5gwIwEZR0Aq9-HwBvko3Jw:1w0XnF:etoIxPiZWW4v3FzUl-VX8kVFRy4TKCVd3FMzstBkm2o', '2026-03-26 04:37:05.258517'),
('d70rh8xghvhmopivdtpfij4prkc5qhzg', '.eJxVjMsOwiAQAP-FsyE8XBY9eu83NMAuUjWQlPZk_HdD0oNeZybzFnPYtzLvndd5IXEVRpx-WQzpyXUIeoR6bzK1uq1LlCORh-1yasSv29H-DUroZWzBOtQMznqfFZrMBvWFFVmNTIwI0YC3kFLOZ-eS5gwIwEZR0Aq9-HwBvko3Jw:1w3LjP:Xrsx6DcqH-WaqddAfWUzZXKnG57nSTB7L4_MD9dEfxk', '2026-04-02 22:20:43.952462'),
('dinnde7hg5e7t6e91o5grysk1ky0khya', '.eJxVjEEOgkAMAP_Ss9lAYcuWo3ffQFpaBDWQsHAy_t2QcNDrzGTe0Mm-jd2efe0mgxZKuPwylf7p8yHsIfN9Cf0yb-uk4UjCaXO4Leav69n-DUbJI7SgJMzRYkGckFKSVDQalZgHGrA0bKrSeDBlLiokFYw1opP3de0NOXy-wvk3Ng:1w3LDW:OnOgqiJk8pYVpIuz5YIfQjYPdC__jDJAfD-hsvamqtA', '2026-04-02 21:47:46.849025'),
('fzkhpgmz7zf4c23yd44eyw7rbx6ho5g9', '.eJxVjMsOwiAQAP-FsyE8XBY9eu83NMAuUjWQlPZk_HdD0oNeZybzFnPYtzLvndd5IXEVRpx-WQzpyXUIeoR6bzK1uq1LlCORh-1yasSv29H-DUroZWzBOtQMznqfFZrMBvWFFVmNTIwI0YC3kFLOZ-eS5gwIwEZR0Aq9-HwBvko3Jw:1w3LjQ:KQP_LXfXRDH5-1DkjNqIgx83k5l2r0PAF1dtB9Z1B9Q', '2026-04-02 22:20:44.198135'),
('h2cfmvks6xap87a6daxor8xdgp90r63r', '.eJxVjMsOwiAQAP-FsyE8XBY9eu83NMAuUjWQlPZk_HdD0oNeZybzFnPYtzLvndd5IXEVRpx-WQzpyXUIeoR6bzK1uq1LlCORh-1yasSv29H-DUroZWzBOtQMznqfFZrMBvWFFVmNTIwI0YC3kFLOZ-eS5gwIwEZR0Aq9-HwBvko3Jw:1w0s9R:X8d5lkzzjgJjSBGzjS6urE5q5Ipi9VbdNBn913uKj2w', '2026-03-27 02:21:21.531200'),
('i61cf0ktzbeduvlqwv7coacoonhpj200', '.eJxVjMsOwiAQAP-FsyE8XBY9eu83NMAuUjWQlPZk_HdD0oNeZybzFnPYtzLvndd5IXEVRpx-WQzpyXUIeoR6bzK1uq1LlCORh-1yasSv29H-DUroZWzBOtQMznqfFZrMBvWFFVmNTIwI0YC3kFLOZ-eS5gwIwEZR0Aq9-HwBvko3Jw:1w3LC6:l3KmpSgtMxhtDSgtyNDp7fBBw9g2wSlZdNkhKQ-ww9I', '2026-04-02 21:46:18.616403'),
('o9na6s6rgqzrnfn24hvnq9d757a5fmbt', '.eJxVjEEOgkAMAP_Ss9lAYcuWo3ffQFpaBDWQsHAy_t2QcNDrzGTe0Mm-jd2efe0mgxZKuPwylf7p8yHsIfN9Cf0yb-uk4UjCaXO4Leav69n-DUbJI7SgJMzRYkGckFKSVDQalZgHGrA0bKrSeDBlLiokFYw1opP3de0NOXy-wvk3Ng:1vzpaz:2-zNX6PU-4A_THsv4f9ZCn4rYihztomMKQCA_53wcQ0', '2026-03-24 05:25:29.159889'),
('rv8urywm6n1hqwpcm3jivtdl4yowuflr', '.eJxVjEEOgkAMAP_Ss9lAYcuWo3ffQFpaBDWQsHAy_t2QcNDrzGTe0Mm-jd2efe0mgxZKuPwylf7p8yHsIfN9Cf0yb-uk4UjCaXO4Leav69n-DUbJI7SgJMzRYkGckFKSVDQalZgHGrA0bKrSeDBlLiokFYw1opP3de0NOXy-wvk3Ng:1w3LBB:ldo5eprnZZmCjMqM-Oirhx4-1Z31I2kd89yDNXYpoV4', '2026-04-02 21:45:21.553010'),
('slx5ge6jzt07g1j8rdstu33gwj597dlu', '.eJxVjMsOwiAQAP-FsyE8XBY9eu83NMAuUjWQlPZk_HdD0oNeZybzFnPYtzLvndd5IXEVRpx-WQzpyXUIeoR6bzK1uq1LlCORh-1yasSv29H-DUroZWzBOtQMznqfFZrMBvWFFVmNTIwI0YC3kFLOZ-eS5gwIwEZR0Aq9-HwBvko3Jw:1w3Qor:yBIdEpb9dFeS57Mnj_iX-26pOHUeeRrW2gPdETfifvk', '2026-04-03 03:46:41.147808'),
('t3sghg0h40tn2rbaquotoxusa5oah2g6', '.eJxVjEEOgkAMAP_Ss9lAYcuWo3ffQFpaBDWQsHAy_t2QcNDrzGTe0Mm-jd2efe0mgxZKuPwylf7p8yHsIfN9Cf0yb-uk4UjCaXO4Leav69n-DUbJI7SgJMzRYkGckFKSVDQalZgHGrA0bKrSeDBlLiokFYw1opP3de0NOXy-wvk3Ng:1w0s9O:vGlxxvCf7EvWgnh8KQzt5TvtZ9o9i1dH8jc6EtpQ_4c', '2026-03-27 02:21:18.425546'),
('ta6vnrsd2x3p08odpve6xua2prcg00n0', '.eJxVjEEOgkAMAP_Ss9lAYcuWo3ffQFpaBDWQsHAy_t2QcNDrzGTe0Mm-jd2efe0mgxZKuPwylf7p8yHsIfN9Cf0yb-uk4UjCaXO4Leav69n-DUbJI7SgJMzRYkGckFKSVDQalZgHGrA0bKrSeDBlLiokFYw1opP3de0NOXy-wvk3Ng:1w3Qov:VclXs_-StogCdzJv92yP1Q4IiAs-OKKkQyPIlHu6Pls', '2026-04-03 03:46:45.620529'),
('zxq6k8zl2bwm918m5jgfbvl9zv666t0b', '.eJxVjEEOgkAMAP_Ss9lAYcuWo3ffQFpaBDWQsHAy_t2QcNDrzGTe0Mm-jd2efe0mgxZKuPwylf7p8yHsIfN9Cf0yb-uk4UjCaXO4Leav69n-DUbJI7SgJMzRYkGckFKSVDQalZgHGrA0bKrSeDBlLiokFYw1opP3de0NOXy-wvk3Ng:1w3Qov:VclXs_-StogCdzJv92yP1Q4IiAs-OKKkQyPIlHu6Pls', '2026-04-03 03:46:45.823369');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `doctores`
--

CREATE TABLE `doctores` (
  `id` int(10) UNSIGNED NOT NULL,
  `nombres` varchar(100) NOT NULL,
  `apellidos` varchar(100) NOT NULL,
  `especialidad` varchar(100) NOT NULL,
  `cedula` varchar(20) NOT NULL,
  `telefono` varchar(15) NOT NULL DEFAULT '',
  `email` varchar(254) NOT NULL DEFAULT '',
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  `usuario_id` int(11) DEFAULT NULL,
  `foto` varchar(100) DEFAULT NULL,
  `biografia` text DEFAULT NULL,
  `horario_atencion` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `doctores`
--

INSERT INTO `doctores` (`id`, `nombres`, `apellidos`, `especialidad`, `cedula`, `telefono`, `email`, `activo`, `usuario_id`, `foto`, `biografia`, `horario_atencion`) VALUES
(3, 'abel', 'diaz', 'Medicina General', '1220201010110', '9490211141', 'abel@gmail.com', 1, 2, 'doctores/WhatsApp_Image_2025-12-28_at_12.03.08_AM.jpeg', 'buen medico', ''),
(5, 'Carlos', 'Diaz', 'Cardiología', 'a', '969002122', 'eliuabel09@gmail.com', 0, NULL, '', '', ''),
(7, 'Josias', 'Calero', 'Estamotologia', 'CA-005670', '901091091', 'eliuabel09@gmail.com', 1, NULL, '', '', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `doctores_horarios`
--

CREATE TABLE `doctores_horarios` (
  `id` int(11) NOT NULL,
  `doctor_id` int(11) NOT NULL,
  `dia_semana` tinyint(4) NOT NULL COMMENT '0=Lun 1=Mar 2=Mie 3=Jue 4=Vie 5=Sab 6=Dom',
  `hora_inicio` time NOT NULL,
  `hora_fin` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `doctores_horarios`
--

INSERT INTO `doctores_horarios` (`id`, `doctor_id`, `dia_semana`, `hora_inicio`, `hora_fin`) VALUES
(54, 3, 0, '08:00:00', '14:00:00'),
(55, 3, 1, '08:00:00', '14:00:00'),
(56, 3, 2, '08:00:00', '14:00:00'),
(57, 3, 3, '08:00:00', '14:00:00'),
(58, 3, 4, '08:00:00', '14:00:00'),
(59, 3, 5, '08:00:00', '14:00:00'),
(72, 6, 0, '08:00:00', '14:00:00'),
(73, 6, 1, '08:00:00', '14:00:00'),
(74, 6, 2, '08:00:00', '14:00:00'),
(75, 6, 4, '08:00:00', '14:00:00'),
(76, 6, 5, '08:00:00', '14:00:00'),
(77, 6, 6, '08:00:00', '14:00:00'),
(78, 7, 1, '08:00:00', '14:00:00'),
(79, 7, 2, '08:00:00', '16:00:00'),
(80, 7, 3, '08:00:00', '16:00:00'),
(81, 7, 5, '08:00:00', '16:00:00'),
(82, 7, 6, '08:00:00', '14:00:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pacientes`
--

CREATE TABLE `pacientes` (
  `id` int(10) UNSIGNED NOT NULL,
  `nombres` varchar(100) NOT NULL,
  `apellidos` varchar(100) NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `sexo` char(1) NOT NULL COMMENT 'M=Masculino F=Femenino O=Otro',
  `curp` varchar(18) DEFAULT NULL,
  `dni` varchar(8) DEFAULT NULL,
  `tipo_sangre` varchar(3) NOT NULL DEFAULT '',
  `telefono` varchar(15) NOT NULL,
  `email` varchar(254) DEFAULT NULL,
  `direccion` text NOT NULL DEFAULT '',
  `alergias` text NOT NULL DEFAULT '',
  `antecedentes` text NOT NULL DEFAULT '',
  `enfermedades_cronicas` text NOT NULL DEFAULT '',
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  `fecha_registro` datetime NOT NULL DEFAULT current_timestamp(),
  `fecha_actualizacion` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ;

--
-- Volcado de datos para la tabla `pacientes`
--

INSERT INTO `pacientes` (`id`, `nombres`, `apellidos`, `fecha_nacimiento`, `sexo`, `curp`, `dni`, `tipo_sangre`, `telefono`, `email`, `direccion`, `alergias`, `antecedentes`, `enfermedades_cronicas`, `activo`, `fecha_registro`, `fecha_actualizacion`) VALUES
(1, 'Juan Pablo', 'García López', '1985-03-12', 'M', 'GALJ850312HDFRZN01', NULL, 'O+', '555-2001', 'jp.garcia@email.com', '', '', '', '', 1, '2026-03-09 18:00:31', '2026-03-09 18:00:31'),
(2, 'María Elena', 'Soto Vargas', '1992-07-25', 'F', 'SOVM920725MDFTRR02', NULL, 'A+', '555-2002', 'm.soto@email.com', '', '', '', '', 1, '2026-03-09 18:00:31', '2026-03-09 18:00:31'),
(19, 'Carlos Andrés', 'Quispe Huanca', '1978-11-05', 'M', 'QUHC781105HPESRN03', NULL, 'B+', '555-2003', 'c.quispe@email.com', 'Calle Real 789, Sullana', '', 'Padre con hipertensión', 'Hipertensión', 1, '2026-03-10 11:38:51', '2026-03-10 11:38:51'),
(20, 'Rosa Isabel', 'Flores Mendoza', '2000-04-18', 'F', 'FOMR000418MDFNRS04', NULL, 'AB+', '555-2004', 'r.flores@email.com', 'Urb. Santa Rosa 12, Sullana', 'Aspirina, Ibuprofeno', '', '', 1, '2026-03-10 11:38:51', '2026-03-10 11:38:51'),
(21, 'Luis Fernando', 'Ramos Chávez', '1965-09-30', 'M', 'RACL650930HPEMNS05', NULL, 'O-', '555-2005', 'l.ramos@email.com', 'Jr. Tacna 321, Sullana', '', 'Hermano con diabetes', 'Diabetes, Asma', 1, '2026-03-10 11:38:51', '2026-03-10 11:38:51'),
(22, 'Ana Sofía', 'Torres Villegas', '1995-12-14', 'F', 'TOVA951214MDFRNNA0', NULL, 'A-', '555-2006', 'a.torres@email.com', 'Av. Grau 654, Sullana', 'Látex', '', '', 1, '2026-03-10 11:38:51', '2026-03-10 11:38:51'),
(23, 'Pedro Antonio', 'Núñez Salinas', '1950-06-22', 'M', 'NUSP500622HPEZDRN0', NULL, 'B-', '555-2007', 'p.nunez@email.com', 'Calle Piura 987, Sullana', 'Sulfas', 'Padre con cáncer', 'Hipertensión, EPOC', 1, '2026-03-10 11:38:51', '2026-03-10 11:38:51'),
(24, 'Lucía Beatriz', 'Castro Reyes', '1988-02-08', 'F', 'CARL880208MDFSTR08', NULL, 'A+', '555-2008', 'l.castro@email.com', 'Jr. Arequipa 147, Sullana', '', '', '', 1, '2026-03-10 11:38:51', '2026-03-10 11:38:51'),
(25, 'Juan', 'Diaz', '2026-03-02', 'M', 'EHEHE', NULL, 'A+', '949021141', 'eliuabel09@gmail.com', 'manuel seoane manzana a 21', '', '', '', 1, '2026-03-10 16:45:47', '2026-03-10 16:45:47'),
(26, 'Carlos', 'Garcia', '1990-05-17', 'M', NULL, '61095087', 'O+', '969002122', 'eliuabel09@gmail.com', 'manuel seoane manzana a 21', 'tuvo cancer', '', 'cort de vista', 1, '2026-03-11 02:04:38', '2026-03-11 02:04:38');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `perfiles_usuario`
--

CREATE TABLE `perfiles_usuario` (
  `id` bigint(20) NOT NULL,
  `rol` varchar(20) NOT NULL,
  `usuario_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `perfiles_usuario`
--

INSERT INTO `perfiles_usuario` (`id`, `rol`, `usuario_id`) VALUES
(1, 'ADMIN', 1),
(2, 'DOCTOR', 2),
(4, 'SECRETARIA', 5);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `recetas`
--

CREATE TABLE `recetas` (
  `id` int(10) UNSIGNED NOT NULL,
  `consulta_id` int(10) UNSIGNED NOT NULL,
  `medicamento` varchar(200) NOT NULL,
  `dosis` varchar(100) NOT NULL,
  `frecuencia` varchar(100) NOT NULL,
  `duracion` varchar(100) NOT NULL,
  `indicaciones` text NOT NULL DEFAULT '',
  `orden` tinyint(3) UNSIGNED NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `recetas`
--

INSERT INTO `recetas` (`id`, `consulta_id`, `medicamento`, `dosis`, `frecuencia`, `duracion`, `indicaciones`, `orden`) VALUES
(1, 1, 'eso', 's', 's', '20', '2', 1),
(2, 2, 'eso', 'a', 'a', '10', 'a', 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `archivos_clinicos`
--
ALTER TABLE `archivos_clinicos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_paciente` (`paciente_id`);

--
-- Indices de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indices de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indices de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `citas`
--
ALTER TABLE `citas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_fecha_estado` (`fecha_hora`,`estado`),
  ADD KEY `idx_paciente_cita` (`paciente_id`,`estado`),
  ADD KEY `idx_doctor_fecha` (`doctor_id`,`fecha_hora`);

--
-- Indices de la tabla `consultas`
--
ALTER TABLE `consultas`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `cita_id` (`cita_id`),
  ADD KEY `idx_consulta_paciente` (`paciente_id`,`fecha`),
  ADD KEY `fk_consulta_doctor` (`doctor_id`);

--
-- Indices de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indices de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indices de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indices de la tabla `doctores`
--
ALTER TABLE `doctores`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `cedula` (`cedula`),
  ADD KEY `idx_doctor_nombre` (`apellidos`,`nombres`),
  ADD KEY `fk_doctor_usuario` (`usuario_id`);

--
-- Indices de la tabla `doctores_horarios`
--
ALTER TABLE `doctores_horarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `horario_unico` (`doctor_id`,`dia_semana`),
  ADD KEY `idx_doctor_id` (`doctor_id`);

--
-- Indices de la tabla `pacientes`
--
ALTER TABLE `pacientes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `curp` (`curp`),
  ADD KEY `idx_nombre` (`apellidos`,`nombres`),
  ADD KEY `idx_curp` (`curp`);

--
-- Indices de la tabla `perfiles_usuario`
--
ALTER TABLE `perfiles_usuario`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `recetas`
--
ALTER TABLE `recetas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_receta_consulta` (`consulta_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `archivos_clinicos`
--
ALTER TABLE `archivos_clinicos`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=57;

--
-- AUTO_INCREMENT de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `citas`
--
ALTER TABLE `citas`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `consultas`
--
ALTER TABLE `consultas`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT de la tabla `doctores`
--
ALTER TABLE `doctores`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `doctores_horarios`
--
ALTER TABLE `doctores_horarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=83;

--
-- AUTO_INCREMENT de la tabla `pacientes`
--
ALTER TABLE `pacientes`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `perfiles_usuario`
--
ALTER TABLE `perfiles_usuario`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `recetas`
--
ALTER TABLE `recetas`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `archivos_clinicos`
--
ALTER TABLE `archivos_clinicos`
  ADD CONSTRAINT `fk_archivo_paciente` FOREIGN KEY (`paciente_id`) REFERENCES `pacientes` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Filtros para la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `citas`
--
ALTER TABLE `citas`
  ADD CONSTRAINT `fk_cita_paciente` FOREIGN KEY (`paciente_id`) REFERENCES `pacientes` (`id`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `consultas`
--
ALTER TABLE `consultas`
  ADD CONSTRAINT `fk_consulta_cita` FOREIGN KEY (`cita_id`) REFERENCES `citas` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_consulta_paciente` FOREIGN KEY (`paciente_id`) REFERENCES `pacientes` (`id`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `doctores`
--
ALTER TABLE `doctores`
  ADD CONSTRAINT `fk_doctor_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `perfiles_usuario`
--
ALTER TABLE `perfiles_usuario`
  ADD CONSTRAINT `perfiles_usuario_usuario_id_23dac70b_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `recetas`
--
ALTER TABLE `recetas`
  ADD CONSTRAINT `fk_receta_consulta` FOREIGN KEY (`consulta_id`) REFERENCES `consultas` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

-- ============================================================
--  INSERT: Nuevos pacientes (IDs 27–36) + 40 citas (13-17 abril 2026)
--  Doctores activos:
--    id=3  → abel diaz       (Medicina General)
--    id=7  → Josias Calero   (Estomatología)
-- ============================================================
 
-- ------------------------------------------------------------
-- 1. NUEVOS PACIENTES (10 pacientes, IDs 27-36)
-- ------------------------------------------------------------
INSERT INTO `pacientes`
  (`id`, `nombres`, `apellidos`, `fecha_nacimiento`, `sexo`, `curp`, `dni`,
   `tipo_sangre`, `telefono`, `email`, `direccion`, `alergias`,
   `antecedentes`, `enfermedades_cronicas`, `activo`, `fecha_registro`, `fecha_actualizacion`)
VALUES
(27, 'Valeria',    'Morales Rivas',    '1997-04-10', 'F', 'MORV970410MDFRVL01', '74521036', 'B+',  '973001101', 'v.morales@email.com',   'Urb. Los Pinos 34, Sullana',       '',             '',                         '',                  1, '2026-04-10 08:00:00', '2026-04-10 08:00:00'),
(28, 'Miguel',     'Pacheco Llacsahuanga', '1982-08-22', 'M', 'PALM820822HPECNG02', '62013489', 'O+', '961002202', 'm.pacheco@email.com', 'Av. Buenos Aires 110, Sullana',    '',             'Padre con hipertensión',    'Hipertensión',      1, '2026-04-10 08:05:00', '2026-04-10 08:05:00'),
(29, 'Sofía',      'Aguilar Panta',    '2003-01-30', 'F', 'AGPS030130MDFNTS03', '75332210', 'A-',  '952003303', 's.aguilar@email.com',   'Jr. Libertad 56, Sullana',         'Penicilina',   '',                         '',                  1, '2026-04-10 08:10:00', '2026-04-10 08:10:00'),
(30, 'Roberto',    'Calle Ordinola',   '1970-06-15', 'M', 'CAOR700615HPELLS04', '40218876', 'AB-', '943004404', 'r.calle@email.com',     'Calle Tumbes 203, Sullana',        'Sulfas',       'Abuelo con diabetes',       'Diabetes tipo 2',   1, '2026-04-10 08:15:00', '2026-04-10 08:15:00'),
(31, 'Carmen',     'Silupu Chiroque',  '1960-11-02', 'F', 'SICC601102MDFPRS05', '17456892', 'O-',  '934005505', 'c.silupu@email.com',    'Urb. Bellavista 78, Sullana',      '',             'Madre con osteoporosis',    'Osteoporosis, HTA', 1, '2026-04-10 08:20:00', '2026-04-10 08:20:00'),
(32, 'Andrés',     'Zapata Feijoo',    '1990-03-25', 'M', 'ZAFA900325HPEPFN06', '71908834', 'A+',  '925006606', 'a.zapata@email.com',    'Jr. San Martín 44, Sullana',       '',             '',                         '',                  1, '2026-04-10 08:25:00', '2026-04-10 08:25:00'),
(33, 'Gabriela',   'Pingo Purizaca',   '2001-09-18', 'F', 'PIGB010918MDFNRG07', '76214390', 'B-',  '916007707', 'g.pingo@email.com',     'Av. Sullana 99, Sullana',          'Ibuprofeno',   '',                         '',                  1, '2026-04-10 08:30:00', '2026-04-10 08:30:00'),
(34, 'Fernando',   'Távara Córdova',   '1975-12-07', 'M', 'TACF751207HPEVRD08', '25318970', 'O+',  '907008808', 'f.tavara@email.com',    'Calle Piura 380, Sullana',         '',             'Sin antecedentes',          'Asma',              1, '2026-04-10 08:35:00', '2026-04-10 08:35:00'),
(35, 'Milagros',   'Huertas Balladares','1993-07-14','F', 'HUBM930714MDFRRG09', '72651048', 'A+',  '988009909', 'm.huertas@email.com',   'Jr. Grau 17, Sullana',             'Látex',        '',                         '',                  1, '2026-04-10 08:40:00', '2026-04-10 08:40:00'),
(36, 'José Luis',  'Vílchez Saavedra', '1955-02-28', 'M', 'VISJ550228HPELCS10', '09234561', 'B+',  '979010010', 'j.vilchez@email.com',   'Urb. Los Algarrobos 5, Sullana',   'Aspirina',     'Padre con EPOC',            'EPOC, HTA',         1, '2026-04-10 08:45:00', '2026-04-10 08:45:00');
 
 
-- ------------------------------------------------------------
-- 2. CITAS (40 citas, 13–17 abril 2026)
--    Doctores: 3 = abel diaz, 7 = Josias Calero
--    Pacientes existentes: 1,2,19,20,21,22,23,24,25,26
--    Pacientes nuevos: 27-36
--    IDs de cita desde 15 (el último registrado era 14)
-- ------------------------------------------------------------
INSERT INTO `citas`
  (`id`, `paciente_id`, `doctor_id`, `fecha_hora`, `duracion_min`, `tipo`,
   `estado`, `motivo`, `notas_admin`, `informe_doctor`, `informe_fecha`)
VALUES
 
-- ── LUNES 13 DE ABRIL ──────────────────────────────────────
 
-- Doctor 3 (abel diaz — Medicina General) mañana 08:00-14:00
(15,  1,  3, '2026-04-13 08:00:00', 30, 'SEGUIMIENTO',  'COMPLETADA',  'Control de presión arterial',          'Paciente puntual',     'Presión estable 120/80. Se indica continuar medicación.', '2026-04-13 08:35:00'),
(16, 19,  3, '2026-04-13 08:30:00', 30, 'SEGUIMIENTO',  'COMPLETADA',  'Control hipertensión',                  'Sin novedad',          'TA 135/85. Se ajusta dosis de losartán.', '2026-04-13 09:10:00'),
(17, 21,  3, '2026-04-13 09:00:00', 30, 'SEGUIMIENTO',  'COMPLETADA',  'Control diabetes',                      '',                     'Glucemia 145 mg/dl. Se refuerza dieta.', '2026-04-13 09:40:00'),
(18, 27,  3, '2026-04-13 09:30:00', 30, 'PRIMERA_VEZ',  'COMPLETADA',  'Dolor de garganta y fiebre',            '',                     'Faringitis aguda. Se receta amoxicilina 500mg.', '2026-04-13 10:05:00'),
(19, 28,  3, '2026-04-13 10:00:00', 30, 'PRIMERA_VEZ',  'COMPLETADA',  'Cefalea frecuente',                     'Derivado por urgencias','Cefalea tensional. Se indica analgésicos y relajantes.', '2026-04-13 10:45:00'),
(20, 29,  3, '2026-04-13 10:30:00', 30, 'PRIMERA_VEZ',  'COMPLETADA',  'Revisión general anual',                '',                     'Paciente sana. Exámenes de rutina solicitados.', '2026-04-13 11:05:00'),
(21, 30,  3, '2026-04-13 11:00:00', 45, 'SEGUIMIENTO',  'COMPLETADA',  'Control diabetes tipo 2',               '',                     'Glucemia en ayunas 160. Se solicita HbA1c.', '2026-04-13 11:55:00'),
(22, 31,  3, '2026-04-13 11:45:00', 30, 'SEGUIMIENTO',  'COMPLETADA',  'Dolor articular generalizado',          '',                     'Se indica densitometría y ajuste de calcio.', '2026-04-13 12:20:00'),
 
-- Doctor 7 (Josias Calero — Estomatología) mañana 08:00-14:00
(23, 22,  7, '2026-04-13 08:00:00', 30, 'PRIMERA_VEZ',  'COMPLETADA',  'Dolor molar superior derecho',         '',                     'Caries en pieza 17. Obturación realizada.', '2026-04-13 08:40:00'),
(24, 23,  7, '2026-04-13 09:00:00', 45, 'SEGUIMIENTO',  'COMPLETADA',  'Revisión post-extracción',              'Traer radiografía',    'Cicatrización correcta. Alta.', '2026-04-13 09:55:00'),
(25, 24,  7, '2026-04-13 10:00:00', 30, 'PRIMERA_VEZ',  'COMPLETADA',  'Limpieza dental y revisión',            '',                     'Sarro moderado. Profilaxis realizada.', '2026-04-13 10:35:00'),
 
-- ── MARTES 14 DE ABRIL ─────────────────────────────────────
 
-- Doctor 3 mañana
(26, 32,  3, '2026-04-14 08:00:00', 30, 'PRIMERA_VEZ',  'CONFIRMADA',  'Tos persistente hace 2 semanas',       '',                     NULL, NULL),
(27, 33,  3, '2026-04-14 08:30:00', 30, 'PRIMERA_VEZ',  'CONFIRMADA',  'Mareos y náuseas',                     '',                     NULL, NULL),
(28, 34,  3, '2026-04-14 09:00:00', 45, 'SEGUIMIENTO',  'CONFIRMADA',  'Control asma, revisión de inhalador',  '',                     NULL, NULL),
(29, 35,  3, '2026-04-14 09:45:00', 30, 'PRIMERA_VEZ',  'CONFIRMADA',  'Erupción cutánea en brazo derecho',    '',                     NULL, NULL),
(30, 36,  3, '2026-04-14 10:15:00', 45, 'SEGUIMIENTO',  'CONFIRMADA',  'Control EPOC e hipertensión',          'Traer espirometría',   NULL, NULL),
(31,  2,  3, '2026-04-14 11:00:00', 30, 'SEGUIMIENTO',  'CONFIRMADA',  'Revisión resultado exámenes laboratorio','',                   NULL, NULL),
 
-- Doctor 7 (Estomatología) — martes atiende 08:00-14:00
(32, 25,  7, '2026-04-14 08:00:00', 30, 'PRIMERA_VEZ',  'CONFIRMADA',  'Dolor encías',                         '',                     NULL, NULL),
(33, 26,  7, '2026-04-14 09:00:00', 30, 'SEGUIMIENTO',  'CONFIRMADA',  'Control ortodoncia',                   '',                     NULL, NULL),
(34, 27,  7, '2026-04-14 10:00:00', 45, 'PRIMERA_VEZ',  'CONFIRMADA',  'Revisión sensibilidad dental',         '',                     NULL, NULL),
 
-- ── MIÉRCOLES 15 DE ABRIL ──────────────────────────────────
 
-- Doctor 3 mañana
(35,  1,  3, '2026-04-15 08:00:00', 30, 'SEGUIMIENTO',  'PENDIENTE',   'Control mensual presión',              '',                     NULL, NULL),
(36, 20,  3, '2026-04-15 08:30:00', 30, 'SEGUIMIENTO',  'PENDIENTE',   'Revisión resultado alergia',           '',                     NULL, NULL),
(37, 28,  3, '2026-04-15 09:00:00', 30, 'SEGUIMIENTO',  'PENDIENTE',   'Evaluación cefalea post-tratamiento',  '',                     NULL, NULL),
(38, 30,  3, '2026-04-15 09:30:00', 30, 'SEGUIMIENTO',  'PENDIENTE',   'Control glucemia',                     '',                     NULL, NULL),
(39, 32,  3, '2026-04-15 10:00:00', 30, 'SEGUIMIENTO',  'PENDIENTE',   'Seguimiento tos, ver resultados',      '',                     NULL, NULL),
(40, 33,  3, '2026-04-15 10:30:00', 15, 'URGENCIA',     'PENDIENTE',   'Mareo fuerte con vómito',              'Prioridad alta',       NULL, NULL),
 
-- Doctor 7 (Estomatología) miércoles 08:00-16:00
(41, 22,  7, '2026-04-15 08:00:00', 30, 'SEGUIMIENTO',  'PENDIENTE',   'Revisión obturación pieza 17',         '',                     NULL, NULL),
(42, 29,  7, '2026-04-15 09:00:00', 60, 'PRIMERA_VEZ',  'PENDIENTE',   'Ortodoncia, evaluación inicial',       '',                     NULL, NULL),
(43, 36,  7, '2026-04-15 10:30:00', 30, 'PRIMERA_VEZ',  'PENDIENTE',   'Dolor en prótesis dental',             '',                     NULL, NULL),
 
-- ── JUEVES 16 DE ABRIL ─────────────────────────────────────
 
-- Doctor 3 mañana
(44, 21,  3, '2026-04-16 08:00:00', 30, 'SEGUIMIENTO',  'PENDIENTE',   'Control glucemia y HbA1c',             '',                     NULL, NULL),
(45, 23,  3, '2026-04-16 08:30:00', 30, 'SEGUIMIENTO',  'PENDIENTE',   'Revisión presión y EPOC',              '',                     NULL, NULL),
(46, 34,  3, '2026-04-16 09:00:00', 30, 'SEGUIMIENTO',  'PENDIENTE',   'Control asma, nueva espirometría',     '',                     NULL, NULL),
(47, 35,  3, '2026-04-16 09:30:00', 30, 'SEGUIMIENTO',  'PENDIENTE',   'Revisión erupción cutánea',            '',                     NULL, NULL),
(48, 31,  3, '2026-04-16 10:00:00', 30, 'SEGUIMIENTO',  'PENDIENTE',   'Resultados densitometría',             '',                     NULL, NULL),
(49, 19,  3, '2026-04-16 10:30:00', 30, 'SEGUIMIENTO',  'PENDIENTE',   'Control TA, revisión mensual',         '',                     NULL, NULL),
 
-- Doctor 7 (Estomatología) jueves 08:00-16:00
(50, 25,  7, '2026-04-16 08:00:00', 45, 'SEGUIMIENTO',  'PENDIENTE',   'Limpieza profunda y revisión encías',  '',                     NULL, NULL),
(51, 33,  7, '2026-04-16 09:30:00', 30, 'PRIMERA_VEZ',  'PENDIENTE',   'Revisión caries múltiple',             '',                     NULL, NULL),
(52, 35,  7, '2026-04-16 11:00:00', 30, 'PRIMERA_VEZ',  'PENDIENTE',   'Dolor mandíbula lado izquierdo',       '',                     NULL, NULL),
 
-- ── VIERNES 17 DE ABRIL ────────────────────────────────────
 
-- Doctor 3 mañana
(53,  2,  3, '2026-04-17 08:00:00', 30, 'SEGUIMIENTO',  'PENDIENTE',   'Control anemia, resultado ferritina',  '',                     NULL, NULL),
(54, 24,  3, '2026-04-17 08:30:00', 30, 'SEGUIMIENTO',  'PENDIENTE',   'Revisión general, chequeo anual',      '',                     NULL, NULL),
(55, 26,  3, '2026-04-17 09:00:00', 30, 'PRIMERA_VEZ',  'PENDIENTE',   'Dolor lumbar crónico',                 '',                     NULL, NULL),
(56, 36,  3, '2026-04-17 09:30:00', 30, 'URGENCIA',     'PENDIENTE',   'Dificultad respiratoria leve',         'Monitorear O2',        NULL, NULL),
(57, 20,  3, '2026-04-17 10:00:00', 30, 'SEGUIMIENTO',  'PENDIENTE',   'Control post-tratamiento alérgico',    '',                     NULL, NULL),
 
-- Doctor 7 (Estomatología) — viernes NO atiende (sin horario registrado)
-- Por ello las últimas 3 citas del viernes van al doctor 3
(58, 29,  3, '2026-04-17 10:30:00', 30, 'SEGUIMIENTO',  'PENDIENTE',   'Seguimiento faringitis, alta esperada','',                     NULL, NULL),
(59, 31,  3, '2026-04-17 11:00:00', 30, 'SEGUIMIENTO',  'PENDIENTE',   'Revisión osteoporosis, ajuste calcio', '',                     NULL, NULL),
(60, 32,  3, '2026-04-17 11:30:00', 30, 'SEGUIMIENTO',  'PENDIENTE',   'Resultado radiografía de tórax',       '',                     NULL, NULL);
 
 
-- ============================================================
-- RESUMEN
--   Pacientes nuevos insertados : 10 (IDs 27–36)
--   Citas insertadas             : 46 filas (IDs 15–60)
--     · 13 abril  : 11 citas  (8 dr. 3 | 3 dr. 7)  — COMPLETADAS
--     · 14 abril  : 9  citas  (6 dr. 3 | 3 dr. 7)  — CONFIRMADAS
--     · 15 abril  : 9  citas  (6 dr. 3 | 3 dr. 7)  — PENDIENTES
--     · 16 abril  : 9  citas  (6 dr. 3 | 3 dr. 7)  — PENDIENTES
--     · 17 abril  : 8  citas  (8 dr. 3)             — PENDIENTES
-- ============================================================