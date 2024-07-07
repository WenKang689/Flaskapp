CREATE DATABASE  IF NOT EXISTS `flaskapp` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `flaskapp`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: flaskapp
-- ------------------------------------------------------
-- Server version	8.3.0

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
-- Table structure for table `cart`
--

DROP TABLE IF EXISTS `cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart` (
  `username` varchar(30) NOT NULL,
  `product_id` char(6) NOT NULL,
  `quantity` int NOT NULL,
  PRIMARY KEY (`username`,`product_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`username`) REFERENCES `user` (`username`) ON UPDATE CASCADE,
  CONSTRAINT `cart_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart`
--

LOCK TABLES `cart` WRITE;
/*!40000 ALTER TABLE `cart` DISABLE KEYS */;
/*!40000 ALTER TABLE `cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `product_id` char(6) NOT NULL,
  `product_name` varchar(50) NOT NULL,
  `processor` varchar(30) NOT NULL,
  `graphics` varchar(30) NOT NULL,
  `dimensions` varchar(30) NOT NULL,
  `weight` int NOT NULL,
  `os` varchar(30) NOT NULL,
  `memory` varchar(30) NOT NULL,
  `storage` varchar(30) NOT NULL,
  `power_supply` varchar(30) NOT NULL,
  `battery` varchar(30) NOT NULL,
  `price` int NOT NULL,
  PRIMARY KEY (`product_id`),
  UNIQUE KEY `product_id` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchase`
--

DROP TABLE IF EXISTS `purchase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchase` (
  `order_id` char(8) NOT NULL,
  `username` varchar(30) DEFAULT NULL,
  `product_id` char(6) DEFAULT NULL,
  `pur_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `pur_method` varchar(10) NOT NULL,
  `pur_amount` int NOT NULL,
  `pur_status` varchar(7) NOT NULL,
  `pur_quantity` int DEFAULT NULL,
  `processed_by` char(6) DEFAULT NULL,
  PRIMARY KEY (`order_id`),
  UNIQUE KEY `order_id` (`order_id`),
  KEY `username` (`username`),
  KEY `product_id` (`product_id`),
  KEY `processed_by` (`processed_by`),
  CONSTRAINT `purchase_ibfk_1` FOREIGN KEY (`username`) REFERENCES `user` (`username`) ON UPDATE CASCADE,
  CONSTRAINT `purchase_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE,
  CONSTRAINT `purchase_ibfk_3` FOREIGN KEY (`processed_by`) REFERENCES `staff` (`stf_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchase`
--

LOCK TABLES `purchase` WRITE;
/*!40000 ALTER TABLE `purchase` DISABLE KEYS */;
/*!40000 ALTER TABLE `purchase` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shipping`
--

DROP TABLE IF EXISTS `shipping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shipping` (
  `ship_id` char(8) NOT NULL,
  `order_id` char(8) DEFAULT NULL,
  `dest_add` varchar(255) NOT NULL,
  `receiver_name` varchar(30) NOT NULL,
  `receiver_phone` varchar(30) NOT NULL,
  `ship_status` varchar(8) NOT NULL,
  `ship_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ship_id`),
  UNIQUE KEY `ship_id` (`ship_id`),
  KEY `order_id` (`order_id`),
  CONSTRAINT `shipping_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `purchase` (`order_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shipping`
--

LOCK TABLES `shipping` WRITE;
/*!40000 ALTER TABLE `shipping` DISABLE KEYS */;
/*!40000 ALTER TABLE `shipping` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS `staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staff` (
  `stf_id` char(6) NOT NULL,
  `stf_psw` varchar(20) NOT NULL,
  `stf_name` varchar(30) NOT NULL,
  `stf_email` varchar(30) NOT NULL,
  `stf_phone` char(10) NOT NULL,
  `stf_dob` date NOT NULL,
  `stf_address` varchar(255) NOT NULL,
  `stf_emer_contact` char(10) NOT NULL,
  `stf_role` char(10) DEFAULT NULL,
  PRIMARY KEY (`stf_id`),
  UNIQUE KEY `stf_id` (`stf_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff`
--

LOCK TABLES `staff` WRITE;
/*!40000 ALTER TABLE `staff` DISABLE KEYS */;
/*!40000 ALTER TABLE `staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `username` varchar(30) NOT NULL,
  `password` varchar(20) NOT NULL,
  `name` varchar(30) NOT NULL,
  `email` varchar(30) DEFAULT NULL,
  `phone` char(10) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `occupation` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`username`),
  UNIQUE KEY `user_id` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('www','fwf','Chong Wen Kang','braynchongwenkang590@gmail.com','0126843432','2024-06-05',NULL,NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-05 15:16:09
