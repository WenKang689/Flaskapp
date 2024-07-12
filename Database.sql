
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
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment` (
  `saved_card_id` char(6) NOT NULL,
  `username` varchar(30) NOT NULL,
  `name_on_card` varchar(50) NOT NULL,
  `card_no` char(16) NOT NULL,
  `cvv` char(3) NOT NULL,
  `expiry_date` char(5) NOT NULL,
  PRIMARY KEY (`saved_card_id`),
  KEY `username` (`username`),
  CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`username`) REFERENCES `user` (`username`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
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
  `brand` varchar(15) NOT NULL,
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
  `stock` int NOT NULL,
  PRIMARY KEY (`product_id`),
  UNIQUE KEY `product_id` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES ('LP0001','Acer Predator Helios 300','Acer','Intel Core i7-10750H','NVIDIA GeForce RTX 2060','363 x 255 x 22.9 mm',2500,'Windows 10','16GB DDR4','512GB PCIe NVMe SSD','230W','59 Wh',12000,0),('LP0002','Acer Swift 3','Acer','AMD Ryzen 7 4700U','AMD Radeon Graphics','323 x 218 x 15.9 mm',1190,'Windows 10','8GB LPDDR4X','512GB PCIe NVMe SSD','65W','48 Wh',6000,0),('LP0003','Acer Aspire 5','Acer','Intel Core i5-1135G7','Intel Iris Xe Graphics','363.4 x 238.5 x 17.9 mm',1700,'Windows 10','8GB DDR4','256GB PCIe NVMe SSD','65W','48 Wh',5000,0),('LP0004','Acer Spin 5','Acer','Intel Core i7-1065G7','Intel Iris Plus Graphics','304.6 x 230.6 x 15.9 mm',1200,'Windows 10','16GB LPDDR4X','512GB PCIe NVMe SSD','65W','56 Wh',9000,0),('LP0005','Acer Nitro 5','Acer','AMD Ryzen 5 4600H','NVIDIA GeForce GTX 1650','363.4 x 255 x 23.9 mm',2500,'Windows 10','8GB DDR4','256GB PCIe NVMe SSD','135W','58 Wh',7000,0),('LP0006','Acer Chromebook Spin 713','Acer','Intel Core i5-1135G7','Intel Iris Xe Graphics','312.6 x 224 x 18 mm',1400,'Chrome OS','8GB','256GB SSD','150W','48 Wh',3233,0),('LP0007','Acer Chromebook 315','Acer','Intel Celeron N4000','Intel UHD Graphics','320 x 206 x 17.5 mm',1900,'Chrome OS','4GB','32GB','160W','52 Wh',843,0),('LP0008','Acer Chromebook 516 GE','Acer','Intel Core i5-1240P','Intel Iris Xe Graphics','358 x 264 x 23.4 mm',1700,'Chrome OS','8GB','256GB','230W','80 Wh',2544,0),('LP0009','Aspire Go 15','Acer','Intel Core i3-N305','Intel UHD Graphics','396.2 x 211.3 x 17 mm',1750,'Windows 11','8GB','512TB','65W','50 Wh',1899,0),('LP0010','Predator Helios Neo 14','Acer','Intel Core Ultra 9','NVIDIA GeForce RTX 4070','313.5 x 211.3 x 17 mm',2100,'Windows 11','32GB','1TB','230W','76 Wh',7799,0),('LP0011','Acer ConceptD 3 Ezel','Acer','Intel Core i7-10750H','NVIDIA GeForce GTX 1650 Max-Q','322.5 x 228 x 20 mm',1700,'Windows 10','16GB DDR4','1TB PCIe NVMe SSD','135W','76 Wh',15000,0),('LP0012','Predator Triton 17 X','Acer','Intel Core i9-13900HX','NVIDIA GeForce RTX 4090','358 x 264 x 23.4 mm',3000,'Windows 11','64GB','4TB','330W','100 Wh',18999,0),('LP0013','Predator Helios 18','Acer','Intel Core i9-13900HX','NVIDIA GeForce RTX 4080','405 x 311.6 x 28.9 mm',3400,'Windows 11','32GB','2TB','330W','90 Wh',12999,0),('LP0014','Predator Triton 14','Acer','Intel Core i7-13700H','NVIDIA GeForce RTX 4070','313.5 x 227 x 19.9 mm',1700,'Windows 11','32GB','1TB','230W','76 Wh',8999,0),('LP0015','Asus ROG Zephyrus G14','Asus','AMD Ryzen 9 5900HS','NVIDIA GeForce RTX 3060','324 x 222 x 19.9 mm',1700,'Windows 10','16GB DDR4','1TB PCIe NVMe SSD','180W','76 Wh',12000,0),('LP0016','Asus TUF Gaming F15','Asus','Intel Core i5-10300H','NVIDIA GeForce GTX 1650','359 x 256 x 24.7 mm',2300,'Windows 10','8GB DDR4','512GB PCIe NVMe SSD','150W','48 Wh',6000,0),('LP0017','Asus ZenBook 14','Asus','AMD Ryzen 7 5800U','AMD Radeon Graphics','319 x 210 x 14.3 mm',1400,'Windows 10','16GB LPDDR4X','1TB PCIe NVMe SSD','65W','63 Wh',8000,0),('LP0018','Asus VivoBook S14','Asus','Intel Core i7-1165G7','Intel Iris Xe Graphics','323 x 211 x 15.9 mm',1500,'Windows 10','16GB DDR4','512GB PCIe NVMe SSD','65W','67 Wh',7000,0),('LP0019','Asus ROG Strix G15','Asus','AMD Ryzen 7 5800H','NVIDIA GeForce RTX 3050 Ti','354 x 259 x 27.2 mm',2300,'Windows 10','16GB DDR4','512GB PCIe NVMe SSD','200W','90 Wh',9000,0),('LP0020','Dell XPS 13','Dell','Intel Core i7-1165G7','Intel Iris Xe Graphics','295.7 x 198.7 x 14.8 mm',1200,'Windows 10','16GB LPDDR4x','512GB PCIe NVMe SSD','45W','52 Wh',10000,0),('LP0021','Dell G5 15','Dell','Intel Core i7-10750H','NVIDIA GeForce GTX 1660 Ti','364 x 273 x 23.7 mm',2500,'Windows 10','16GB DDR4','1TB PCIe NVMe SSD','180W','68 Wh',8000,0),('LP0022','Dell Inspiron 15 5000','Dell','Intel Core i5-1135G7','Intel Iris Xe Graphics','356 x 234 x 18 mm',1750,'Windows 10','8GB DDR4','512GB PCIe NVMe SSD','65W','53 Wh',5000,0),('LP0023','Dell Latitude 7420','Dell','Intel Core i7-1185G7','Intel Iris Xe Graphics','305.7 x 207.5 x 17.6 mm',1320,'Windows 10','16GB LPDDR4x','1TB PCIe NVMe SSD','65W','63 Wh',12000,0),('LP0024','Dell Alienware m15 R6','Dell','Intel Core i7-11800H','NVIDIA GeForce RTX 3070','356.2 x 272.5 x 22.9 mm',2400,'Windows 10','16GB DDR4','1TB PCIe NVMe SSD','240W','86 Wh',14000,0),('LP0025','HP Spectre x360 14','HP','Intel Core i7-1165G7','Intel Iris Xe Graphics','298.5 x 220.4 x 16.9 mm',1400,'Windows 10','16GB LPDDR4x','512GB PCIe NVMe SSD','65W','66 Wh',11000,0),('LP0026','HP Omen 15','HP','AMD Ryzen 7 5800H','NVIDIA GeForce RTX 3060','357.9 x 239.7 x 22.6 mm',2400,'Windows 10','16GB DDR4','1TB PCIe NVMe SSD','200W','70.9 Wh',13000,0),('LP0027','HP Pavilion x360','HP','Intel Core i5-1135G7','Intel Iris Xe Graphics','308.5 x 206 x 17.9 mm',1600,'Windows 10','8GB DDR4','256GB PCIe NVMe SSD','45W','43 Wh',6000,0),('LP0028','HP Envy 13','HP','Intel Core i7-1165G7','Intel Iris Xe Graphics','306.5 x 194.6 x 16.9 mm',1200,'Windows 10','16GB LPDDR4x','512GB PCIe NVMe SSD','65W','53 Wh',9000,0),('LP0029','HP Elite Dragonfly','HP','Intel Core i7-1165G7','Intel Iris Xe Graphics','304.3 x 197.5 x 16.1 mm',990,'Windows 10','16GB LPDDR4x','1TB PCIe NVMe SSD','65W','56.2 Wh',15000,0),('LP0030','Lenovo Legion 5 Pro','Lenovo','AMD Ryzen 7 5800H','NVIDIA GeForce RTX 3070','356 x 260.4 x 26.7 mm',2540,'Windows 11','16GB DDR4','1TB PCIe NVMe SSD','300W','80 Wh',8000,0),('LP0031','Lenovo ThinkPad X1 Carbon Gen 9','Lenovo','Intel Core i7-1165G7','Intel Iris Xe Graphics','314.5 x 221.6 x 14.9 mm',1130,'Windows 11','16GB LPDDR4X','512GB PCIe NVMe SSD','65W','57 Wh',10000,0),('LP0032','Lenovo Yoga 9i','Lenovo','Intel Core i7-1185G7','Intel Iris Xe Graphics','320.4 x 216.7 x 16.1 mm',1300,'Windows 11','16GB LPDDR4X','1TB PCIe NVMe SSD','65W','60 Wh',9000,0),('LP0033','Lenovo IdeaPad 3','Lenovo','AMD Ryzen 5 5500U','AMD Radeon Graphics','327.1 x 241 x 19.9 mm',1650,'Windows 10','8GB DDR4','512GB PCIe NVMe SSD','65W','45 Wh',4000,0),('LP0034','Lenovo ThinkBook 14s Yoga','Lenovo','Intel Core i7-1165G7','Intel Iris Xe Graphics','320.5 x 216.5 x 16.9 mm',1500,'Windows 11','16GB DDR4','512GB PCIe NVMe SSD','65W','60 Wh',8000,0),('LP0035','Legion Pro 7i','Lenovo','Intel Core i9-13900HX','NVIDIA GeForce RTX 4080','320 x 220 x 16.8 mm',2100,'Windows 11 Pro','32GB DDR5','1TB SSD','330W','100 Wh',12469,0),('LP0036','MSI GS66 Stealth','MSI','Intel Core i7-10875H','NVIDIA GeForce RTX 2070 Super','358.3 x 248 x 19.8 mm',2100,'Windows 10','32GB DDR4','1TB PCIe NVMe SSD','230W','99.9 Wh',15000,0),('LP0037','MSI GE76 Raider','MSI','Intel Core i9-11980HK','NVIDIA GeForce RTX 3080','397.6 x 284.5 x 25.9 mm',2900,'Windows 10','32GB DDR4','1TB PCIe NVMe SSD','280W','99.9 Wh',18000,0),('LP0038','MSI Prestige 14','MSI','Intel Core i7-1185G7','Intel Iris Xe Graphics','319 x 215 x 15.9 mm',1200,'Windows 10','16GB LPDDR4x','512GB PCIe NVMe SSD','65W','52 Wh',9000,0),('LP0039','MSI Modern 14','MSI','Intel Core i5-10210U','Intel UHD Graphics','322 x 222 x 16.9 mm',1300,'Windows 10','8GB DDR4','512GB PCIe NVMe SSD','65W','52 Wh',5000,0),('LP0040','MSI Creator 15','MSI','Intel Core i7-10875H','NVIDIA GeForce RTX 2060','358 x 248 x 19.8 mm',2100,'Windows 10','32GB DDR4','1TB PCIe NVMe SSD','230W','99.9 Wh',14000,0),('LP0041','Razer Blade 15','Razer','Intel Core i7-11800H','NVIDIA GeForce RTX 3070','355 x 235 x 17 mm',2040,'Windows 11','16GB DDR4','1TB PCIe NVMe SSD','230W','80 Wh',15000,0),('LP0042','Razer Blade Stealth 13','Razer','Intel Core i7-1165G7','Intel Iris Xe Graphics','304.6 x 210 x 15.3 mm',1360,'Windows 10','16GB LPDDR4x','512GB PCIe NVMe SSD','100W','53.1 Wh',12000,0),('LP0043','Razer Book 13','Razer','Intel Core i7-1165G7','Intel Iris Xe Graphics','295 x 198.5 x 15.1 mm',1350,'Windows 10','16GB LPDDR4x','512GB PCIe NVMe SSD','65W','55 Wh',13000,0),('LP0044','Razer Blade 14','Razer','AMD Ryzen 9 5900HX','NVIDIA GeForce RTX 3060','319.7 x 220 x 16.8 mm',1750,'Windows 11','16GB DDR4','1TB PCIe NVMe SSD','230W','61.6 Wh',14000,0),('LP0045','Razer Blade Pro 17','Razer','Intel Core i7-10875H','NVIDIA GeForce RTX 2080 Super','395 x 260 x 19.9 mm',2900,'Windows 10','32GB DDR4','1TB PCIe NVMe SSD','230W','70.5 Wh',18000,0),('LP0046','Huawei MateBook X Pro','Huawei','Intel Core i7-1165G7','Intel Iris Xe Graphics','304 x 217 x 14.6 mm',1330,'Windows 10','16GB LPDDR4x','1TB SSD','65W','56 Wh',12000,0),('LP0047','Huawei MateBook 14','Huawei','AMD Ryzen 7 4800H','AMD Radeon Graphics','307.5 x 223.8 x 15.9 mm',1530,'Windows 10','16GB DDR4','512GB PCIe NVMe SSD','65W','56 Wh',9000,0),('LP0048','Huawei MateBook D 15','Huawei','AMD Ryzen 5 3500U','AMD Radeon Vega 8 Graphics','357.8 x 229.9 x 16.9 mm',1530,'Windows 10','8GB DDR4','256GB PCIe NVMe SSD','65W','42 Wh',5000,0),('LP0049','Huawei MateBook 13','Huawei','Intel Core i5-1135G7','Intel Iris Xe Graphics','286 x 211 x 14.9 mm',1290,'Windows 10','16GB LPDDR4x','512GB PCIe NVMe SSD','65W','42 Wh',7000,0),('LP0050','Huawei MateBook X','Huawei','Intel Core i5-10210U','Intel UHD Graphics','284.4 x 206.7 x 13.6 mm',1000,'Windows 10','16GB LPDDR3','512GB PCIe NVMe SSD','65W','42 Wh',8000,0);
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_pic`
--

DROP TABLE IF EXISTS `product_pic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_pic` (
  `pic_id` char(6) NOT NULL,
  `product_id` char(6) NOT NULL,
  `pic_url` varchar(255) NOT NULL,
  PRIMARY KEY (`pic_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `product_pic_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_pic`
--

LOCK TABLES `product_pic` WRITE;
/*!40000 ALTER TABLE `product_pic` DISABLE KEYS */;
/*!40000 ALTER TABLE `product_pic` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchase`
--

DROP TABLE IF EXISTS `purchase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchase` (
  `order_id` char(8) NOT NULL,
  `username` varchar(30) NOT NULL,
  `product_id` char(6) NOT NULL,
  `pur_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `pur_amount` int NOT NULL,
  `pur_status` varchar(7) NOT NULL,
  `pur_quantity` int NOT NULL,
  `processed_by` char(6) NOT NULL,
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
-- Table structure for table `review`
--

DROP TABLE IF EXISTS `review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `review` (
  `review_id` char(6) NOT NULL,
  `role` varchar(5) NOT NULL,
  `username_or_stf_id` varchar(30) NOT NULL,
  `review` varchar(255) DEFAULT NULL,
  `rating` int NOT NULL,
  PRIMARY KEY (`review_id`),
  KEY `username` (`username_or_stf_id`),
  CONSTRAINT `review_ibfk_1` FOREIGN KEY (`username_or_stf_id`) REFERENCES `user` (`username`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `review`
--

LOCK TABLES `review` WRITE;
/*!40000 ALTER TABLE `review` DISABLE KEYS */;
/*!40000 ALTER TABLE `review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `search_history`
--

DROP TABLE IF EXISTS `search_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `search_history` (
  `search_id` char(6) NOT NULL,
  `username` varchar(30) NOT NULL,
  `search_query` varchar(255) NOT NULL,
  PRIMARY KEY (`search_id`),
  KEY `username` (`username`),
  CONSTRAINT `search_history_ibfk_1` FOREIGN KEY (`username`) REFERENCES `user` (`username`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `search_history`
--

LOCK TABLES `search_history` WRITE;
/*!40000 ALTER TABLE `search_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `search_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shipping`
--

DROP TABLE IF EXISTS `shipping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shipping` (
  `ship_id` char(8) NOT NULL,
  `order_id` char(8) NOT NULL,
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
  `prof_pic` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`username`),
  UNIQUE KEY `user_id` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('aaa','ccc','Chong Wen Kang','braynchongwenkang590@gmail.com','0126843432','2024-06-05',NULL,NULL,NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'flaskapp'
--

--
-- Dumping routines for database 'flaskapp'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-12 23:51:44
