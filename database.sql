-- MySQL dump 10.13  Distrib 5.5.62, for Win64 (AMD64)
--
-- Host: 192.168.74.129    Database: NuOJ
-- ------------------------------------------------------
-- Server version	5.5.5-10.6.7-MariaDB-2ubuntu1.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `problem`
--

DROP TABLE IF EXISTS `problem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `problem` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `problem_pid` varchar(20) NOT NULL,
  `problem_author` varchar(20) NOT NULL,
  `solution_group` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=100004 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `problem`
--

LOCK TABLES `problem` WRITE;
/*!40000 ALTER TABLE `problem` DISABLE KEYS */;
/*!40000 ALTER TABLE `problem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profile`
--

DROP TABLE IF EXISTS `profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `profile` (
  `user_uid` varchar(36) NOT NULL,
  `img_type` varchar(5) DEFAULT NULL,
  `email` text DEFAULT NULL,
  `school` text DEFAULT NULL,
  `bio` text DEFAULT NULL,
  PRIMARY KEY (`user_uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profile`
--

LOCK TABLES `profile` WRITE;
/*!40000 ALTER TABLE `profile` DISABLE KEYS */;
/*!40000 ALTER TABLE `profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `submission`
--

DROP TABLE IF EXISTS `submission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `submission` (
  `solution_id` varchar(40) NOT NULL,
  `solution_group` varchar(40) DEFAULT NULL,
  `problem_id` varchar(40) NOT NULL,
  `user_uid` varchar(40) NOT NULL,
  `language` varchar(20) NOT NULL,
  `date` varchar(40) NOT NULL,
  `type` varchar(40) NOT NULL,
  `result` varchar(20) DEFAULT NULL,
  `time` varchar(40) DEFAULT NULL,
  `memory` varchar(40) DEFAULT NULL,
  `judger_id` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`solution_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `submission`
--

LOCK TABLES `submission` WRITE;
/*!40000 ALTER TABLE `submission` DISABLE KEYS */;
INSERT INTO `submission` VALUES ('87da6a26-8ef9-471f-9006-200384257e8a','98cccad3-ae04-4cd4-89f8-ece961aa364b','afc520c1779b907289e4','han910625','C++','2022-08-28 22:15:44.837361','PC','Failed','1.138','170.24',NULL),('93ac6372-da52-409e-92d7-4acb944bb6d7','3ee2ec97-72eb-4d45-a939-14e48cadbcaa','afc520c1779b907289e4','han910625','C++','2022-08-28 21:51:31.888225','PC',NULL,NULL,NULL,NULL),('ac150d90-1c89-4be5-bb18-8f5e872d1cb8','8b74ecd2-c43c-4c9a-aa88-25d555c8eb02','afc520c1779b907289e4','han910625','C++','2022-08-28 22:13:48.937646','PC','OK','1.315','171.69',NULL),('d53afc6f-da45-4a92-ae0b-76d8e259c80e','862196cd-ec54-4b3c-9d70-b0ee56acff69','afc520c1779b907289e4','han910625','C++','2022-08-28 21:50:51.655780','PC',NULL,NULL,NULL,NULL),('ed3c1805-5013-4a75-93e7-0df5cbe70bec','8b2b89c9-d0dc-4a88-8d23-0fd4e68cc41c','afc520c1779b907289e4','han910625','C++','2022-08-28 21:51:47.081770','PC','OK','1.631','199.55',NULL);
/*!40000 ALTER TABLE `submission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `user_uid` varchar(36) NOT NULL,
  `handle` varchar(32) DEFAULT NULL,
  `password` varchar(128) NOT NULL,
  `email` varchar(320) NOT NULL,
  `role` int(11) NOT NULL,
  `email_verified` tinyint(1) NOT NULL,
  PRIMARY KEY (`user_uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'NuOJ'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-08-28 22:21:31
