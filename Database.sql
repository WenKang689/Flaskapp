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
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback` (
  `feedback_id` char(6) NOT NULL,
  `stf_id` char(6) NOT NULL,
  `feedback` varchar(255) NOT NULL,
  `feedback_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `reply` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`feedback_id`),
  KEY `stf_id` (`stf_id`),
  CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`stf_id`) REFERENCES `staff` (`stf_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
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
  `pay_email` varchar(50) NOT NULL,
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
INSERT INTO `payment` VALUES ('PC0001','wkwk','rrg','8765433456765432','654','09/24','braynchongwenkang590@gmail.com');
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
INSERT INTO `product_pic` VALUES ('PP0001','LP0001','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0001)+Acer+Predator+Helios+300/aph+300+-+1.jpg'),('PP0002','LP0001','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0001)+Acer+Predator+Helios+300/aph+300+-+2.jpg'),('PP0003','LP0001','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0001)+Acer+Predator+Helios+300/aph+300+-+3.jpg'),('PP0004','LP0001','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0001)+Acer+Predator+Helios+300/aph+300+-+4.jpg'),('PP0005','LP0002','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0002)+Acer+Swift+3/as3+-+1.jpg'),('PP0006','LP0002','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0002)+Acer+Swift+3/as3+-+2.jpg'),('PP0007','LP0002','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0002)+Acer+Swift+3/as3+-+3.jpg'),('PP0008','LP0003','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0003)+Acer+Aspire+5/aa5+-+1.jpg'),('PP0009','LP0003','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0003)+Acer+Aspire+5/aa5+-+2.jpg'),('PP0010','LP0003','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0003)+Acer+Aspire+5/aa5+-+3.jpg'),('PP0011','LP0003','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0003)+Acer+Aspire+5/aa5+-+4.jpg'),('PP0012','LP0004','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0004)+Acer+Spin+5/as5+-+1.jpg'),('PP0013','LP0004','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0004)+Acer+Spin+5/as5+-+2.jpg'),('PP0014','LP0004','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0004)+Acer+Spin+5/as5+-+3.jpg'),('PP0015','LP0004','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0004)+Acer+Spin+5/as5+-+4.jpg'),('PP0016','LP0004','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0004)+Acer+Spin+5/as5+-+5.jpg'),('PP0017','LP0004','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0004)+Acer+Spin+5/as5+-+6.jpg'),('PP0018','LP0005','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0005)+Acer+Nitro+5/an5+-+1.jpg'),('PP0019','LP0005','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0005)+Acer+Nitro+5/an5+-+2.jpg'),('PP0020','LP0005','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0005)+Acer+Nitro+5/an5+-+3.jpg'),('PP0021','LP0006','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0006)+Acer+Chromebook+Spin+713/acs+713+-+1.jpg'),('PP0022','LP0006','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0006)+Acer+Chromebook+Spin+713/acs+713+-+2.jpg'),('PP0023','LP0006','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0006)+Acer+Chromebook+Spin+713/acs+713+-+3.jpg'),('PP0024','LP0006','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0006)+Acer+Chromebook+Spin+713/acs+713+-+4.jpg'),('PP0025','LP0007','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0007)+Acer+Chromebook+315/ac315+-+1.jpg'),('PP0026','LP0007','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0007)+Acer+Chromebook+315/ac315+-+2.jpg'),('PP0027','LP0007','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0007)+Acer+Chromebook+315/ac315+-+3.jpg'),('PP0028','LP0007','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0007)+Acer+Chromebook+315/ac315+-+4.jpg'),('PP0029','LP0007','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0007)+Acer+Chromebook+315/ac315+-+5.jpg'),('PP0030','LP0008','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0008)+Acer+Chromebook+516+GE/ac516+-+1.jpg'),('PP0031','LP0008','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0008)+Acer+Chromebook+516+GE/ac516+-+2.jpg'),('PP0032','LP0008','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0008)+Acer+Chromebook+516+GE/ac516+-+3.jpg'),('PP0033','LP0008','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0008)+Acer+Chromebook+516+GE/ac516+-+4.jpg'),('PP0034','LP0008','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0008)+Acer+Chromebook+516+GE/ac516+-+5.jpg'),('PP0035','LP0009','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0009)+Acer+Aspire+Go+15/aag15+-+1.jpg'),('PP0036','LP0009','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0009)+Acer+Aspire+Go+15/aag15+-+2.jpg'),('PP0037','LP0009','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0009)+Acer+Aspire+Go+15/aag15+-+3.jpg'),('PP0038','LP0009','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0009)+Acer+Aspire+Go+15/aag15+-+4.jpg'),('PP0039','LP0010','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0010)+Acer+Predator+Helios+Neo+14/aphn14+-1.jpg'),('PP0040','LP0010','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0010)+Acer+Predator+Helios+Neo+14/aphn14+-2.jpg'),('PP0041','LP0010','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0010)+Acer+Predator+Helios+Neo+14/aphn14+-3.jpg'),('PP0042','LP0010','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0010)+Acer+Predator+Helios+Neo+14/aphn14+-4.jpg'),('PP0043','LP0011','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0011)+Acer+ConceptD+3+Ezel/ac3e+-1.jpg'),('PP0044','LP0011','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0011)+Acer+ConceptD+3+Ezel/ac3e+-2.jpg'),('PP0045','LP0011','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0011)+Acer+ConceptD+3+Ezel/ac3e+-3.jpg'),('PP0046','LP0011','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0011)+Acer+ConceptD+3+Ezel/ac3e+-4.jpg'),('PP0047','LP0012','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0012)+Acer+Predator+Trition+17+X/apt17x+-1.jpg'),('PP0048','LP0012','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0012)+Acer+Predator+Trition+17+X/apt17x+-2.jpg'),('PP0049','LP0012','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0012)+Acer+Predator+Trition+17+X/apt17x+-3.jpg'),('PP0050','LP0012','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0012)+Acer+Predator+Trition+17+X/apt17x+-4.jpg'),('PP0051','LP0013','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0013)+Acer+Predator+Helios+18/aph18-1.jpg'),('PP0052','LP0013','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0013)+Acer+Predator+Helios+18/aph18-2.jpg'),('PP0053','LP0013','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0013)+Acer+Predator+Helios+18/aph18-3.jpg'),('PP0054','LP0014','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0014)+Acer+Predator+Triton+14/apt14+-1.jpg'),('PP0055','LP0014','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0014)+Acer+Predator+Triton+14/apt14+-2.jpg'),('PP0056','LP0014','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0014)+Acer+Predator+Triton+14/apt14+-3.jpg'),('PP0057','LP0014','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0001-LP0014)+Acer/(LP0014)+Acer+Predator+Triton+14/apt14+-4.jpg'),('PP0058','LP0015','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0015-LP0019)+Asus/(LP0015)+Asus+ROG+Zephyrus+G14/arzg14-+1.jpg'),('PP0059','LP0015','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0015-LP0019)+Asus/(LP0015)+Asus+ROG+Zephyrus+G14/arzg14-+2.jpg'),('PP0060','LP0015','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0015-LP0019)+Asus/(LP0015)+Asus+ROG+Zephyrus+G14/arzg14-+3.jpg'),('PP0061','LP0015','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0015-LP0019)+Asus/(LP0015)+Asus+ROG+Zephyrus+G14/arzg14-+4.jpg'),('PP0062','LP0015','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0015-LP0019)+Asus/(LP0015)+Asus+ROG+Zephyrus+G14/arzg14-+5.jpg'),('PP0063','LP0016','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0015-LP0019)+Asus/(LP0016)+Asus+TUF+Gaming+F15/atgf15+-1.jpg'),('PP0064','LP0016','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0015-LP0019)+Asus/(LP0016)+Asus+TUF+Gaming+F15/atgf15+-2.jpg'),('PP0065','LP0016','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0015-LP0019)+Asus/(LP0016)+Asus+TUF+Gaming+F15/atgf15+-3.jpg'),('PP0066','LP0016','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0015-LP0019)+Asus/(LP0016)+Asus+TUF+Gaming+F15/atgf15+-4.jpg'),('PP0067','LP0017','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0015-LP0019)+Asus/(LP0017)+Asus+ZenBook+14/az14+-1.jpg'),('PP0068','LP0017','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0015-LP0019)+Asus/(LP0017)+Asus+ZenBook+14/az14+-2.jpg'),('PP0069','LP0017','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0015-LP0019)+Asus/(LP0017)+Asus+ZenBook+14/az14+-3.jpg'),('PP0070','LP0017','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0015-LP0019)+Asus/(LP0017)+Asus+ZenBook+14/az14+-4.jpg'),('PP0071','LP0017','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0015-LP0019)+Asus/(LP0017)+Asus+ZenBook+14/az14+-5.jpg'),('PP0072','LP0018','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0015-LP0019)+Asus/(LP0018)+Asus+VivoBook+S14/avs14+-1.jpg'),('PP0073','LP0018','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0015-LP0019)+Asus/(LP0018)+Asus+VivoBook+S14/avs14+-2.jpg'),('PP0074','LP0018','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0015-LP0019)+Asus/(LP0018)+Asus+VivoBook+S14/avs14+-3.jpg'),('PP0075','LP0018','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0015-LP0019)+Asus/(LP0018)+Asus+VivoBook+S14/avs14+-4.jpg'),('PP0076','LP0019','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0015-LP0019)+Asus/(LP0019)+Asus+ROG+Strix+G15/arsg15+-1.jpg'),('PP0077','LP0019','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0015-LP0019)+Asus/(LP0019)+Asus+ROG+Strix+G15/arsg15+-2.jpg'),('PP0078','LP0019','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0015-LP0019)+Asus/(LP0019)+Asus+ROG+Strix+G15/arsg15+-3.jpg'),('PP0079','LP0019','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0015-LP0019)+Asus/(LP0019)+Asus+ROG+Strix+G15/arsg15+-4.jpg'),('PP0080','LP0020','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0020-LP0024)+Dell/(LP0020)+Dell+XPS+13/dxps13+-1.jpg'),('PP0081','LP0020','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0020-LP0024)+Dell/(LP0020)+Dell+XPS+13/dxps13+-2.jpg'),('PP0082','LP0020','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0020-LP0024)+Dell/(LP0020)+Dell+XPS+13/dxps13+-3.jpg'),('PP0083','LP0020','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0020-LP0024)+Dell/(LP0020)+Dell+XPS+13/dxps13+-4.jpg'),('PP0084','LP0020','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0020-LP0024)+Dell/(LP0020)+Dell+XPS+13/dxps13+-5.jpg'),('PP0085','LP0021','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0020-LP0024)+Dell/(LP0021)+Dell+G5+15/dg515-+1.jpg'),('PP0086','LP0021','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0020-LP0024)+Dell/(LP0021)+Dell+G5+15/dg515-+2.jpg'),('PP0087','LP0021','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0020-LP0024)+Dell/(LP0021)+Dell+G5+15/dg515-+3.jpg'),('PP0088','LP0021','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0020-LP0024)+Dell/(LP0021)+Dell+G5+15/dg515-+4.jpg'),('PP0089','LP0021','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0020-LP0024)+Dell/(LP0021)+Dell+G5+15/dg515-+5.jpg'),('PP0090','LP0022','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0020-LP0024)+Dell/(LP0022)+Dell+Inspiron+15+5000/di15+-1.jpg'),('PP0091','LP0022','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0020-LP0024)+Dell/(LP0022)+Dell+Inspiron+15+5000/di15+-2.jpg'),('PP0092','LP0022','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0020-LP0024)+Dell/(LP0022)+Dell+Inspiron+15+5000/di15+-3.jpg'),('PP0093','LP0022','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0020-LP0024)+Dell/(LP0022)+Dell+Inspiron+15+5000/di15+-4.jpg'),('PP0094','LP0023','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0020-LP0024)+Dell/(LP0023)+Dell+Latitude+7420/dl7420+-1.jpg'),('PP0095','LP0023','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0020-LP0024)+Dell/(LP0023)+Dell+Latitude+7420/dl7420+-2.jpg'),('PP0096','LP0023','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0020-LP0024)+Dell/(LP0023)+Dell+Latitude+7420/dl7420+-3.jpg'),('PP0097','LP0023','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0020-LP0024)+Dell/(LP0023)+Dell+Latitude+7420/dl7420+-4.jpg'),('PP0098','LP0024','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0020-LP0024)+Dell/(LP0024)+Dell+Alienware+m15+R6/dam15+-1.jpg'),('PP0099','LP0024','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0020-LP0024)+Dell/(LP0024)+Dell+Alienware+m15+R6/dam15+-2.jpg'),('PP0100','LP0024','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0020-LP0024)+Dell/(LP0024)+Dell+Alienware+m15+R6/dam15+-3.jpg'),('PP0101','LP0024','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0020-LP0024)+Dell/(LP0024)+Dell+Alienware+m15+R6/dam15+-4.jpg'),('PP0102','LP0025','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0025-LP0029)+Hp/(LP0025)+Hp+Spectre+x360+14/hpsx360+-1.jpg'),('PP0103','LP0025','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0025-LP0029)+Hp/(LP0025)+Hp+Spectre+x360+14/hpsx360+-2.jpg'),('PP0104','LP0025','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0025-LP0029)+Hp/(LP0025)+Hp+Spectre+x360+14/hpsx360+-3.jpg'),('PP0105','LP0025','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0025-LP0029)+Hp/(LP0025)+Hp+Spectre+x360+14/hpsx360+-4.jpg'),('PP0106','LP0026','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0025-LP0029)+Hp/(LP0026)+Hp+Omen+15/ho15+-1.jpg'),('PP0107','LP0026','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0025-LP0029)+Hp/(LP0026)+Hp+Omen+15/ho15+-2.jpg'),('PP0108','LP0026','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0025-LP0029)+Hp/(LP0026)+Hp+Omen+15/ho15+-3.jpg'),('PP0109','LP0026','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0025-LP0029)+Hp/(LP0026)+Hp+Omen+15/ho15+-4.jpg'),('PP0110','LP0026','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0025-LP0029)+Hp/(LP0026)+Hp+Omen+15/ho15+-5.jpg'),('PP0111','LP0027','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0025-LP0029)+Hp/(LP0027)+Hp+Pavilion+x360/hpx360+-1.jpg'),('PP0112','LP0027','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0025-LP0029)+Hp/(LP0027)+Hp+Pavilion+x360/hpx360+-2.jpg'),('PP0113','LP0027','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0025-LP0029)+Hp/(LP0027)+Hp+Pavilion+x360/hpx360+-3.jpg'),('PP0114','LP0027','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0025-LP0029)+Hp/(LP0027)+Hp+Pavilion+x360/hpx360+-4.jpg'),('PP0115','LP0027','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0025-LP0029)+Hp/(LP0027)+Hp+Pavilion+x360/hpx360+-5.jpg'),('PP0116','LP0028','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0025-LP0029)+Hp/(LP0028)+Hp+Envy+13/he13+-1.jpg'),('PP0117','LP0028','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0025-LP0029)+Hp/(LP0028)+Hp+Envy+13/he13+-2.jpg'),('PP0118','LP0028','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0025-LP0029)+Hp/(LP0028)+Hp+Envy+13/he13+-3.jpg'),('PP0119','LP0028','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0025-LP0029)+Hp/(LP0028)+Hp+Envy+13/he13+-4.jpg'),('PP0120','LP0029','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0025-LP0029)+Hp/(LP0029)+Hp+Elite+Dragonfly/hed-1.jpg'),('PP0121','LP0029','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0025-LP0029)+Hp/(LP0029)+Hp+Elite+Dragonfly/hed-2.jpg'),('PP0122','LP0029','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0025-LP0029)+Hp/(LP0029)+Hp+Elite+Dragonfly/hed-3.jpg'),('PP0123','LP0029','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0025-LP0029)+Hp/(LP0029)+Hp+Elite+Dragonfly/hed-4.jpg'),('PP0124','LP0030','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0030-LP0035)+Lenovo/(LP0030)+Lenovo+Legion+5+Pro/ll5p-1.jpg'),('PP0125','LP0030','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0030-LP0035)+Lenovo/(LP0030)+Lenovo+Legion+5+Pro/ll5p-2.jpg'),('PP0126','LP0030','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0030-LP0035)+Lenovo/(LP0030)+Lenovo+Legion+5+Pro/ll5p-3.jpg'),('PP0127','LP0030','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0030-LP0035)+Lenovo/(LP0030)+Lenovo+Legion+5+Pro/ll5p-4.jpg'),('PP0128','LP0031','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0030-LP0035)+Lenovo/(LP0031)+Lenovo+ThinkPad+X1+Carbon+Gen9/ltxcg9-1.jpg'),('PP0129','LP0031','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0030-LP0035)+Lenovo/(LP0031)+Lenovo+ThinkPad+X1+Carbon+Gen9/ltxcg9-2.jpg'),('PP0130','LP0031','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0030-LP0035)+Lenovo/(LP0031)+Lenovo+ThinkPad+X1+Carbon+Gen9/ltxcg9-3.jpg'),('PP0131','LP0031','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0030-LP0035)+Lenovo/(LP0031)+Lenovo+ThinkPad+X1+Carbon+Gen9/ltxcg9-4.jpg'),('PP0132','LP0032','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0030-LP0035)+Lenovo/(LP0032)+Lenovo+Yoga+9i/ly9i+-1.jpg'),('PP0133','LP0032','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0030-LP0035)+Lenovo/(LP0032)+Lenovo+Yoga+9i/ly9i+-2.jpg'),('PP0134','LP0032','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0030-LP0035)+Lenovo/(LP0032)+Lenovo+Yoga+9i/ly9i+-3.jpg'),('PP0135','LP0032','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0030-LP0035)+Lenovo/(LP0032)+Lenovo+Yoga+9i/ly9i+-4.jpg'),('PP0136','LP0033','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0030-LP0035)+Lenovo/(LP0033)+Lenovo+IdeaPad+3/li3+-1.jpg'),('PP0137','LP0033','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0030-LP0035)+Lenovo/(LP0033)+Lenovo+IdeaPad+3/li3+-2.jpg'),('PP0138','LP0033','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0030-LP0035)+Lenovo/(LP0033)+Lenovo+IdeaPad+3/li3+-3.jpg'),('PP0139','LP0033','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0030-LP0035)+Lenovo/(LP0033)+Lenovo+IdeaPad+3/li3+-4.jpg'),('PP0140','LP0034','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0030-LP0035)+Lenovo/(LP0034)+Lenovo+ThinkBook+14s+Yoga/lt14y+-1.jpg'),('PP0141','LP0034','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0030-LP0035)+Lenovo/(LP0034)+Lenovo+ThinkBook+14s+Yoga/lt14y+-2jpg'),('PP0142','LP0034','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0030-LP0035)+Lenovo/(LP0034)+Lenovo+ThinkBook+14s+Yoga/lt14y+-3.jpg'),('PP0143','LP0034','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0030-LP0035)+Lenovo/(LP0034)+Lenovo+ThinkBook+14s+Yoga/lt14y+-4.jpg'),('PP0144','LP0035','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0030-LP0035)+Lenovo/(LP0035)+Lenovo+Legion+Pro+7i/l7p+-1.jpg'),('PP0145','LP0035','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0030-LP0035)+Lenovo/(LP0035)+Lenovo+Legion+Pro+7i/l7p+-2.jpg'),('PP0146','LP0035','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0030-LP0035)+Lenovo/(LP0035)+Lenovo+Legion+Pro+7i/l7p+-3.jpg'),('PP0147','LP0035','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0030-LP0035)+Lenovo/(LP0035)+Lenovo+Legion+Pro+7i/l7p+-4.jpg'),('PP0148','LP0036','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0036-LP0040)+MSI/(LP0036)+MSI+GS66+Stealth+13/mgs66+-1.jpg'),('PP0149','LP0036','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0036-LP0040)+MSI/(LP0036)+MSI+GS66+Stealth+13/mgs66+-2.jpg'),('PP0150','LP0036','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0036-LP0040)+MSI/(LP0036)+MSI+GS66+Stealth+13/mgs66+-3.jpg'),('PP0151','LP0036','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0036-LP0040)+MSI/(LP0036)+MSI+GS66+Stealth+13/mgs66+-4.jpg'),('PP0152','LP0037','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0036-LP0040)+MSI/(LP0037)+MSI+GE76+Raider/msi+raider-1.jpg'),('PP0153','LP0037','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0036-LP0040)+MSI/(LP0037)+MSI+GE76+Raider/msi+raider-2.jpg'),('PP0154','LP0037','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0036-LP0040)+MSI/(LP0037)+MSI+GE76+Raider/msi+raider-3.jpg'),('PP0155','LP0037','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0036-LP0040)+MSI/(LP0037)+MSI+GE76+Raider/msi+raider-4.jpg'),('PP0156','LP0038','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0036-LP0040)+MSI/(LP0038)+MSI+Prestige+14/msi+prestige-1.jpg'),('PP0157','LP0038','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0036-LP0040)+MSI/(LP0038)+MSI+Prestige+14/msi+prestige-2.jpg'),('PP0158','LP0038','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0036-LP0040)+MSI/(LP0038)+MSI+Prestige+14/msi+prestige-3.jpg'),('PP0159','LP0038','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0036-LP0040)+MSI/(LP0038)+MSI+Prestige+14/msi+prestige-4.jpg'),('PP0160','LP0039','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0036-LP0040)+MSI/(LP0039)+MSI+Modern+14/msi+modern-1.jpg'),('PP0161','LP0039','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0036-LP0040)+MSI/(LP0039)+MSI+Modern+14/msi+modern-2.jpg'),('PP0162','LP0039','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0036-LP0040)+MSI/(LP0039)+MSI+Modern+14/msi+modern-3.jpg'),('PP0163','LP0039','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0036-LP0040)+MSI/(LP0039)+MSI+Modern+14/msi+modern-4.jpg'),('PP0164','LP0040','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0036-LP0040)+MSI/(LP0040)+MSI+Creator+15/msi+creator-1.jpg'),('PP0165','LP0040','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0036-LP0040)+MSI/(LP0040)+MSI+Creator+15/msi+creator-2.jpg'),('PP0166','LP0040','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0036-LP0040)+MSI/(LP0040)+MSI+Creator+15/msi+creator-3.jpg'),('PP0167','LP0040','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0036-LP0040)+MSI/(LP0040)+MSI+Creator+15/msi+creator-4.jpg'),('PP0168','LP0041','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0041-LP0045)+Razer/(LP0041)+Razer+Blade+15/rb15-1.jpg'),('PP0169','LP0041','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0041-LP0045)+Razer/(LP0041)+Razer+Blade+15/rb15-2.jpg'),('PP0170','LP0041','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0041-LP0045)+Razer/(LP0041)+Razer+Blade+15/rb15-3.jpg'),('PP0171','LP0041','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0041-LP0045)+Razer/(LP0041)+Razer+Blade+15/rb15-4.jpg'),('PP0172','LP0042','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0041-LP0045)+Razer/(LP0042)+Razer+Blade+Stealth+13/rbs13-1.jpg'),('PP0173','LP0042','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0041-LP0045)+Razer/(LP0042)+Razer+Blade+Stealth+13/rbs13-2.jpg'),('PP0174','LP0042','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0041-LP0045)+Razer/(LP0042)+Razer+Blade+Stealth+13/rbs13-3.jpg'),('PP0175','LP0042','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0041-LP0045)+Razer/(LP0042)+Razer+Blade+Stealth+13/rbs13-4.jpg'),('PP0176','LP0043','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0041-LP0045)+Razer/(LP0043)+Razer+Book+13/rb13+-1.jpg'),('PP0177','LP0043','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0041-LP0045)+Razer/(LP0043)+Razer+Book+13/rb13+-2.jpg'),('PP0178','LP0043','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0041-LP0045)+Razer/(LP0043)+Razer+Book+13/rb13+-3.jpg'),('PP0179','LP0043','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0041-LP0045)+Razer/(LP0043)+Razer+Book+13/rb13+-4.jpg'),('PP0180','LP0044','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0041-LP0045)+Razer/(LP0044)+Razer+Blade+14/rb14+-1.jpg'),('PP0181','LP0044','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0041-LP0045)+Razer/(LP0044)+Razer+Blade+14/rb14+-2.jpg'),('PP0182','LP0044','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0041-LP0045)+Razer/(LP0044)+Razer+Blade+14/rb14+-3.jpg'),('PP0183','LP0044','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0041-LP0045)+Razer/(LP0044)+Razer+Blade+14/rb14+-4.jpg'),('PP0184','LP0045','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0041-LP0045)+Razer/(LP0045)+Razer+Blade+Pro+17/rb17-1.jpg'),('PP0185','LP0045','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0041-LP0045)+Razer/(LP0045)+Razer+Blade+Pro+17/rb17-2.jpg'),('PP0186','LP0045','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0041-LP0045)+Razer/(LP0045)+Razer+Blade+Pro+17/rb17-3.jpg'),('PP0187','LP0045','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0041-LP0045)+Razer/(LP0045)+Razer+Blade+Pro+17/rb17-4.jpg'),('PP0188','LP0046','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0046-LP0050)+Huawei/(LP0046)+Huawei+MateBook+X+Pro/hmxp+-1.jpg'),('PP0189','LP0046','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0046-LP0050)+Huawei/(LP0046)+Huawei+MateBook+X+Pro/hmxp+-2.jpg'),('PP0190','LP0046','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0046-LP0050)+Huawei/(LP0046)+Huawei+MateBook+X+Pro/hmxp+-3.jpg'),('PP0191','LP0046','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0046-LP0050)+Huawei/(LP0046)+Huawei+MateBook+X+Pro/hmxp+-4.jpg'),('PP0192','LP0047','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0046-LP0050)+Huawei/(LP0047)+Huawei+MateBook+14/hm14+-1.jpg'),('PP0193','LP0047','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0046-LP0050)+Huawei/(LP0047)+Huawei+MateBook+14/hm14+-2.jpg'),('PP0194','LP0047','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0046-LP0050)+Huawei/(LP0047)+Huawei+MateBook+14/hm14+-3.jpg'),('PP0195','LP0047','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0046-LP0050)+Huawei/(LP0047)+Huawei+MateBook+14/hm14+-4.jpg'),('PP0196','LP0048','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0046-LP0050)+Huawei/(LP0048)+Huawei+MateBook+D+15/hmd15+-1.jpg'),('PP0197','LP0048','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0046-LP0050)+Huawei/(LP0048)+Huawei+MateBook+D+15/hmd15+-2.jpg'),('PP0198','LP0048','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0046-LP0050)+Huawei/(LP0048)+Huawei+MateBook+D+15/hmd15+-3.jpg'),('PP0199','LP0048','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0046-LP0050)+Huawei/(LP0048)+Huawei+MateBook+D+15/hmd15+-4.jpg'),('PP0200','LP0049','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0046-LP0050)+Huawei/(LP0049)+Huawei+MateBook+13/hm13+-1.jpg'),('PP0201','LP0049','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0046-LP0050)+Huawei/(LP0049)+Huawei+MateBook+13/hm13+-2.jpg'),('PP0202','LP0049','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0046-LP0050)+Huawei/(LP0049)+Huawei+MateBook+13/hm13+-3.jpg'),('PP0203','LP0049','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0046-LP0050)+Huawei/(LP0049)+Huawei+MateBook+13/hm13+-4.jpg'),('PP0204','LP0050','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0046-LP0050)+Huawei/(LP0050)+Huawei+MateBook+X/hmx+-1.jpg'),('PP0205','LP0050','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0046-LP0050)+Huawei/(LP0050)+Huawei+MateBook+X/hmx+-2.jpg'),('PP0206','LP0050','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0046-LP0050)+Huawei/(LP0050)+Huawei+MateBook+X/hmx+-3.jpg'),('PP0207','LP0050','https://sourc-wk-sdp-project.s3.amazonaws.com/(LP0046-LP0050)+Huawei/(LP0050)+Huawei+MateBook+X/hmx+-4.jpg');
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
  `processed_by` char(6) DEFAULT NULL,
  `saved_card_id` char(6) NOT NULL,
  PRIMARY KEY (`order_id`,`product_id`),
  UNIQUE KEY `order_id` (`order_id`),
  KEY `username` (`username`),
  KEY `product_id` (`product_id`),
  KEY `saved_card_id` (`saved_card_id`),
  CONSTRAINT `purchase_ibfk_1` FOREIGN KEY (`username`) REFERENCES `user` (`username`) ON UPDATE CASCADE,
  CONSTRAINT `purchase_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE,
  CONSTRAINT `purchase_ibfk_3` FOREIGN KEY (`saved_card_id`) REFERENCES `payment` (`saved_card_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchase`
--

LOCK TABLES `purchase` WRITE;
/*!40000 ALTER TABLE `purchase` DISABLE KEYS */;
INSERT INTO `purchase` VALUES ('IN0001','wkwk','LP0001','2024-08-07 03:53:29',12000,'pending',1,NULL,'PC0001'),('IN0002','wkwk','LP0001','2024-08-07 04:04:40',12000,'pending',1,NULL,'PC0001'),('IN0003','wkwk','LP0001','2024-08-12 03:33:38',24000,'pending',2,NULL,'PC0001'),('IN0004','wkwk','LP0001','2024-08-14 03:49:59',12000,'pending',1,NULL,'PC0001'),('IN0005','wkwk','LP0001','2024-08-15 03:17:10',12000,'pending',1,NULL,'PC0001');
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
  `order_id` char(6) DEFAULT NULL,
  `product_id` char(6) DEFAULT NULL,
  `username` varchar(30) DEFAULT NULL,
  `review` varchar(255) DEFAULT NULL,
  `rating` int NOT NULL,
  `review_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `reply` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`review_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `review_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `review`
--

LOCK TABLES `review` WRITE;
/*!40000 ALTER TABLE `review` DISABLE KEYS */;
INSERT INTO `review` VALUES ('RV0001','IN0001','LP0001','wkwk','haha',5,'2024-08-07 03:54:01',NULL),('RV0002','IN0002','LP0001','wkwk','ninj',1,'2024-08-07 04:04:56',NULL);
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
  `search_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
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
INSERT INTO `search_history` VALUES ('SC0001','wkwk','f3f','2024-08-04 16:35:42'),('SC0002','wkwk','acer','2024-08-04 16:35:47'),('SC0003','wkwk','acer','2024-08-04 16:55:02'),('SC0004','wkwk','acer','2024-08-04 16:55:07'),('SC0005','wkwk','acer','2024-08-04 16:55:18'),('SC0006','wkwk','acer','2024-08-04 16:57:37'),('SC0007','wkwk','acer','2024-08-04 16:57:41'),('SC0008','wkwk','pre','2024-08-07 03:52:11');
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
INSERT INTO `shipping` VALUES ('SH0001','IN0001','geg','erg','0168953485','pending','2024-08-07 03:53:29'),('SH0002','IN0002','109-3-2 Jalan Pudu Ulu, Pudu Impian 1','Chong Wen Kang','0166893432','pending','2024-08-07 04:04:40'),('SH0003','IN0003','109-3-2 Jalan Pudu Ulu, Pudu Impian 1','Chong Wen Kang','0166893432','pending','2024-08-12 03:33:38'),('SH0004','IN0004','Lot Puchong, 13, Lorong Kenangan 2, Kampung Kenangan, 47100 Puchong, Selangor','Chong Wen Kang','0123882384','pending','2024-08-14 03:49:59'),('SH0005','IN0005','109-3-2 Jalan Pudu Ulu, Pudu Impian 1','Chong Wen Kang','0166893432','pending','2024-08-15 03:17:10');
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
INSERT INTO `user` VALUES ('aaa','asd','Chong Wen Kang','braynchongwenkang590@gmail.com','0126843432','2024-06-05',NULL,NULL,NULL),('sw','sss','sw','shynwei04@gmail.com','1323','2024-07-03','11, JALAN BEDARA','fe',NULL),('timi','dfg6543@','wyt','timi04@gmail.com','0157463967','2000-09-22','Lot Puchong, 13, Lorong Kenangan 2, Kampung Kenangan, 47100 Puchong, Selangor','Student',NULL),('wkwk','wk','wen kang','braynchong590@gmail.com','0166893432','2024-07-13','asd','asd','https://sourc-wk-sdp-project.s3.amazonaws.com/User Profile Picture/wkwk');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_recommendations`
--

DROP TABLE IF EXISTS `user_recommendations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_recommendations` (
  `username` varchar(30) NOT NULL,
  `product_id_1` char(6) DEFAULT NULL,
  `score_1` decimal(5,2) DEFAULT NULL,
  `product_id_2` char(6) DEFAULT NULL,
  `score_2` decimal(5,2) DEFAULT NULL,
  `product_id_3` char(6) DEFAULT NULL,
  `score_3` decimal(5,2) DEFAULT NULL,
  `product_id_4` char(6) DEFAULT NULL,
  `score_4` decimal(5,2) DEFAULT NULL,
  `product_id_5` char(6) DEFAULT NULL,
  `score_5` decimal(5,2) DEFAULT NULL,
  `product_id_6` char(6) DEFAULT NULL,
  `score_6` decimal(5,2) DEFAULT NULL,
  `product_id_7` char(6) DEFAULT NULL,
  `score_7` decimal(5,2) DEFAULT NULL,
  `product_id_8` char(6) DEFAULT NULL,
  `score_8` decimal(5,2) DEFAULT NULL,
  `product_id_9` char(6) DEFAULT NULL,
  `score_9` decimal(5,2) DEFAULT NULL,
  `product_id_10` char(6) DEFAULT NULL,
  `score_10` decimal(5,2) DEFAULT NULL,
  `product_id_11` char(6) DEFAULT NULL,
  `score_11` decimal(5,2) DEFAULT NULL,
  `product_id_12` char(6) DEFAULT NULL,
  `score_12` decimal(5,2) DEFAULT NULL,
  `product_id_13` char(6) DEFAULT NULL,
  `score_13` decimal(5,2) DEFAULT NULL,
  `product_id_14` char(6) DEFAULT NULL,
  `score_14` decimal(5,2) DEFAULT NULL,
  `product_id_15` char(6) DEFAULT NULL,
  `score_15` decimal(5,2) DEFAULT NULL,
  `product_id_16` char(6) DEFAULT NULL,
  `score_16` decimal(5,2) DEFAULT NULL,
  `product_id_17` char(6) DEFAULT NULL,
  `score_17` decimal(5,2) DEFAULT NULL,
  `product_id_18` char(6) DEFAULT NULL,
  `score_18` decimal(5,2) DEFAULT NULL,
  `product_id_19` char(6) DEFAULT NULL,
  `score_19` decimal(5,2) DEFAULT NULL,
  `product_id_20` char(6) DEFAULT NULL,
  `score_20` decimal(5,2) DEFAULT NULL,
  `product_id_21` char(6) DEFAULT NULL,
  `score_21` decimal(5,2) DEFAULT NULL,
  `product_id_22` char(6) DEFAULT NULL,
  `score_22` decimal(5,2) DEFAULT NULL,
  `product_id_23` char(6) DEFAULT NULL,
  `score_23` decimal(5,2) DEFAULT NULL,
  `product_id_24` char(6) DEFAULT NULL,
  `score_24` decimal(5,2) DEFAULT NULL,
  `product_id_25` char(6) DEFAULT NULL,
  `score_25` decimal(5,2) DEFAULT NULL,
  `product_id_26` char(6) DEFAULT NULL,
  `score_26` decimal(5,2) DEFAULT NULL,
  `product_id_27` char(6) DEFAULT NULL,
  `score_27` decimal(5,2) DEFAULT NULL,
  `product_id_28` char(6) DEFAULT NULL,
  `score_28` decimal(5,2) DEFAULT NULL,
  `product_id_29` char(6) DEFAULT NULL,
  `score_29` decimal(5,2) DEFAULT NULL,
  `product_id_30` char(6) DEFAULT NULL,
  `score_30` decimal(5,2) DEFAULT NULL,
  `last_updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`username`),
  KEY `product_id_1` (`product_id_1`),
  KEY `product_id_2` (`product_id_2`),
  KEY `product_id_3` (`product_id_3`),
  KEY `product_id_4` (`product_id_4`),
  KEY `product_id_5` (`product_id_5`),
  KEY `product_id_6` (`product_id_6`),
  KEY `product_id_7` (`product_id_7`),
  KEY `product_id_8` (`product_id_8`),
  KEY `product_id_9` (`product_id_9`),
  KEY `product_id_10` (`product_id_10`),
  KEY `product_id_11` (`product_id_11`),
  KEY `product_id_12` (`product_id_12`),
  KEY `product_id_13` (`product_id_13`),
  KEY `product_id_14` (`product_id_14`),
  KEY `product_id_15` (`product_id_15`),
  KEY `product_id_16` (`product_id_16`),
  KEY `product_id_17` (`product_id_17`),
  KEY `product_id_18` (`product_id_18`),
  KEY `product_id_19` (`product_id_19`),
  KEY `product_id_20` (`product_id_20`),
  KEY `product_id_21` (`product_id_21`),
  KEY `product_id_22` (`product_id_22`),
  KEY `product_id_23` (`product_id_23`),
  KEY `product_id_24` (`product_id_24`),
  KEY `product_id_25` (`product_id_25`),
  KEY `product_id_26` (`product_id_26`),
  KEY `product_id_27` (`product_id_27`),
  KEY `product_id_28` (`product_id_28`),
  KEY `product_id_29` (`product_id_29`),
  KEY `product_id_30` (`product_id_30`),
  CONSTRAINT `user_recommendations_ibfk_1` FOREIGN KEY (`username`) REFERENCES `user` (`username`) ON UPDATE CASCADE,
  CONSTRAINT `user_recommendations_ibfk_10` FOREIGN KEY (`product_id_9`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE,
  CONSTRAINT `user_recommendations_ibfk_11` FOREIGN KEY (`product_id_10`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE,
  CONSTRAINT `user_recommendations_ibfk_12` FOREIGN KEY (`product_id_11`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE,
  CONSTRAINT `user_recommendations_ibfk_13` FOREIGN KEY (`product_id_12`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE,
  CONSTRAINT `user_recommendations_ibfk_14` FOREIGN KEY (`product_id_13`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE,
  CONSTRAINT `user_recommendations_ibfk_15` FOREIGN KEY (`product_id_14`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE,
  CONSTRAINT `user_recommendations_ibfk_16` FOREIGN KEY (`product_id_15`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE,
  CONSTRAINT `user_recommendations_ibfk_17` FOREIGN KEY (`product_id_16`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE,
  CONSTRAINT `user_recommendations_ibfk_18` FOREIGN KEY (`product_id_17`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE,
  CONSTRAINT `user_recommendations_ibfk_19` FOREIGN KEY (`product_id_18`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE,
  CONSTRAINT `user_recommendations_ibfk_2` FOREIGN KEY (`product_id_1`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE,
  CONSTRAINT `user_recommendations_ibfk_20` FOREIGN KEY (`product_id_19`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE,
  CONSTRAINT `user_recommendations_ibfk_21` FOREIGN KEY (`product_id_20`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE,
  CONSTRAINT `user_recommendations_ibfk_22` FOREIGN KEY (`product_id_21`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE,
  CONSTRAINT `user_recommendations_ibfk_23` FOREIGN KEY (`product_id_22`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE,
  CONSTRAINT `user_recommendations_ibfk_24` FOREIGN KEY (`product_id_23`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE,
  CONSTRAINT `user_recommendations_ibfk_25` FOREIGN KEY (`product_id_24`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE,
  CONSTRAINT `user_recommendations_ibfk_26` FOREIGN KEY (`product_id_25`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE,
  CONSTRAINT `user_recommendations_ibfk_27` FOREIGN KEY (`product_id_26`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE,
  CONSTRAINT `user_recommendations_ibfk_28` FOREIGN KEY (`product_id_27`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE,
  CONSTRAINT `user_recommendations_ibfk_29` FOREIGN KEY (`product_id_28`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE,
  CONSTRAINT `user_recommendations_ibfk_3` FOREIGN KEY (`product_id_2`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE,
  CONSTRAINT `user_recommendations_ibfk_30` FOREIGN KEY (`product_id_29`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE,
  CONSTRAINT `user_recommendations_ibfk_31` FOREIGN KEY (`product_id_30`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE,
  CONSTRAINT `user_recommendations_ibfk_4` FOREIGN KEY (`product_id_3`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE,
  CONSTRAINT `user_recommendations_ibfk_5` FOREIGN KEY (`product_id_4`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE,
  CONSTRAINT `user_recommendations_ibfk_6` FOREIGN KEY (`product_id_5`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE,
  CONSTRAINT `user_recommendations_ibfk_7` FOREIGN KEY (`product_id_6`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE,
  CONSTRAINT `user_recommendations_ibfk_8` FOREIGN KEY (`product_id_7`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE,
  CONSTRAINT `user_recommendations_ibfk_9` FOREIGN KEY (`product_id_8`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_recommendations`
--

LOCK TABLES `user_recommendations` WRITE;
/*!40000 ALTER TABLE `user_recommendations` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_recommendations` ENABLE KEYS */;
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

-- Dump completed on 2024-08-15 11:48:53
