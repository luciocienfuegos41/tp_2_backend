-- tp_backend.partidos definition

CREATE TABLE `partidos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `equipo_local` varchar(50) NOT NULL,
  `equipo_visitante` varchar(50) NOT NULL,
  `goles_local` int DEFAULT NULL,
  `goles_visitante` int DEFAULT NULL,
  `estadio` varchar(70) DEFAULT NULL,
  `fase` varchar(50) NOT NULL,
  `ciudad` varchar(70) DEFAULT NULL,
  `fecha` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- tp_backend.usuarios definition

CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `email` varchar(70) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- tp_backend.prediccion definition

CREATE TABLE `prediccion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `id_partido` int NOT NULL,
  `goles_local` int NOT NULL,
  `goles_visitante` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_usuario` (`id_usuario`,`id_partido`),
  KEY `id_partido` (`id_partido`),
  CONSTRAINT `prediccion_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `prediccion_ibfk_2` FOREIGN KEY (`id_partido`) REFERENCES `partidos` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

