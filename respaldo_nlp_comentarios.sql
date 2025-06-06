-- MySQL dump 10.13  Distrib 8.0.39, for Win64 (x86_64)
--
-- Host: localhost    Database: nlp_comentarios
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
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
INSERT INTO `curso` VALUES (1,'Ingenier├¡a de Software II',1),(2,'Probabilidad y Estad├¡stica',2),(3,'Base de Datos II',3),(4,'Desarrollo Web',3),(5,'Base de Datos II',4),(6,'Complejidad Algor├¡tmica',4),(7,'Ingl├®s III',5);
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
INSERT INTO `docente` VALUES (1,'Ana Maria Caviedes Castillo','ana.caviedes.c@uniautonoma.edu.co'),(2,'Jose Fernando Concha Gonzalez','jose.concha.g@uniautonoma.edu.co'),(3,'Ana Gabriela Fernandez Morantes','ana.fernandez.m@uniautonoma.edu.co'),(4,'Diego Fernando Prado Osorio','diego.prado.o@uniautonoma.edu.co'),(5,'Diana Patricia Garzon Mu├▒oz','diana.garzon.m@uniautonoma.edu.co');
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
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evaluacion`
--

LOCK TABLES `evaluacion` WRITE;
/*!40000 ALTER TABLE `evaluacion` DISABLE KEYS */;
INSERT INTO `evaluacion` VALUES (1,1,1,'excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','La profesora ha sido un maestro verdadero, con una capacidad para explicar conceptos complejos de manera sencilla y clara que es verdaderamente ├║nica. Ha sido un honor aprender de ella y he sentido que he crecido como persona gracias a su ense├▒anza. Su pasi├│n por el tema es contagiosa y ha hecho que me sienta motivado para seguir aprendiendo y mejorando.','neutral','El curso ha sido una experiencia verdaderamente transformadora, con un contenido que ha sido fascinante y relevante. Me he sentido como si hubiera descubierto un nuevo mundo de conocimientos y habilidades.','neutral','2025-04-19 20:26:22',NULL),(2,1,1,'bueno','bueno','bueno','bueno','bueno','bueno','bueno','bueno','bueno','bueno','La profesora es muy amable y siempre est├í dispuesta a ayudar. El curso es interesante y me ha permitido aprender mucho. La forma en que se explica es clara y f├ícil de entender.','neutral','El curso es interesante y me ha permitido aprender mucho. La forma en que se explica es clara y f├ícil de entender.','neutral','2025-04-19 20:39:40',NULL),(3,1,1,'regular','regular','regular','regular','regular','regular','regular','regular','regular','regular','La profesora es buena, siempre est├í disponible para ayudar y explica las materias de manera clara.','neutral','El curso es regular, no es muy interesante pero s├¡ es ├║til para aprender. La forma en que se explica es aceptable','neutral','2025-04-19 21:50:15',NULL),(4,1,1,'malo','malo','malo','malo','malo','malo','malo','malo','malo','malo','La profesora no es muy efectiva en la explicaci├│n de las materias y no est├í disponible cuando se necesita ayuda.','neutral','El curso es malo, no es interesante y no me ha permitido aprender mucho sobre el tema. La forma en que se explica es confusa y no es f├ícil de entender.','negativo','2025-04-19 21:51:59',NULL),(5,1,1,'pesimo','pesimo','pesimo','pesimo','pesimo','pesimo','pesimo','pesimo','pesimo','pesimo','La profesora es ineficiente en la explicaci├│n de las materias y no est├í disponible cuando se necesita ayuda. Su actitud es desconsiderada y no se preocupa por el bienestar de los estudiantes.','neutral','El curso es terrible, no es interesante y no me ha permitido aprender nada sobre el tema. La forma en que se explica es confusa y no es f├ícil de entender. La profesora no se toma la molestia de preparar las clases y no se preocupa por la calidad del aprendizaje.','negativo','2025-04-19 21:53:12',NULL),(6,2,2,'excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','Fercho es un profesor excepcional, muy dedicado y comprometido con el bienestar de sus estudiantes. Su forma de explicar las materias es clara y f├ícil de entender, siempre est├í disponible para ayudar y se preocupa por la calidad del aprendizaje. Es un verdadero l├¡der y un ejemplo a seguir para todos los estudiantes.','neutral','La forma en que se explica es fascinante y siempre hay espacio para la discusi├│n y la reflexi├│n. Es un curso que recomendar├¡a a todos los estudiantes sin duda.','neutral','2025-04-19 22:34:41',NULL),(7,2,2,'excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','Me gustar├¡a felicitarte por tu capacidad para explicar conceptos complejos de manera sencilla y clara. Has sido un profesor inspirador y has logrado que me sienta c├│modo y confiado en mi capacidad para aprender. Tu paciencia y dedicaci├│n han sido fundamentales para mi ├®xito en el curso.','neutral','Quiero expresar mi m├ís sincero agradecimiento por el curso que me has impartido. Has sido un maestro excepcional y has logrado que me sienta motivado y apasionado por el tema.','neutral','2025-04-21 10:03:21',NULL),(8,2,2,'excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','Eres un profesor muy bueno, explicas las cosas de manera sencilla y te tomas el tiempo para que entendamos. Me has hecho sentir c├│modo y seguro en la clase. ┬íMuchas gracias!','positivo','Quiero agradecerte mucho por el curso que me has dado. Ha sido muy interesante y me has ense├▒ado mucho.','neutral','2025-04-21 10:05:20',NULL),(9,2,2,'bueno','bueno','bueno','bueno','bueno','bueno','bueno','bueno','bueno','bueno','Eres un profesor de primera, me has hecho re├¡r, me has hecho pensar y me has hecho aprender. Tu entusiasmo y pasi├│n por el tema son contagiosos y me han hecho sentir como si estuviera en un viaje de descubrimiento. ┬íMuchas gracias por todo!','neutral','Eres un profesor muy bueno, explicas las cosas de manera sencilla y te tomas el tiempo para que entendamos. Me has hecho sentir c├│modo y seguro en la clase. ┬íMuchas gracias!','positivo','2025-04-21 10:07:45',NULL),(10,2,2,'malo','malo','malo','malo','malo','malo','malo','malo','malo','malo','Eres un profesor muy malo. No sabes explicar las cosas de manera clara, no te importa si los estudiantes entienden o no, y no te tomas el tiempo para ayudarnos. Me has hecho sentir frustrado y est├║pido. ┬íNo te recomiendo a nadie que te tome como profesor!','negativo','Lo siento, pero el curso ha sido un desastre. Me has hecho perder mi tiempo y no he aprendido nada.','negativo','2025-04-21 10:09:11',NULL),(11,3,3,'excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','Eres la mejor profesora que he tenido jam├ís. Me has hecho re├¡r, me has hecho pensar y me has hecho aprender. Tu entusiasmo y pasi├│n por el tema son contagiosos y me han hecho sentir como si estuviera en un viaje de descubrimiento. ┬íMuchas gracias por todo! Me siento afortunada de haber tenido la oportunidad de aprender de ti.','neutral','┬íQu├® alegr├¡a haber tomado el curso contigo! Ha sido una experiencia incre├¡ble y me has ense├▒ado cosas que nunca hubiera imaginado. ┬íEres una maestra fant├ística!','neutral','2025-04-21 10:10:33',NULL),(12,3,3,'pesimo','pesimo','pesimo','pesimo','pesimo','pesimo','pesimo','pesimo','pesimo','pesimo','Eres una profesora muy mala. No sabes explicar las cosas de manera clara, no te importa si los estudiantes entienden o no, y no te tomas el tiempo para ayudarnos. Me has hecho sentir frustrada y est├║pida. ┬íNo te recomiendo a nadie que te tome como profesora!','neutral','Lo siento, pero el curso ha sido un desastre. Me has hecho perder mi tiempo y no he aprendido nada.','negativo','2025-04-21 10:11:58',NULL),(13,3,3,'regular','regular','regular','regular','regular','regular','regular','regular','regular','regular','Eres una profesora que intenta hacer lo mejor que puede, pero a veces no es suficiente. Me has explicado algunas cosas de manera clara, pero tambi├®n has tenido momentos en los que he sentido que no estaba segura de lo que estabas diciendo. En general, he aprendido algunas cosas ├║tiles, pero no ha sido una experiencia perfecta.','neutral','El curso ha sido decente, pero no ha sido lo que esperaba. Me has ense├▒ado algunos conceptos interesantes, pero tambi├®n ha habido momentos en los que me he sentido un poco perdida','neutral','2025-04-21 10:13:17',NULL),(14,3,3,'regular','malo','bueno','regular','excelente','bueno','bueno','malo','regular','bueno','Eres una profesora que intenta mantener a los estudiantes interesados, pero a veces no es suficiente. Me has explicado algunas cosas de manera clara, pero tambi├®n has tenido momentos en los que he sentido que no estaba segura de lo que estabas diciendo. En general, he aprendido algunas cosas ├║tiles, pero no ha sido una experiencia impresionante.','neutral','El curso ha sido aceptable, pero no ha sido lo mejor que he visto. Me has ense├▒ado algunos conceptos interesantes, pero tambi├®n ha habido momentos en los que me he sentido un poco aburrido.','neutral','2025-04-21 10:21:45',NULL),(15,3,3,'excelente','bueno','excelente','bueno','excelente','bueno','excelente','bueno','excelente','bueno','Tu entusiasmo y pasi├│n por el tema son contagiosos y me han hecho sentir como si estuviera en un viaje de descubrimiento. ┬íMuchas gracias por todo! Me siento afortunada de haber tenido la oportunidad de aprender de ti.','neutral','Ha sido una experiencia incre├¡ble y me has ense├▒ado cosas que nunca hubiera imaginado. ┬íEres una maestra fant├ística!','neutral','2025-04-21 10:23:27',NULL),(16,1,1,'excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','Eres una profesora inspiradora que me ha hecho sentir motivada y apasionada por el tema. Tu forma de ense├▒ar es ├║nica y me ha permitido aprender de manera divertida y efectiva. ┬íTe agradezco por todo lo que me has ense├▒ado! Me siento afortunada de haber tenido la oportunidad de aprender de ti.','neutral','Me ha encantado el curso que me diste. Ha sido una experiencia emocionante y me has permitido descubrir nuevos conocimientos y habilidades. ┬íEres una maestra excepcional!','neutral','2025-04-21 10:25:12',NULL),(17,1,1,'excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','Tu profesora es muy dedicada y apasionada por su trabajo, lo que se refleja en la forma en que explica conceptos complejos de manera clara y accesible.','neutral','El curso ha sido una experiencia enriquecedora y divertida gracias a la variedad de actividades y recursos que se han utilizado para mantenernos motivados y comprometidos con el aprendizaje. La forma en que se ha estructurado el curso ha permitido que cada uno de nosotros desarrollara su propio ritmo y estilo de aprendizaje, lo que ha sido muy beneficioso para m├¡.','neutral','2025-04-22 10:55:27',NULL),(18,1,1,'excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','Mi profesora es excelente y brillante. Su dedicaci├│n y pasi├│n por el trabajo son maravillosas y se reflejan en la forma en que explica conceptos complejos de manera sencilla y clara. Me he sentido muy satisfecho con la forma en que se ha cuidado de nosotros y me ha proporcionado retroalimentaci├│n positiva y constructiva.','positivo','El curso ha sido genial y fant├ístico. Me he sentido muy contento y feliz durante todo el proceso. La forma en que se ha estructurado el curso ha sido claro y ├║til, lo que me ha permitido aprender mucho y desarrollar mis habilidades de manera eficiente. La variedad de actividades y recursos ha sido asombroso y me ha mantenido muy motivado.','positivo','2025-04-22 11:07:16',NULL),(19,1,1,'excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','La profesora es buena explicando los temas me ah ayudado mucho con mis preguntas.','neutral','El curso ah sido excelente, el material es muy bueno  y aprendido muchas cosass','positivo','2025-04-22 13:36:26',NULL),(20,1,1,'excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','excelente','El profesor ha sido un gran maestro, siempre dispuesto a ayudar y explicar de manera clara y paciente. Su entusiasmo y dedicaci├│n han hecho que el curso sea m├ís agradable y divertido. Muchas gracias por su excelente trabajo.','positivo','El curso ha sido muy ├║til y completo, cubriendo todos los temas necesarios de manera clara y concisa. Me ha permitido mejorar mis habilidades en [nombre del ├írea de estudio] y estoy satisfecho con la experiencia.','positivo','2025-04-27 13:23:25',NULL);
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
INSERT INTO `users` VALUES ('Ana Maria Caviedes Castillo','ana.caviedes.c@uniautonoma.edu.co','$2b$12$8vsdzzKwekJ.CTPS0ucq8uRF7shCGlqi5SASB7jB2v8GcJ0maVSae','2025-04-18 11:58:01','Ana Maria','Caviedes Castillo',1,0,1),('Jose Fernando Concha Gonzalez','jose.concha.g@uniautonoma.edu.co','$2b$12$hmWLuRiFeMjQF9Ef2JbkBegu4e1HQwA9PNoi2E6Bgum/gO2Xa6cs.','2025-04-18 11:58:01','Jose Fernando','Concha Gonzalez',1,0,2),('Ana Gabriela Fernandez Morantes','ana.fernandez.m@uniautonoma.edu.co','$2b$12$0beWZoYgvRGfrSvmjwUW6.uF.dXIk6WB6AXB4AtsnrHr5jTM5Q2rG','2025-04-18 11:58:01','Ana Gabriela','Fernandez Morantes',1,0,3),('Diego Fernando Prado Osorios','diego.prado.o@uniautonoma.edu.co','$2b$12$WIHbv7PtK0kTtJe8wl77h.saQiTeUArcL.FLaJkRVuw1A6KD4sJE.','2025-04-18 11:58:01','Diego Fernando','Prado Osorios',1,0,4),('Diana Patricia Garzon Mu├▒oz','diana.garzon.m@uniautonoma.edu.co','$2b$12$kRjTXdSYKfCthpImGNI3WuaY.2S9l7piA93e7mGvUbRH862bFcNaS','2025-04-18 11:58:02','Diana Patricia','Garzon Mu├▒oz',1,0,5),('David Urrutia Ceron','david.urrutia.c@uniautonoma.edu.co','$2b$12$33q.bAD.FTNlFy57/thyf.Tj4It44IkBTN7wrInzj52miYs4WVmcm','2025-04-18 14:05:40','David','Urrutia Ceron',1,0,6),('Deiby Alejandro Ramirez Galvis','deiby.ramirez.g@uniautonoma.edu.co','$2b$12$e1aZQtlN3JxUF/CvWh1yfeZ0TcctBCfuVdfQsh98XuV8yItL7044W','2025-04-18 14:05:41','Deiby Alejandro','Ramirez Galvis',1,0,7),('Thomas Montoya Magon','thomas.montoya.m@uniautonoma.edu.co','$2b$12$yAZEVTz1ZjJ4Se8GFIZ7YeHzi2sXDvnRgIVk0Kb4QsjWggPlccCxC','2025-04-18 14:05:41','Thomas','Montoya Magon',1,0,8),('Luisa Jhulieth Joaqui Jimenez','luisa.joaqui.j@uniautonoma.edu.co','$2b$12$Q7PM9.m4uzEevx3NWeVDruGUJ3W4Mp6aif2wnlA/6HAzRmp7xQ2qi','2025-04-18 14:05:41','Luisa Jhulieth','Joaqui Jimenez',1,0,9),('Daviel Rivas Agredo','daniel.rivas.a@uniautonoma.edu.co','$2b$12$K0VZZ9sY4maWD7mjVVaR9.NeSG7oUNIwX.GxotdYry2HNLbEUCLg.','2025-04-18 14:05:41','Daniel','Rivas Agredo',1,0,10),('Administrador','admin@uniautonoma.edu.co','$2b$12$eNjuXa3SSO2VWh3PkHnP5eh4jDYEnT1a/IsmmXQey6efj/yUEFQqe','2025-04-18 22:09:10','Administrador','General',1,1,11);
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

-- Dump completed on 2025-04-27 19:51:15
