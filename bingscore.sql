-- MySQL dump 10.13  Distrib 8.0.15, for Win64 (x86_64)
--
-- Host: localhost    Database: example
-- ------------------------------------------------------
-- Server version	8.0.15

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8mb4 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cards`
--

DROP TABLE IF EXISTS `cards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `cards` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `match_id` int(11) NOT NULL,
  `time` int(11) NOT NULL,
  `type` enum('Yellow','Red') NOT NULL,
  `number` int(11) NOT NULL,
  `player` varchar(25) DEFAULT NULL,
  `team` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cards`
--

LOCK TABLES `cards` WRITE;
/*!40000 ALTER TABLE `cards` DISABLE KEYS */;
/*!40000 ALTER TABLE `cards` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `corners`
--

DROP TABLE IF EXISTS `corners`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `corners` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `match_id` int(11) NOT NULL,
  `time` int(11) NOT NULL,
  `number` int(11) NOT NULL,
  `team` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `corners`
--

LOCK TABLES `corners` WRITE;
/*!40000 ALTER TABLE `corners` DISABLE KEYS */;
/*!40000 ALTER TABLE `corners` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `goals`
--

DROP TABLE IF EXISTS `goals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `goals` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `match_id` int(11) NOT NULL,
  `time` int(11) NOT NULL,
  `number` int(11) NOT NULL,
  `player` varchar(99) DEFAULT NULL,
  `team` int(11) NOT NULL,
  `how` varchar(99) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `goals`
--

LOCK TABLES `goals` WRITE;
/*!40000 ALTER TABLE `goals` DISABLE KEYS */;
/*!40000 ALTER TABLE `goals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `matches`
--

DROP TABLE IF EXISTS `matches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `matches` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `team_1` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `team_2` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `datetime` datetime NOT NULL,
  `pitch` varchar(25) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `weather` varchar(25) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `ht_on_target_1` int(11) DEFAULT NULL,
  `ht_off_target_1` int(11) DEFAULT NULL,
  `ht_d_attacks_1` int(11) DEFAULT NULL,
  `ht_attacks_1` int(11) DEFAULT NULL,
  `ht_possession_1` int(11) DEFAULT NULL,
  `ht_on_target_2` int(11) DEFAULT NULL,
  `ht_off_target_2` int(11) DEFAULT NULL,
  `ht_d_attacks_2` int(11) DEFAULT NULL,
  `ht_attacks_2` int(11) DEFAULT NULL,
  `ht_possession_2` int(11) DEFAULT NULL,
  `ht_additional_time` int(11) DEFAULT NULL,
  `ft_on_target_1` int(11) DEFAULT NULL,
  `ft_off_target_1` int(11) DEFAULT NULL,
  `ft_d_attacks_1` int(11) DEFAULT NULL,
  `ft_attacks_1` int(11) DEFAULT NULL,
  `ft_possession_1` int(11) DEFAULT NULL,
  `ft_on_target_2` int(11) DEFAULT NULL,
  `ft_off_target_2` int(11) DEFAULT NULL,
  `ft_d_attacks_2` int(11) DEFAULT NULL,
  `ft_attacks_2` int(11) DEFAULT NULL,
  `ft_possession_2` int(11) DEFAULT NULL,
  `log` json DEFAULT NULL,
  `ft_additional_time` int(11) DEFAULT NULL,
  `ht_corners_count` varchar(25) DEFAULT NULL,
  `ft_corners_count` varchar(25) DEFAULT NULL,
  `ht_goals_count` varchar(25) DEFAULT NULL,
  `ft_goals_count` varchar(25) DEFAULT NULL,
  `url` varchar(60) NOT NULL,
  `league` varchar(155) NOT NULL,
  `trend_h` float DEFAULT NULL,
  `trend_g` float DEFAULT NULL,
  `trend_c` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `matches`
--

LOCK TABLES `matches` WRITE;
/*!40000 ALTER TABLE `matches` DISABLE KEYS */;
/*!40000 ALTER TABLE `matches` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-08-29 22:18:22
