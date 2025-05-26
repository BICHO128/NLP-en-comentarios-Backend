CREATE DATABASE  IF NOT EXISTS `nlp_comentarios` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `nlp_comentarios`;
-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: nlp_comentarios
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('b85bd07b860c');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comentario`
--

DROP TABLE IF EXISTS `comentario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comentario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `texto` text NOT NULL,
  `sentimiento` varchar(20) DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comentario`
--

LOCK TABLES `comentario` WRITE;
/*!40000 ALTER TABLE `comentario` DISABLE KEYS */;
/*!40000 ALTER TABLE `comentario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `curso`
--

DROP TABLE IF EXISTS `curso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `curso` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `docente_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `docente_id` (`docente_id`),
  CONSTRAINT `curso_ibfk_1` FOREIGN KEY (`docente_id`) REFERENCES `docente` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `curso`
--

LOCK TABLES `curso` WRITE;
/*!40000 ALTER TABLE `curso` DISABLE KEYS */;
INSERT INTO `curso` VALUES (1,'Ingeniería de Software II',1),(2,'Probabilidad y Estadística',2),(3,'Base de Datos II',3),(4,'Desarrollo Web',3),(5,'Base de Datos II',4),(6,'Complejidad Algorítmica',4),(7,'Inglés III',5);
/*!40000 ALTER TABLE `curso` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `docente`
--

DROP TABLE IF EXISTS `docente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `docente` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(120) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `docente`
--

LOCK TABLES `docente` WRITE;
/*!40000 ALTER TABLE `docente` DISABLE KEYS */;
INSERT INTO `docente` VALUES (1,'Ana Maria Caviedes Castillo','ana.caviedes.c@uniautonoma.edu.co'),(2,'Jose Fernando Concha Gonzalez','jose.concha.g@uniautonoma.edu.co'),(3,'Ana Gabriela Fernandez Morantes','ana.fernandez.m@uniautonoma.edu.co'),(4,'Diego Fernando Prado Osorio','diego.prado.o@uniautonoma.edu.co'),(5,'Diana Patricia Garzon Muñoz','diana.garzon.m@uniautonoma.edu.co');
/*!40000 ALTER TABLE `docente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estudiante`
--

DROP TABLE IF EXISTS `estudiante`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estudiante` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(120) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estudiante`
--

LOCK TABLES `estudiante` WRITE;
/*!40000 ALTER TABLE `estudiante` DISABLE KEYS */;
INSERT INTO `estudiante` VALUES (1,'David Urrutia Ceron','david.urrutia.c@uniautonoma.edu.co'),(2,'Deiby Alejandro Ramirez Galvis','deiby.ramirez.g@uniautonoma.edu.co'),(3,'Thomas Montoya Magon','thomas.montoya.m@uniautonoma.edu.co'),(4,'Luisa Jhulieth Joaqui Jimenez','luisa.joaqui.j@uniautonoma.edu.co'),(5,'Daviel Rivas Agredo','daniel.rivas.a@uniautonoma.edu.co');
/*!40000 ALTER TABLE `estudiante` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `evaluacion`
--

DROP TABLE IF EXISTS `evaluacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `evaluacion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `docente_id` int NOT NULL,
  `curso_id` int NOT NULL,
  `satisfaccion_general` varchar(20) DEFAULT NULL,
  `metodologia` varchar(20) DEFAULT NULL,
  `comunicacion` varchar(20) DEFAULT NULL,
  `material_didactico` varchar(20) DEFAULT NULL,
  `puntualidad` varchar(20) DEFAULT NULL,
  `respeto` varchar(20) DEFAULT NULL,
  `organizacion` varchar(20) DEFAULT NULL,
  `claridad` varchar(20) DEFAULT NULL,
  `retroalimentacion` varchar(20) DEFAULT NULL,
  `disponibilidad` varchar(20) DEFAULT NULL,
  `comentario_docente` text,
  `sentimiento_docente` varchar(50) DEFAULT NULL,
  `comentario_curso` text,
  `sentimiento_curso` varchar(50) DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  `estudiante_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `curso_id` (`curso_id`),
  KEY `docente_id` (`docente_id`),
  KEY `estudiante_id` (`estudiante_id`),
  CONSTRAINT `evaluacion_ibfk_1` FOREIGN KEY (`curso_id`) REFERENCES `curso` (`id`),
  CONSTRAINT `evaluacion_ibfk_2` FOREIGN KEY (`docente_id`) REFERENCES `docente` (`id`),
  CONSTRAINT `evaluacion_ibfk_3` FOREIGN KEY (`estudiante_id`) REFERENCES `estudiante` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evaluacion`
--

LOCK TABLES `evaluacion` WRITE;
/*!40000 ALTER TABLE `evaluacion` DISABLE KEYS */;
INSERT INTO `evaluacion` VALUES (1,1,1,'excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','La profesora ha sido un maestro verdadero, con una capacidad para explicar conceptos complejos de manera sencilla y clara que es verdaderamente única. Ha sido un honor aprender de ella y he sentido que he crecido como persona gracias a su enseñanza. Su pasión por el tema es contagiosa y ha hecho que me sienta motivado para seguir aprendiendo y mejorando.','neutral','El curso ha sido una experiencia verdaderamente transformadora, con un contenido que ha sido fascinante y relevante. Me he sentido como si hubiera descubierto un nuevo mundo de conocimientos y habilidades.','neutral','2025-04-19 20:26:22',NULL),(2,1,1,'bueno','bueno','bueno','bueno','bueno','bueno','bueno','bueno','bueno','bueno','La profesora es muy amable y siempre está dispuesta a ayudar. El curso es interesante y me ha permitido aprender mucho. La forma en que se explica es clara y fácil de entender.','neutral','El curso es interesante y me ha permitido aprender mucho. La forma en que se explica es clara y fácil de entender.','neutral','2025-04-19 20:39:40',NULL),(3,1,1,'regular','regular','regular','regular','regular','regular','regular','regular','regular','regular','La profesora es buena, siempre está disponible para ayudar y explica las materias de manera clara.','neutral','El curso es regular, no es muy interesante pero sí es útil para aprender. La forma en que se explica es aceptable','neutral','2025-04-19 21:50:15',NULL),(4,1,1,'malo','malo','malo','malo','malo','malo','malo','malo','malo','malo','La profesora no es muy efectiva en la explicación de las materias y no está disponible cuando se necesita ayuda.','neutral','El curso es malo, no es interesante y no me ha permitido aprender mucho sobre el tema. La forma en que se explica es confusa y no es fácil de entender.','negativo','2025-04-19 21:51:59',NULL),(5,1,1,'pesimo','pesimo','pesimo','pesimo','pesimo','pesimo','pesimo','pesimo','pesimo','pesimo','La profesora es ineficiente en la explicación de las materias y no está disponible cuando se necesita ayuda. Su actitud es desconsiderada y no se preocupa por el bienestar de los estudiantes.','neutral','El curso es terrible, no es interesante y no me ha permitido aprender nada sobre el tema. La forma en que se explica es confusa y no es fácil de entender. La profesora no se toma la molestia de preparar las clases y no se preocupa por la calidad del aprendizaje.','negativo','2025-04-19 21:53:12',NULL),(6,2,2,'excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','Fercho es un profesor excepcional, muy dedicado y comprometido con el bienestar de sus estudiantes. Su forma de explicar las materias es clara y fácil de entender, siempre está disponible para ayudar y se preocupa por la calidad del aprendizaje. Es un verdadero líder y un ejemplo a seguir para todos los estudiantes.','neutral','La forma en que se explica es fascinante y siempre hay espacio para la discusión y la reflexión. Es un curso que recomendaría a todos los estudiantes sin duda.','neutral','2025-04-19 22:34:41',NULL);
/*!40000 ALTER TABLE `evaluacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `name` varchar(80) NOT NULL,
  `id` int NOT NULL,
  `users_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `users_id` (`users_id`),
  CONSTRAINT `roles_ibfk_1` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `username` varchar(80) NOT NULL,
  `email` varchar(80) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL,
  `first_name` varchar(30) DEFAULT NULL,
  `last_name` varchar(30) DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `is_admin` tinyint(1) DEFAULT NULL,
  `id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('Ana Maria Caviedes Castillo','ana.caviedes.c@uniautonoma.edu.co','$2b$12$8vsdzzKwekJ.CTPS0ucq8uRF7shCGlqi5SASB7jB2v8GcJ0maVSae','2025-04-18 11:58:01','Ana Maria','Caviedes Castillo',1,0,1),('Jose Fernando Concha Gonzalez','jose.concha.g@uniautonoma.edu.co','$2b$12$hmWLuRiFeMjQF9Ef2JbkBegu4e1HQwA9PNoi2E6Bgum/gO2Xa6cs.','2025-04-18 11:58:01','Jose Fernando','Concha Gonzalez',1,0,2),('Ana Gabriela Fernandez Morantes','ana.fernandez.m@uniautonoma.edu.co','$2b$12$0beWZoYgvRGfrSvmjwUW6.uF.dXIk6WB6AXB4AtsnrHr5jTM5Q2rG','2025-04-18 11:58:01','Ana Gabriela','Fernandez Morantes',1,0,3),('Diego Fernando Prado Osorios','diego.prado.o@uniautonoma.edu.co','$2b$12$WIHbv7PtK0kTtJe8wl77h.saQiTeUArcL.FLaJkRVuw1A6KD4sJE.','2025-04-18 11:58:01','Diego Fernando','Prado Osorios',1,0,4),('Diana Patricia Garzon Muñoz','diana.garzon.m@uniautonoma.edu.co','$2b$12$kRjTXdSYKfCthpImGNI3WuaY.2S9l7piA93e7mGvUbRH862bFcNaS','2025-04-18 11:58:02','Diana Patricia','Garzon Muñoz',1,0,5),('David Urrutia Ceron','david.urrutia.c@uniautonoma.edu.co','$2b$12$33q.bAD.FTNlFy57/thyf.Tj4It44IkBTN7wrInzj52miYs4WVmcm','2025-04-18 14:05:40','David','Urrutia Ceron',1,0,6),('Deiby Alejandro Ramirez Galvis','deiby.ramirez.g@uniautonoma.edu.co','$2b$12$e1aZQtlN3JxUF/CvWh1yfeZ0TcctBCfuVdfQsh98XuV8yItL7044W','2025-04-18 14:05:41','Deiby Alejandro','Ramirez Galvis',1,0,7),('Thomas Montoya Magon','thomas.montoya.m@uniautonoma.edu.co','$2b$12$yAZEVTz1ZjJ4Se8GFIZ7YeHzi2sXDvnRgIVk0Kb4QsjWggPlccCxC','2025-04-18 14:05:41','Thomas','Montoya Magon',1,0,8),('Luisa Jhulieth Joaqui Jimenez','luisa.joaqui.j@uniautonoma.edu.co','$2b$12$Q7PM9.m4uzEevx3NWeVDruGUJ3W4Mp6aif2wnlA/6HAzRmp7xQ2qi','2025-04-18 14:05:41','Luisa Jhulieth','Joaqui Jimenez',1,0,9),('Daviel Rivas Agredo','daniel.rivas.a@uniautonoma.edu.co','$2b$12$K0VZZ9sY4maWD7mjVVaR9.NeSG7oUNIwX.GxotdYry2HNLbEUCLg.','2025-04-18 14:05:41','Daniel','Rivas Agredo',1,0,10),('Administrador','admin@uniautonoma.edu.co','$2b$12$eNjuXa3SSO2VWh3PkHnP5eh4jDYEnT1a/IsmmXQey6efj/yUEFQqe','2025-04-18 22:09:10','Administrador','General',1,1,11);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-20 22:18:15
