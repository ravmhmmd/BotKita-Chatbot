-- MariaDB dump 10.18  Distrib 10.5.8-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: stima
-- ------------------------------------------------------
-- Server version	10.5.8-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `kuis`
--

DROP TABLE IF EXISTS `kuis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kuis` (
  `kode_kuliah` varchar(25) NOT NULL,
  `Deskripsi` varchar(30) NOT NULL,
  `tanggal` varchar(25) NOT NULL,
  PRIMARY KEY (`kode_kuliah`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kuis`
--

LOCK TABLES `kuis` WRITE;
/*!40000 ALTER TABLE `kuis` DISABLE KEYS */;
INSERT INTO `kuis` VALUES ('IF3310','bab 2 sampai 3','22/04/2014');
/*!40000 ALTER TABLE `kuis` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tubes`
--

DROP TABLE IF EXISTS `tubes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tubes` (
  `kode_kuliah` varchar(25) NOT NULL,
  `Deskripsi` varchar(30) NOT NULL,
  `tanggal` varchar(25) NOT NULL,
  PRIMARY KEY (`kode_kuliah`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tubes`
--

LOCK TABLES `tubes` WRITE;
/*!40000 ALTER TABLE `tubes` DISABLE KEYS */;
INSERT INTO `tubes` VALUES ('IF2210','materi inheritance','04/05/2021'),('IF3310','bab 2 sampai 3','22/04/2014');
/*!40000 ALTER TABLE `tubes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tucil`
--

DROP TABLE IF EXISTS `tucil`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tucil` (
  `kode_kuliah` varchar(25) NOT NULL,
  `Deskripsi` varchar(30) NOT NULL,
  `tanggal` varchar(25) NOT NULL,
  PRIMARY KEY (`kode_kuliah`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tucil`
--

LOCK TABLES `tucil` WRITE;
/*!40000 ALTER TABLE `tucil` DISABLE KEYS */;
INSERT INTO `tucil` VALUES ('IF3310','bab 2 sampai 3','22/04/2014');
/*!40000 ALTER TABLE `tucil` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ujian`
--

DROP TABLE IF EXISTS `ujian`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ujian` (
  `kode_kuliah` varchar(25) NOT NULL,
  `Deskripsi` varchar(30) NOT NULL,
  `tanggal` varchar(25) NOT NULL,
  PRIMARY KEY (`kode_kuliah`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ujian`
--

LOCK TABLES `ujian` WRITE;
/*!40000 ALTER TABLE `ujian` DISABLE KEYS */;
/*!40000 ALTER TABLE `ujian` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-04-27 12:06:39
