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
INSERT INTO `cart` VALUES ('jh_33','LP0026',1),('jh_33','LP0033',1),('kaiy','LP0009',1),('kaiy','LP0016',1),('kh_888','LP0004',1),('kh_888','LP0020',1),('sw_0418','LP0024',1),('sw_0418','LP0042',1),('timi','LP0013',1),('timi','LP0017',2),('wk','LP0001',1),('wk','LP0006',1),('yh_22','LP0006',1),('zx','LP0039',1),('zx','LP0041',1);
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
INSERT INTO `feedback` VALUES ('FB0001','SF0001','the system is smooth','2024-08-20 13:08:00',NULL),('FB0002','SF0002','I love the system','2024-08-22 11:43:59',NULL),('FB0003','SF0003','how to see the laptop image?','2024-08-22 16:43:59',NULL),('FB0004','SF0004','The image is clear','2024-08-23 16:43:59',NULL),('FB0005','SF0005','Good','2024-08-15 05:02:59',NULL),('FB0006','SF0006','Awesome system','2024-08-20 16:43:59',NULL),('FB0007','SF0007','I\'m getting used to it','2024-08-22 16:43:59',NULL),('FB0008','SF0008','I\'m new, luckily the system is easy to use','2024-08-22 18:43:50',NULL),('FB0009','SF0001','wao, the laptop management became easier compared to old times','2024-08-23 19:43:59',NULL),('FB0010','SF0002','Orders management is good','2024-08-24 15:43:59',NULL);
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
  `status` tinyint(1) NOT NULL DEFAULT '1',
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
INSERT INTO `payment` VALUES ('PC0001','timi','timi wee','1008998233456098','189','08/27','timiweeyuetim@gmail.com',1),('PC0002','wk','wen kang','1846776541129008','108','10/30','braynchongwenkang590@gmail.com',1),('PC0003','kh_888','kai hong','6657884399008880','302','06/27','kaihong@gmail.com',1),('PC0004','kaiy','kai yong','1845332700089917','754','08/25','vandyck@gmail.com',1),('PC0005','yh_22','yung hao','6654313388756001','778','08/28','yyhao0422@gmail.com',1),('PC0006','jh_33','jo hern','5312776549009876','587','08/27','johern@gmail.com',1),('PC0007','zx','zhi xian','4439239497581218','665','01/25','zhixian@gmail.com',1),('PC0008','sw_0418','shyn wei','1736234012644120','790','05/28','sw0418@gmail.com',1),('PC0009','timi','timi','1008887472859728','339','08/25','timiweeyuetim@gmail.com',1),('PC0010','timi','timi wee','4432575609169059','747','05/29','timiweeyuetim@gmail.com',0);
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
  `status` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`product_id`),
  UNIQUE KEY `product_id` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES ('LP0001','Acer Predator Helios 300','Acer','Intel Core i7-10750H','NVIDIA GeForce RTX 2060','363 x 255 x 22.9 mm',2500,'Windows 10','16GB DDR4','512GB PCIe NVMe SSD','230W','59 Wh',12000,20,1),('LP0002','Acer Swift 3','Acer','AMD Ryzen 7 4700U','AMD Radeon Graphics','323 x 218 x 15.9 mm',1190,'Windows 10','8GB LPDDR4X','512GB PCIe NVMe SSD','65W','48 Wh',6000,20,1),('LP0003','Acer Aspire 5','Acer','Intel Core i5-1135G7','Intel Iris Xe Graphics','363.4 x 238.5 x 17.9 mm',1700,'Windows 10','8GB DDR4','256GB PCIe NVMe SSD','65W','48 Wh',5000,30,1),('LP0004','Acer Spin 5','Acer','Intel Core i7-1065G7','Intel Iris Plus Graphics','304.6 x 230.6 x 15.9 mm',1200,'Windows 10','16GB LPDDR4X','512GB PCIe NVMe SSD','65W','56 Wh',9000,40,1),('LP0005','Acer Nitro 5','Acer','AMD Ryzen 5 4600H','NVIDIA GeForce GTX 1650','363.4 x 255 x 23.9 mm',2500,'Windows 10','8GB DDR4','256GB PCIe NVMe SSD','135W','58 Wh',7000,30,1),('LP0006','Acer Chromebook Spin 713','Acer','Intel Core i5-1135G7','Intel Iris Xe Graphics','312.6 x 224 x 18 mm',1400,'Chrome OS','8GB','256GB SSD','150W','48 Wh',3233,20,1),('LP0007','Acer Chromebook 315','Acer','Intel Celeron N4000','Intel UHD Graphics','320 x 206 x 17.5 mm',1900,'Chrome OS','4GB','32GB','160W','52 Wh',843,20,1),('LP0008','Acer Chromebook 516 GE','Acer','Intel Core i5-1240P','Intel Iris Xe Graphics','358 x 264 x 23.4 mm',1700,'Chrome OS','8GB','256GB','230W','80 Wh',2544,0,1),('LP0009','Aspire Go 15','Acer','Intel Core i3-N305','Intel UHD Graphics','396.2 x 211.3 x 17 mm',1750,'Windows 11','8GB','512TB','65W','50 Wh',1899,30,1),('LP0010','Predator Helios Neo 14','Acer','Intel Core Ultra 9','NVIDIA GeForce RTX 4070','313.5 x 211.3 x 17 mm',2100,'Windows 11','32GB','1TB','230W','76 Wh',7799,20,1),('LP0011','Acer ConceptD 3 Ezel','Acer','Intel Core i7-10750H','NVIDIA GeForce GTX 1650 Max-Q','322.5 x 228 x 20 mm',1700,'Windows 10','16GB DDR4','1TB PCIe NVMe SSD','135W','76 Wh',15000,0,1),('LP0012','Predator Triton 17 X','Acer','Intel Core i9-13900HX','NVIDIA GeForce RTX 4090','358 x 264 x 23.4 mm',3000,'Windows 11','64GB','4TB','330W','100 Wh',18999,20,1),('LP0013','Predator Helios 18','Acer','Intel Core i9-13900HX','NVIDIA GeForce RTX 4080','405 x 311.6 x 28.9 mm',3400,'Windows 11','32GB','2TB','330W','90 Wh',12999,20,1),('LP0014','Predator Triton 14','Acer','Intel Core i7-13700H','NVIDIA GeForce RTX 4070','313.5 x 227 x 19.9 mm',1700,'Windows 11','32GB','1TB','230W','76 Wh',8999,0,1),('LP0015','Asus ROG Zephyrus G14','Asus','AMD Ryzen 9 5900HS','NVIDIA GeForce RTX 3060','324 x 222 x 19.9 mm',1700,'Windows 10','16GB DDR4','1TB PCIe NVMe SSD','180W','76 Wh',12000,20,1),('LP0016','Asus TUF Gaming F15','Asus','Intel Core i5-10300H','NVIDIA GeForce GTX 1650','359 x 256 x 24.7 mm',2300,'Windows 10','8GB DDR4','512GB PCIe NVMe SSD','150W','48 Wh',6000,20,1),('LP0017','Asus ZenBook 14','Asus','AMD Ryzen 7 5800U','AMD Radeon Graphics','319 x 210 x 14.3 mm',1400,'Windows 10','16GB LPDDR4X','1TB PCIe NVMe SSD','65W','63 Wh',8000,20,1),('LP0018','Asus VivoBook S14','Asus','Intel Core i7-1165G7','Intel Iris Xe Graphics','323 x 211 x 15.9 mm',1500,'Windows 10','16GB DDR4','512GB PCIe NVMe SSD','65W','67 Wh',7000,20,1),('LP0019','Asus ROG Strix G15','Asus','AMD Ryzen 7 5800H','NVIDIA GeForce RTX 3050 Ti','354 x 259 x 27.2 mm',2300,'Windows 10','16GB DDR4','512GB PCIe NVMe SSD','200W','90 Wh',9000,20,1),('LP0020','Dell XPS 13','Dell','Intel Core i7-1165G7','Intel Iris Xe Graphics','295.7 x 198.7 x 14.8 mm',1200,'Windows 10','16GB LPDDR4x','512GB PCIe NVMe SSD','45W','52 Wh',10000,20,1),('LP0021','Dell G5 15','Dell','Intel Core i7-10750H','NVIDIA GeForce GTX 1660 Ti','364 x 273 x 23.7 mm',2500,'Windows 10','16GB DDR4','1TB PCIe NVMe SSD','180W','68 Wh',8000,20,1),('LP0022','Dell Inspiron 15 5000','Dell','Intel Core i5-1135G7','Intel Iris Xe Graphics','356 x 234 x 18 mm',1750,'Windows 10','8GB DDR4','512GB PCIe NVMe SSD','65W','53 Wh',5000,20,1),('LP0023','Dell Latitude 7420','Dell','Intel Core i7-1185G7','Intel Iris Xe Graphics','305.7 x 207.5 x 17.6 mm',1320,'Windows 10','16GB LPDDR4x','1TB PCIe NVMe SSD','65W','63 Wh',12000,20,1),('LP0024','Dell Alienware m15 R6','Dell','Intel Core i7-11800H','NVIDIA GeForce RTX 3070','356.2 x 272.5 x 22.9 mm',2400,'Windows 10','16GB DDR4','1TB PCIe NVMe SSD','240W','86 Wh',14000,20,1),('LP0025','HP Spectre x360 14','HP','Intel Core i7-1165G7','Intel Iris Xe Graphics','298.5 x 220.4 x 16.9 mm',1400,'Windows 10','16GB LPDDR4x','512GB PCIe NVMe SSD','65W','66 Wh',11000,20,1),('LP0026','HP Omen 15','HP','AMD Ryzen 7 5800H','NVIDIA GeForce RTX 3060','357.9 x 239.7 x 22.6 mm',2400,'Windows 10','16GB DDR4','1TB PCIe NVMe SSD','200W','70.9 Wh',13000,20,1),('LP0027','HP Pavilion x360','HP','Intel Core i5-1135G7','Intel Iris Xe Graphics','308.5 x 206 x 17.9 mm',1600,'Windows 10','8GB DDR4','256GB PCIe NVMe SSD','45W','43 Wh',6000,20,1),('LP0028','HP Envy 13','HP','Intel Core i7-1165G7','Intel Iris Xe Graphics','306.5 x 194.6 x 16.9 mm',1200,'Windows 10','16GB LPDDR4x','512GB PCIe NVMe SSD','65W','53 Wh',9000,20,1),('LP0029','HP Elite Dragonfly','HP','Intel Core i7-1165G7','Intel Iris Xe Graphics','304.3 x 197.5 x 16.1 mm',990,'Windows 10','16GB LPDDR4x','1TB PCIe NVMe SSD','65W','56.2 Wh',15000,30,1),('LP0030','Lenovo Legion 5 Pro','Lenovo','AMD Ryzen 7 5800H','NVIDIA GeForce RTX 3070','356 x 260.4 x 26.7 mm',2540,'Windows 11','16GB DDR4','1TB PCIe NVMe SSD','300W','80 Wh',8000,20,1),('LP0031','Lenovo ThinkPad X1 Carbon Gen 9','Lenovo','Intel Core i7-1165G7','Intel Iris Xe Graphics','314.5 x 221.6 x 14.9 mm',1130,'Windows 11','16GB LPDDR4X','512GB PCIe NVMe SSD','65W','57 Wh',10000,20,1),('LP0032','Lenovo Yoga 9i','Lenovo','Intel Core i7-1185G7','Intel Iris Xe Graphics','320.4 x 216.7 x 16.1 mm',1300,'Windows 11','16GB LPDDR4X','1TB PCIe NVMe SSD','65W','60 Wh',9000,20,1),('LP0033','Lenovo IdeaPad 3','Lenovo','AMD Ryzen 5 5500U','AMD Radeon Graphics','327.1 x 241 x 19.9 mm',1650,'Windows 10','8GB DDR4','512GB PCIe NVMe SSD','65W','45 Wh',4000,20,1),('LP0034','Lenovo ThinkBook 14s Yoga','Lenovo','Intel Core i7-1165G7','Intel Iris Xe Graphics','320.5 x 216.5 x 16.9 mm',1500,'Windows 11','16GB DDR4','512GB PCIe NVMe SSD','65W','60 Wh',8000,20,1),('LP0035','Legion Pro 7i','Lenovo','Intel Core i9-13900HX','NVIDIA GeForce RTX 4080','320 x 220 x 16.8 mm',2100,'Windows 11 Pro','32GB DDR5','1TB SSD','330W','100 Wh',12469,20,1),('LP0036','MSI GS66 Stealth','MSI','Intel Core i7-10875H','NVIDIA GeForce RTX 2070 Super','358.3 x 248 x 19.8 mm',2100,'Windows 10','32GB DDR4','1TB PCIe NVMe SSD','230W','99.9 Wh',15000,20,1),('LP0037','MSI GE76 Raider','MSI','Intel Core i9-11980HK','NVIDIA GeForce RTX 3080','397.6 x 284.5 x 25.9 mm',2900,'Windows 10','32GB DDR4','1TB PCIe NVMe SSD','280W','99.9 Wh',18000,20,1),('LP0038','MSI Prestige 14','MSI','Intel Core i7-1185G7','Intel Iris Xe Graphics','319 x 215 x 15.9 mm',1200,'Windows 10','16GB LPDDR4x','512GB PCIe NVMe SSD','65W','52 Wh',9000,20,1),('LP0039','MSI Modern 14','MSI','Intel Core i5-10210U','Intel UHD Graphics','322 x 222 x 16.9 mm',1300,'Windows 10','8GB DDR4','512GB PCIe NVMe SSD','65W','52 Wh',5000,21,1),('LP0040','MSI Creator 15','MSI','Intel Core i7-10875H','NVIDIA GeForce RTX 2060','358 x 248 x 19.8 mm',2100,'Windows 10','32GB DDR4','1TB PCIe NVMe SSD','230W','99.9 Wh',14000,20,1),('LP0041','Razer Blade 15','Razer','Intel Core i7-11800H','NVIDIA GeForce RTX 3070','355 x 235 x 17 mm',2040,'Windows 11','16GB DDR4','1TB PCIe NVMe SSD','230W','80 Wh',15000,20,1),('LP0042','Razer Blade Stealth 13','Razer','Intel Core i7-1165G7','Intel Iris Xe Graphics','304.6 x 210 x 15.3 mm',1360,'Windows 10','16GB LPDDR4x','512GB PCIe NVMe SSD','100W','53.1 Wh',12000,20,1),('LP0043','Razer Book 13','Razer','Intel Core i7-1165G7','Intel Iris Xe Graphics','295 x 198.5 x 15.1 mm',1350,'Windows 10','16GB LPDDR4x','512GB PCIe NVMe SSD','65W','55 Wh',13000,20,1),('LP0044','Razer Blade 14','Razer','AMD Ryzen 9 5900HX','NVIDIA GeForce RTX 3060','319.7 x 220 x 16.8 mm',1750,'Windows 11','16GB DDR4','1TB PCIe NVMe SSD','230W','61.6 Wh',14000,20,1),('LP0045','Razer Blade Pro 17','Razer','Intel Core i7-10875H','NVIDIA GeForce RTX 2080 Super','395 x 260 x 19.9 mm',2900,'Windows 10','32GB DDR4','1TB PCIe NVMe SSD','230W','70.5 Wh',18000,20,1),('LP0046','Huawei MateBook X Pro','Huawei','Intel Core i7-1165G7','Intel Iris Xe Graphics','304 x 217 x 14.6 mm',1330,'Windows 10','16GB LPDDR4x','1TB SSD','65W','56 Wh',12000,20,1),('LP0047','Huawei MateBook 14','Huawei','AMD Ryzen 7 4800H','AMD Radeon Graphics','307.5 x 223.8 x 15.9 mm',1530,'Windows 10','16GB DDR4','512GB PCIe NVMe SSD','65W','56 Wh',9000,20,1),('LP0048','Huawei MateBook D 15','Huawei','AMD Ryzen 5 3500U','AMD Radeon Vega 8 Graphics','357.8 x 229.9 x 16.9 mm',1530,'Windows 10','8GB DDR4','256GB PCIe NVMe SSD','65W','42 Wh',5000,20,1),('LP0049','Huawei MateBook 13','Huawei','Intel Core i5-1135G7','Intel Iris Xe Graphics','286 x 211 x 14.9 mm',1290,'Windows 10','16GB LPDDR4x','512GB PCIe NVMe SSD','65W','42 Wh',7000,20,1),('LP0050','Huawei MateBook X','Huawei','Intel Core i5-10210U','Intel UHD Graphics','284.4 x 206.7 x 13.6 mm',1000,'Windows 10','16GB LPDDR3','512GB PCIe NVMe SSD','65W','42 Wh',8000,20,1);
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
  `order_id` char(6) NOT NULL,
  `username` varchar(30) NOT NULL,
  `product_id` char(6) NOT NULL,
  `pur_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `pur_amount` int NOT NULL,
  `pur_status` varchar(10) NOT NULL,
  `pur_quantity` int NOT NULL,
  `processed_by` char(6) DEFAULT NULL,
  `saved_card_id` char(6) NOT NULL,
  PRIMARY KEY (`order_id`,`product_id`),
  KEY `username` (`username`),
  KEY `product_id` (`product_id`),
  KEY `saved_card_id` (`saved_card_id`),
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
INSERT INTO `purchase` VALUES ('IN0001','timi','LP0018','2024-07-13 05:57:01',7000,'pending',1,NULL,'PC0009'),('IN0002','timi','LP0016','2024-07-15 05:57:46',6000,'pending',1,NULL,'PC0009'),('IN0003','wk','LP0013','2024-07-08 06:00:56',12999,'pending',1,NULL,'PC0010'),('IN0004','kh_888','LP0029','2024-07-28 06:04:16',40000,'pending',2,NULL,'PC0011'),('IN0004','kh_888','LP0031','2024-08-26 06:04:16',40000,'pending',1,NULL,'PC0011'),('IN0005','kaiy','LP0027','2024-08-26 06:07:14',6000,'pending',1,NULL,'PC0012'),('IN0006','kaiy','LP0023','2024-11-26 06:08:12',12000,'pending',1,NULL,'PC0012'),('IN0007','yh_22','LP0028','2024-06-26 06:10:57',18000,'pending',1,NULL,'PC0013'),('IN0007','yh_22','LP0047','2024-03-26 06:10:57',18000,'pending',1,NULL,'PC0013'),('IN0008','jh_33','LP0029','2024-08-26 06:15:44',15000,'pending',1,NULL,'PC0014'),('IN0009','zx','LP0040','2024-12-26 06:18:48',28000,'pending',2,NULL,'PC0015'),('IN0010','sw_0418','LP0020','2024-08-26 06:21:07',10000,'pending',1,NULL,'PC0016'),('IN0011','timi','LP0011','2023-03-15 03:00:00',30000,'pending',2,NULL,'PC0009'),('IN0012','wk','LP0012','2023-06-25 01:45:00',18999,'pending',1,NULL,'PC0002'),('IN0013','kh_888','LP0013','2023-08-30 06:20:00',25998,'pending',2,NULL,'PC0003'),('IN0014','kaiy','LP0014','2023-10-05 05:10:00',8999,'pending',1,NULL,'PC0004'),('IN0015','yh_22','LP0015','2023-11-12 08:30:00',36000,'pending',3,NULL,'PC0005'),('IN0016','jh_33','LP0016','2023-12-20 06:00:00',6000,'pending',1,NULL,'PC0006'),('IN0017','zx','LP0017','2024-01-25 09:15:00',16000,'pending',2,NULL,'PC0007'),('IN0018','sw_0418','LP0018','2024-02-13 07:45:00',7000,'pending',1,NULL,'PC0008'),('IN0019','timi','LP0019','2024-03-22 04:35:00',18000,'pending',2,NULL,'PC0001'),('IN0020','wk','LP0020','2024-04-05 10:50:00',10000,'pending',1,NULL,'PC0002'),('IN0021','kh_888','LP0021','2024-05-10 06:40:00',24000,'pending',3,NULL,'PC0003'),('IN0022','kaiy','LP0022','2024-06-15 05:05:00',10000,'pending',2,NULL,'PC0004'),('IN0023','yh_22','LP0023','2024-07-20 08:25:00',12000,'pending',1,NULL,'PC0005'),('IN0024','jh_33','LP0024','2024-08-28 11:10:00',28000,'pending',2,NULL,'PC0006'),('IN0025','zx','LP0025','2024-09-30 01:55:00',11000,'pending',1,NULL,'PC0007'),('IN0026','sw_0418','LP0026','2024-10-05 09:20:00',13000,'pending',1,NULL,'PC0008'),('IN0027','timi','LP0027','2024-11-15 07:00:00',12000,'pending',2,NULL,'PC0009'),('IN0028','wk','LP0028','2024-12-10 06:30:00',9000,'pending',1,NULL,'PC0002'),('IN0029','kh_888','LP0029','2024-01-18 03:45:00',45000,'pending',3,NULL,'PC0003'),('IN0030','kaiy','LP0030','2024-02-27 05:35:00',8000,'pending',1,NULL,'PC0004'),('IN0031','yh_22','LP0031','2024-03-20 08:50:00',20000,'pending',2,NULL,'PC0005'),('IN0032','jh_33','LP0032','2024-04-30 04:40:00',18000,'pending',2,NULL,'PC0006'),('IN0033','zx','LP0033','2024-05-17 06:15:00',12000,'pending',3,NULL,'PC0007'),('IN0034','sw_0418','LP0034','2024-06-25 02:55:00',16000,'pending',2,NULL,'PC0008'),('IN0035','timi','LP0035','2024-07-18 07:25:00',12469,'pending',1,NULL,'PC0009'),('IN0036','wk','LP0036','2024-08-29 04:20:00',30000,'pending',2,NULL,'PC0002'),('IN0037','kh_888','LP0037','2024-09-15 05:00:00',54000,'pending',3,NULL,'PC0003'),('IN0038','kaiy','LP0038','2024-10-10 03:45:00',9000,'pending',1,NULL,'PC0004'),('IN0039','yh_22','LP0039','2024-11-05 08:10:00',10000,'pending',2,NULL,'PC0005'),('IN0040','jh_33','LP0040','2024-12-20 10:00:00',14000,'pending',1,NULL,'PC0006'),('IN0041','zx','LP0041','2024-01-15 06:35:00',30000,'pending',2,NULL,'PC0007'),('IN0042','sw_0418','LP0042','2024-02-22 04:50:00',12000,'pending',1,NULL,'PC0008'),('IN0043','timi','LP0043','2024-03-19 05:20:00',13000,'pending',1,NULL,'PC0009'),('IN0044','wk','LP0044','2024-04-25 08:30:00',28000,'pending',2,NULL,'PC0002'),('IN0045','kh_888','LP0045','2024-05-18 03:40:00',36000,'pending',2,NULL,'PC0003'),('IN0046','kaiy','LP0046','2024-06-20 09:15:00',12000,'pending',1,NULL,'PC0004'),('IN0047','yh_22','LP0047','2024-07-25 07:10:00',18000,'pending',2,NULL,'PC0005'),('IN0048','jh_33','LP0048','2024-08-30 04:35:00',5000,'pending',1,NULL,'PC0006'),('IN0049','zx','LP0049','2024-09-15 06:20:00',7000,'pending',1,NULL,'PC0007'),('IN0050','sw_0418','LP0050','2024-10-10 10:00:00',16000,'pending',2,NULL,'PC0008'),('IN0051','timi','LP0010','2022-11-23 02:30:00',7799,'pending',1,NULL,'PC0009'),('IN0052','wk','LP0020','2022-12-11 01:15:00',20000,'pending',2,NULL,'PC0002'),('IN0053','kh_888','LP0030','2022-10-05 05:20:00',16000,'pending',2,NULL,'PC0003'),('IN0054','kaiy','LP0040','2022-09-01 04:10:00',9000,'pending',1,NULL,'PC0004'),('IN0055','yh_22','LP0029','2022-08-12 08:30:00',30000,'pending',2,NULL,'PC0005'),('IN0056','jh_33','LP0011','2022-01-15 03:25:00',15000,'pending',1,NULL,'PC0006'),('IN0057','zx','LP0012','2022-02-18 01:50:00',37998,'pending',2,NULL,'PC0007'),('IN0058','sw_0418','LP0013','2022-03-22 05:35:00',12999,'pending',1,NULL,'PC0008'),('IN0059','timi','LP0014','2022-04-25 07:10:00',17998,'pending',2,NULL,'PC0009'),('IN0060','wk','LP0015','2022-05-28 08:20:00',36000,'pending',3,NULL,'PC0002'),('IN0061','kh_888','LP0016','2022-06-30 06:05:00',12000,'pending',2,NULL,'PC0003'),('IN0062','kaiy','LP0017','2022-07-25 05:45:00',24000,'pending',3,NULL,'PC0004'),('IN0063','yh_22','LP0018','2022-08-30 04:20:00',7000,'pending',1,NULL,'PC0005'),('IN0064','jh_33','LP0019','2022-09-12 10:15:00',27000,'pending',3,NULL,'PC0006'),('IN0065','zx','LP0020','2022-10-28 08:50:00',20000,'pending',2,NULL,'PC0007'),('IN0066','sw_0418','LP0021','2022-11-05 06:40:00',16000,'pending',2,NULL,'PC0008'),('IN0067','timi','LP0022','2022-12-15 05:10:00',10000,'pending',2,NULL,'PC0009'),('IN0068','wk','LP0023','2022-01-30 02:05:00',12000,'pending',1,NULL,'PC0002'),('IN0069','kh_888','LP0024','2022-02-20 04:45:00',42000,'pending',3,NULL,'PC0003'),('IN0070','kaiy','LP0025','2022-03-28 07:25:00',22000,'pending',2,NULL,'PC0004'),('IN0071','yh_22','LP0026','2022-04-25 03:50:00',26000,'pending',2,NULL,'PC0005'),('IN0072','jh_33','LP0027','2022-05-30 09:00:00',12000,'pending',2,NULL,'PC0006'),('IN0073','zx','LP0028','2022-06-28 10:35:00',18000,'pending',2,NULL,'PC0007'),('IN0074','sw_0418','LP0029','2022-07-15 04:55:00',30000,'pending',2,NULL,'PC0008'),('IN0075','timi','LP0030','2022-08-29 05:20:00',16000,'pending',2,NULL,'PC0009'),('IN0076','wk','LP0031','2022-09-22 08:40:00',10000,'pending',1,NULL,'PC0002'),('IN0077','kh_888','LP0032','2022-10-30 06:15:00',18000,'pending',2,NULL,'PC0003'),('IN0078','kaiy','LP0033','2022-11-25 07:50:00',36000,'pending',3,NULL,'PC0004'),('IN0079','yh_22','LP0034','2022-12-31 09:30:00',16000,'pending',2,NULL,'PC0005'),('IN0080','jh_33','LP0035','2022-01-15 04:25:00',12469,'pending',1,NULL,'PC0006'),('IN0081','zx','LP0036','2023-01-12 05:40:00',15000,'pending',1,NULL,'PC0007'),('IN0082','sw_0418','LP0037','2023-02-25 06:50:00',36000,'pending',2,NULL,'PC0008'),('IN0083','timi','LP0038','2023-03-20 02:30:00',9000,'pending',1,NULL,'PC0009'),('IN0084','wk','LP0039','2023-04-15 04:55:00',15000,'pending',3,NULL,'PC0002'),('IN0085','kh_888','LP0040','2023-05-22 03:45:00',28000,'pending',2,NULL,'PC0003'),('IN0086','kaiy','LP0041','2023-06-18 07:25:00',30000,'pending',2,NULL,'PC0004'),('IN0087','yh_22','LP0042','2023-07-28 08:40:00',12000,'pending',1,NULL,'PC0005'),('IN0088','jh_33','LP0043','2023-08-25 02:50:00',13000,'pending',1,NULL,'PC0006'),('IN0089','zx','LP0044','2023-09-22 05:55:00',42000,'pending',3,NULL,'PC0007'),('IN0090','sw_0418','LP0045','2023-10-15 07:20:00',36000,'pending',2,NULL,'PC0008'),('IN0091','timi','LP0046','2023-11-20 03:35:00',24000,'pending',2,NULL,'PC0009'),('IN0092','wk','LP0047','2023-12-05 06:00:00',27000,'pending',3,NULL,'PC0002'),('IN0093','kh_888','LP0048','2023-01-28 05:20:00',10000,'pending',2,NULL,'PC0003'),('IN0094','kaiy','LP0049','2023-02-15 08:45:00',7000,'pending',1,NULL,'PC0004'),('IN0095','yh_22','LP0050','2023-03-30 04:35:00',8000,'pending',1,NULL,'PC0005'),('IN0096','jh_33','LP0001','2023-04-12 10:25:00',24000,'pending',2,NULL,'PC0006'),('IN0097','zx','LP0002','2023-05-20 03:55:00',12000,'pending',2,NULL,'PC0007'),('IN0098','sw_0418','LP0003','2023-06-25 02:30:00',25000,'pending',5,NULL,'PC0008'),('IN0099','timi','LP0004','2023-07-15 06:15:00',18000,'pending',2,NULL,'PC0009'),('IN0100','wk','LP0005','2023-08-20 04:10:00',35000,'pending',5,NULL,'PC0002');
/*!40000 ALTER TABLE `purchase` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recommendation`
--

DROP TABLE IF EXISTS `recommendation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recommendation` (
  `username` varchar(30) NOT NULL,
  `product_id` char(6) NOT NULL,
  `score` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`username`,`product_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `recommendation_ibfk_1` FOREIGN KEY (`username`) REFERENCES `user` (`username`) ON UPDATE CASCADE,
  CONSTRAINT `recommendation_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recommendation`
--

LOCK TABLES `recommendation` WRITE;
/*!40000 ALTER TABLE `recommendation` DISABLE KEYS */;
INSERT INTO `recommendation` VALUES ('jh_33','LP0001',31.13),('jh_33','LP0002',56.95),('jh_33','LP0003',61.26),('jh_33','LP0004',44.04),('jh_33','LP0005',52.65),('jh_33','LP0006',68.87),('jh_33','LP0007',78.48),('jh_33','LP0008',71.83),('jh_33','LP0009',74.61),('jh_33','LP0010',49.21),('jh_33','LP0011',18.21),('jh_33','LP0012',1.00),('jh_33','LP0013',26.83),('jh_33','LP0014',44.05),('jh_33','LP0015',31.13),('jh_33','LP0016',100.00),('jh_33','LP0017',48.35),('jh_33','LP0018',52.65),('jh_33','LP0019',44.04),('jh_33','LP0020',39.74),('jh_33','LP0021',48.35),('jh_33','LP0022',61.26),('jh_33','LP0023',31.13),('jh_33','LP0024',22.52),('jh_33','LP0025',35.43),('jh_33','LP0026',26.82),('jh_33','LP0027',56.95),('jh_33','LP0028',44.04),('jh_33','LP0029',18.21),('jh_33','LP0030',48.35),('jh_33','LP0031',39.74),('jh_33','LP0032',44.04),('jh_33','LP0033',65.56),('jh_33','LP0034',48.35),('jh_33','LP0035',29.11),('jh_33','LP0036',18.21),('jh_33','LP0037',5.30),('jh_33','LP0038',44.04),('jh_33','LP0039',61.26),('jh_33','LP0040',22.52),('jh_33','LP0041',18.21),('jh_33','LP0042',31.13),('jh_33','LP0043',26.82),('jh_33','LP0044',22.52),('jh_33','LP0045',5.30),('jh_33','LP0046',31.13),('jh_33','LP0047',44.04),('jh_33','LP0048',61.26),('jh_33','LP0049',52.65),('jh_33','LP0050',48.35),('kaiy','LP0001',27.00),('kaiy','LP0002',53.00),('kaiy','LP0003',75.00),('kaiy','LP0004',26.00),('kaiy','LP0005',54.00),('kaiy','LP0006',54.00),('kaiy','LP0007',1.00),('kaiy','LP0008',55.00),('kaiy','LP0009',84.00),('kaiy','LP0010',59.00),('kaiy','LP0011',26.00),('kaiy','LP0012',57.00),('kaiy','LP0013',57.00),('kaiy','LP0014',57.00),('kaiy','LP0015',27.00),('kaiy','LP0016',78.00),('kaiy','LP0017',27.00),('kaiy','LP0018',26.00),('kaiy','LP0019',27.00),('kaiy','LP0020',26.00),('kaiy','LP0021',26.00),('kaiy','LP0022',75.00),('kaiy','LP0023',26.00),('kaiy','LP0024',27.00),('kaiy','LP0025',50.00),('kaiy','LP0026',54.00),('kaiy','LP0027',100.00),('kaiy','LP0028',50.00),('kaiy','LP0029',50.00),('kaiy','LP0030',54.00),('kaiy','LP0031',50.00),('kaiy','LP0032',50.00),('kaiy','LP0033',53.00),('kaiy','LP0034',50.00),('kaiy','LP0035',54.00),('kaiy','LP0036',26.00),('kaiy','LP0037',27.00),('kaiy','LP0038',26.00),('kaiy','LP0039',77.00),('kaiy','LP0040',27.00),('kaiy','LP0041',53.00),('kaiy','LP0042',26.00),('kaiy','LP0043',26.00),('kaiy','LP0044',54.00),('kaiy','LP0045',26.00),('kaiy','LP0046',27.00),('kaiy','LP0047',27.00),('kaiy','LP0048',51.00),('kaiy','LP0049',50.00),('kaiy','LP0050',51.00),('kh_888','LP0001',31.13),('kh_888','LP0002',56.95),('kh_888','LP0003',61.26),('kh_888','LP0004',44.04),('kh_888','LP0005',52.65),('kh_888','LP0006',68.87),('kh_888','LP0007',78.48),('kh_888','LP0008',71.83),('kh_888','LP0009',74.61),('kh_888','LP0010',49.21),('kh_888','LP0011',18.21),('kh_888','LP0012',1.00),('kh_888','LP0013',26.83),('kh_888','LP0014',44.05),('kh_888','LP0015',31.13),('kh_888','LP0016',100.00),('kh_888','LP0017',48.35),('kh_888','LP0018',52.65),('kh_888','LP0019',44.04),('kh_888','LP0020',39.74),('kh_888','LP0021',48.35),('kh_888','LP0022',61.26),('kh_888','LP0023',31.13),('kh_888','LP0024',22.52),('kh_888','LP0025',35.43),('kh_888','LP0026',26.82),('kh_888','LP0027',56.95),('kh_888','LP0028',44.04),('kh_888','LP0029',18.21),('kh_888','LP0030',48.35),('kh_888','LP0031',39.74),('kh_888','LP0032',44.04),('kh_888','LP0033',65.56),('kh_888','LP0034',48.35),('kh_888','LP0035',29.11),('kh_888','LP0036',18.21),('kh_888','LP0037',5.30),('kh_888','LP0038',44.04),('kh_888','LP0039',61.26),('kh_888','LP0040',22.52),('kh_888','LP0041',18.21),('kh_888','LP0042',31.13),('kh_888','LP0043',26.82),('kh_888','LP0044',22.52),('kh_888','LP0045',5.30),('kh_888','LP0046',31.13),('kh_888','LP0047',44.04),('kh_888','LP0048',61.26),('kh_888','LP0049',52.65),('kh_888','LP0050',48.35),('sw_0418','LP0001',1.00),('sw_0418','LP0002',1.00),('sw_0418','LP0003',1.00),('sw_0418','LP0004',1.00),('sw_0418','LP0005',1.00),('sw_0418','LP0006',1.00),('sw_0418','LP0007',1.00),('sw_0418','LP0008',1.00),('sw_0418','LP0009',1.00),('sw_0418','LP0010',1.00),('sw_0418','LP0011',1.00),('sw_0418','LP0012',1.00),('sw_0418','LP0013',1.00),('sw_0418','LP0014',1.00),('sw_0418','LP0015',1.00),('sw_0418','LP0016',1.00),('sw_0418','LP0017',1.00),('sw_0418','LP0018',1.00),('sw_0418','LP0019',1.00),('sw_0418','LP0020',96.00),('sw_0418','LP0021',98.00),('sw_0418','LP0022',96.00),('sw_0418','LP0023',96.00),('sw_0418','LP0024',100.00),('sw_0418','LP0025',1.00),('sw_0418','LP0026',1.00),('sw_0418','LP0027',1.00),('sw_0418','LP0028',1.00),('sw_0418','LP0029',1.00),('sw_0418','LP0030',1.00),('sw_0418','LP0031',1.00),('sw_0418','LP0032',1.00),('sw_0418','LP0033',1.00),('sw_0418','LP0034',1.00),('sw_0418','LP0035',1.00),('sw_0418','LP0036',1.00),('sw_0418','LP0037',1.00),('sw_0418','LP0038',1.00),('sw_0418','LP0039',1.00),('sw_0418','LP0040',1.00),('sw_0418','LP0041',1.00),('sw_0418','LP0042',1.00),('sw_0418','LP0043',1.00),('sw_0418','LP0044',1.00),('sw_0418','LP0045',1.00),('sw_0418','LP0046',1.00),('sw_0418','LP0047',1.00),('sw_0418','LP0048',1.00),('sw_0418','LP0049',1.00),('sw_0418','LP0050',1.00),('timi','LP0001',31.13),('timi','LP0002',56.95),('timi','LP0003',61.26),('timi','LP0004',44.04),('timi','LP0005',52.65),('timi','LP0006',68.87),('timi','LP0007',78.48),('timi','LP0008',71.83),('timi','LP0009',74.61),('timi','LP0010',49.21),('timi','LP0011',18.21),('timi','LP0012',1.00),('timi','LP0013',26.83),('timi','LP0014',44.05),('timi','LP0015',31.13),('timi','LP0016',100.00),('timi','LP0017',48.35),('timi','LP0018',52.65),('timi','LP0019',44.04),('timi','LP0020',39.74),('timi','LP0021',48.35),('timi','LP0022',61.26),('timi','LP0023',31.13),('timi','LP0024',22.52),('timi','LP0025',35.43),('timi','LP0026',26.82),('timi','LP0027',56.95),('timi','LP0028',44.04),('timi','LP0029',18.21),('timi','LP0030',48.35),('timi','LP0031',39.74),('timi','LP0032',44.04),('timi','LP0033',65.56),('timi','LP0034',48.35),('timi','LP0035',29.11),('timi','LP0036',18.21),('timi','LP0037',5.30),('timi','LP0038',44.04),('timi','LP0039',61.26),('timi','LP0040',22.52),('timi','LP0041',18.21),('timi','LP0042',31.13),('timi','LP0043',26.82),('timi','LP0044',22.52),('timi','LP0045',5.30),('timi','LP0046',31.13),('timi','LP0047',44.04),('timi','LP0048',61.26),('timi','LP0049',52.65),('timi','LP0050',48.35),('wk','LP0001',100.00),('wk','LP0002',1.00),('wk','LP0003',1.00),('wk','LP0004',64.00),('wk','LP0005',1.00),('wk','LP0006',1.00),('wk','LP0007',1.00),('wk','LP0008',1.00),('wk','LP0009',1.00),('wk','LP0010',38.00),('wk','LP0011',66.00),('wk','LP0012',37.00),('wk','LP0013',37.00),('wk','LP0014',73.00),('wk','LP0015',68.00),('wk','LP0016',1.00),('wk','LP0017',34.00),('wk','LP0018',64.00),('wk','LP0019',67.00),('wk','LP0020',64.00),('wk','LP0021',66.00),('wk','LP0022',1.00),('wk','LP0023',64.00),('wk','LP0024',100.00),('wk','LP0025',64.00),('wk','LP0026',68.00),('wk','LP0027',1.00),('wk','LP0028',64.00),('wk','LP0029',64.00),('wk','LP0030',68.00),('wk','LP0031',64.00),('wk','LP0032',64.00),('wk','LP0033',1.00),('wk','LP0034',64.00),('wk','LP0035',35.00),('wk','LP0036',66.00),('wk','LP0037',67.00),('wk','LP0038',64.00),('wk','LP0039',1.00),('wk','LP0040',67.00),('wk','LP0041',100.00),('wk','LP0042',64.00),('wk','LP0043',64.00),('wk','LP0044',68.00),('wk','LP0045',66.00),('wk','LP0046',67.00),('wk','LP0047',34.00),('wk','LP0048',1.00),('wk','LP0049',33.00),('wk','LP0050',33.00),('yh_22','LP0001',1.00),('yh_22','LP0002',48.00),('yh_22','LP0003',92.00),('yh_22','LP0004',1.00),('yh_22','LP0005',49.00),('yh_22','LP0006',98.00),('yh_22','LP0007',1.00),('yh_22','LP0008',100.00),('yh_22','LP0009',52.00),('yh_22','LP0010',1.00),('yh_22','LP0011',1.00),('yh_22','LP0012',1.00),('yh_22','LP0013',1.00),('yh_22','LP0014',1.00),('yh_22','LP0015',1.00),('yh_22','LP0016',96.00),('yh_22','LP0017',1.00),('yh_22','LP0018',1.00),('yh_22','LP0019',1.00),('yh_22','LP0020',1.00),('yh_22','LP0021',1.00),('yh_22','LP0022',92.00),('yh_22','LP0023',1.00),('yh_22','LP0024',1.00),('yh_22','LP0025',1.00),('yh_22','LP0026',1.00),('yh_22','LP0027',92.00),('yh_22','LP0028',1.00),('yh_22','LP0029',1.00),('yh_22','LP0030',1.00),('yh_22','LP0031',1.00),('yh_22','LP0032',1.00),('yh_22','LP0033',48.00),('yh_22','LP0034',1.00),('yh_22','LP0035',1.00),('yh_22','LP0036',1.00),('yh_22','LP0037',1.00),('yh_22','LP0038',1.00),('yh_22','LP0039',94.00),('yh_22','LP0040',1.00),('yh_22','LP0041',1.00),('yh_22','LP0042',1.00),('yh_22','LP0043',1.00),('yh_22','LP0044',1.00),('yh_22','LP0045',1.00),('yh_22','LP0046',1.00),('yh_22','LP0047',1.00),('yh_22','LP0048',47.00),('yh_22','LP0049',47.00),('yh_22','LP0050',47.00),('zx','LP0001',26.00),('zx','LP0002',50.00),('zx','LP0003',72.00),('zx','LP0004',25.00),('zx','LP0005',77.00),('zx','LP0006',52.00),('zx','LP0007',1.00),('zx','LP0008',53.00),('zx','LP0009',80.00),('zx','LP0010',57.00),('zx','LP0011',49.00),('zx','LP0012',55.00),('zx','LP0013',55.00),('zx','LP0014',55.00),('zx','LP0015',26.00),('zx','LP0016',100.00),('zx','LP0017',26.00),('zx','LP0018',25.00),('zx','LP0019',26.00),('zx','LP0020',25.00),('zx','LP0021',74.00),('zx','LP0022',72.00),('zx','LP0023',25.00),('zx','LP0024',26.00),('zx','LP0025',25.00),('zx','LP0026',26.00),('zx','LP0027',72.00),('zx','LP0028',25.00),('zx','LP0029',25.00),('zx','LP0030',52.00),('zx','LP0031',49.00),('zx','LP0032',49.00),('zx','LP0033',50.00),('zx','LP0034',49.00),('zx','LP0035',52.00),('zx','LP0036',49.00),('zx','LP0037',50.00),('zx','LP0038',49.00),('zx','LP0039',98.00),('zx','LP0040',50.00),('zx','LP0041',50.00),('zx','LP0042',25.00),('zx','LP0043',25.00),('zx','LP0044',52.00),('zx','LP0045',25.00),('zx','LP0046',26.00),('zx','LP0047',26.00),('zx','LP0048',49.00),('zx','LP0049',49.00),('zx','LP0050',49.00);
/*!40000 ALTER TABLE `recommendation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `report`
--

DROP TABLE IF EXISTS `report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `report` (
  `order_id` char(8) NOT NULL,
  `date_day` date DEFAULT NULL,
  `date_week` date DEFAULT NULL,
  `date_month` date DEFAULT NULL,
  `date_year` date DEFAULT NULL,
  `sales` decimal(10,2) DEFAULT NULL,
  `product_sold` int DEFAULT NULL,
  `product_id` char(6) DEFAULT NULL,
  `product_name` varchar(100) DEFAULT NULL,
  `total_order` int DEFAULT NULL,
  `total_user` int DEFAULT NULL,
  `new_user` int DEFAULT NULL,
  PRIMARY KEY (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `report`
--

LOCK TABLES `report` WRITE;
/*!40000 ALTER TABLE `report` DISABLE KEYS */;
INSERT INTO `report` VALUES ('IN0001','2024-07-13','2024-07-08','2024-07-01','2024-01-01',7000.00,1,'LP0018','Asus VivoBook S14',1,10,10),('IN0002','2024-07-15','2024-07-15','2024-07-01','2024-01-01',6000.00,1,'LP0016','Asus TUF Gaming F15',1,10,10),('IN0003','2024-07-08','2024-07-08','2024-07-01','2024-01-01',12999.00,1,'LP0013','Predator Helios 18',1,10,10),('IN0004','2024-07-28','2024-07-22','2024-07-01','2024-01-01',40000.00,2,'LP0029','HP Elite Dragonfly',1,10,10),('IN0005','2024-08-26','2024-08-26','2024-08-01','2024-01-01',6000.00,1,'LP0027','HP Pavilion x360',4,10,10),('IN0006','2024-11-26','2024-11-25','2024-11-01','2024-01-01',12000.00,1,'LP0023','Dell Latitude 7420',1,10,10),('IN0007','2024-06-26','2024-06-24','2024-06-01','2024-01-01',18000.00,1,'LP0028','HP Envy 13',1,10,10),('IN0008','2024-08-26','2024-08-26','2024-08-01','2024-01-01',15000.00,1,'LP0029','HP Elite Dragonfly',4,10,10),('IN0009','2024-12-26','2024-12-23','2024-12-01','2024-01-01',28000.00,2,'LP0040','MSI Creator 15',1,10,10),('IN0010','2024-08-26','2024-08-26','2024-08-01','2024-01-01',10000.00,1,'LP0020','Dell XPS 13',4,10,10),('IN0011','2023-03-15','2023-03-13','2023-03-01','2023-01-01',30000.00,2,'LP0011','Acer ConceptD 3 Ezel',1,10,10),('IN0012','2023-06-25','2023-06-19','2023-06-01','2023-01-01',18999.00,1,'LP0012','Predator Triton 17 X',2,10,10),('IN0013','2023-08-30','2023-08-28','2023-08-01','2023-01-01',25998.00,2,'LP0013','Predator Helios 18',1,10,10),('IN0014','2023-10-05','2023-10-02','2023-10-01','2023-01-01',8999.00,1,'LP0014','Predator Triton 14',1,10,10),('IN0015','2023-11-12','2023-11-06','2023-11-01','2023-01-01',36000.00,3,'LP0015','Asus ROG Zephyrus G14',1,10,10),('IN0016','2023-12-20','2023-12-18','2023-12-01','2023-01-01',6000.00,1,'LP0016','Asus TUF Gaming F15',1,10,10),('IN0017','2024-01-25','2024-01-22','2024-01-01','2024-01-01',16000.00,2,'LP0017','Asus ZenBook 14',1,10,10),('IN0018','2024-02-13','2024-02-12','2024-02-01','2024-01-01',7000.00,1,'LP0018','Asus VivoBook S14',1,10,10),('IN0019','2024-03-22','2024-03-18','2024-03-01','2024-01-01',18000.00,2,'LP0019','Asus ROG Strix G15',1,10,10),('IN0020','2024-04-05','2024-04-01','2024-04-01','2024-01-01',10000.00,1,'LP0020','Dell XPS 13',1,10,10),('IN0021','2024-05-10','2024-05-06','2024-05-01','2024-01-01',24000.00,3,'LP0021','Dell G5 15',1,10,10),('IN0022','2024-06-15','2024-06-10','2024-06-01','2024-01-01',10000.00,2,'LP0022','Dell Inspiron 15 5000',1,10,10),('IN0023','2024-07-20','2024-07-15','2024-07-01','2024-01-01',12000.00,1,'LP0023','Dell Latitude 7420',1,10,10),('IN0024','2024-08-28','2024-08-26','2024-08-01','2024-01-01',28000.00,2,'LP0024','Dell Alienware m15 R6',1,10,10),('IN0025','2024-09-30','2024-09-30','2024-09-01','2024-01-01',11000.00,1,'LP0025','HP Spectre x360 14',1,10,10),('IN0026','2024-10-05','2024-09-30','2024-10-01','2024-01-01',13000.00,1,'LP0026','HP Omen 15',1,10,10),('IN0027','2024-11-15','2024-11-11','2024-11-01','2024-01-01',12000.00,2,'LP0027','HP Pavilion x360',1,10,10),('IN0028','2024-12-10','2024-12-09','2024-12-01','2024-01-01',9000.00,1,'LP0028','HP Envy 13',1,10,10),('IN0029','2024-01-18','2024-01-15','2024-01-01','2024-01-01',45000.00,3,'LP0029','HP Elite Dragonfly',1,10,10),('IN0030','2024-02-27','2024-02-26','2024-02-01','2024-01-01',8000.00,1,'LP0030','Lenovo Legion 5 Pro',1,10,10),('IN0031','2024-03-20','2024-03-18','2024-03-01','2024-01-01',20000.00,2,'LP0031','Lenovo ThinkPad X1 Carbon Gen 9',1,10,10),('IN0032','2024-04-30','2024-04-29','2024-04-01','2024-01-01',18000.00,2,'LP0032','Lenovo Yoga 9i',1,10,10),('IN0033','2024-05-17','2024-05-13','2024-05-01','2024-01-01',12000.00,3,'LP0033','Lenovo IdeaPad 3',1,10,10),('IN0034','2024-06-25','2024-06-24','2024-06-01','2024-01-01',16000.00,2,'LP0034','Lenovo ThinkBook 14s Yoga',1,10,10),('IN0035','2024-07-18','2024-07-15','2024-07-01','2024-01-01',12469.00,1,'LP0035','Legion Pro 7i',1,10,10),('IN0036','2024-08-29','2024-08-26','2024-08-01','2024-01-01',30000.00,2,'LP0036','MSI GS66 Stealth',1,10,10),('IN0037','2024-09-15','2024-09-09','2024-09-01','2024-01-01',54000.00,3,'LP0037','MSI GE76 Raider',2,10,10),('IN0038','2024-10-10','2024-10-07','2024-10-01','2024-01-01',9000.00,1,'LP0038','MSI Prestige 14',2,10,10),('IN0039','2024-11-05','2024-11-04','2024-11-01','2024-01-01',10000.00,2,'LP0039','MSI Modern 14',1,10,10),('IN0040','2024-12-20','2024-12-16','2024-12-01','2024-01-01',14000.00,1,'LP0040','MSI Creator 15',1,10,10),('IN0041','2024-01-15','2024-01-15','2024-01-01','2024-01-01',30000.00,2,'LP0041','Razer Blade 15',1,10,10),('IN0042','2024-02-22','2024-02-19','2024-02-01','2024-01-01',12000.00,1,'LP0042','Razer Blade Stealth 13',1,10,10),('IN0043','2024-03-19','2024-03-18','2024-03-01','2024-01-01',13000.00,1,'LP0043','Razer Book 13',1,10,10),('IN0044','2024-04-25','2024-04-22','2024-04-01','2024-01-01',28000.00,2,'LP0044','Razer Blade 14',1,10,10),('IN0045','2024-05-18','2024-05-13','2024-05-01','2024-01-01',36000.00,2,'LP0045','Razer Blade Pro 17',1,10,10),('IN0046','2024-06-20','2024-06-17','2024-06-01','2024-01-01',12000.00,1,'LP0046','Huawei MateBook X Pro',1,10,10),('IN0047','2024-07-25','2024-07-22','2024-07-01','2024-01-01',18000.00,2,'LP0047','Huawei MateBook 14',1,10,10),('IN0048','2024-08-30','2024-08-26','2024-08-01','2024-01-01',5000.00,1,'LP0048','Huawei MateBook D 15',1,10,10),('IN0049','2024-09-15','2024-09-09','2024-09-01','2024-01-01',7000.00,1,'LP0049','Huawei MateBook 13',2,10,10),('IN0050','2024-10-10','2024-10-07','2024-10-01','2024-01-01',16000.00,2,'LP0050','Huawei MateBook X',2,10,10),('IN0051','2022-11-23','2022-11-21','2022-11-01','2022-01-01',7799.00,1,'LP0010','Predator Helios Neo 14',1,10,10),('IN0052','2022-12-11','2022-12-05','2022-12-01','2022-01-01',20000.00,2,'LP0020','Dell XPS 13',1,10,10),('IN0053','2022-10-05','2022-10-03','2022-10-01','2022-01-01',16000.00,2,'LP0030','Lenovo Legion 5 Pro',1,10,10),('IN0054','2022-09-01','2022-08-29','2022-09-01','2022-01-01',9000.00,1,'LP0040','MSI Creator 15',1,10,10),('IN0055','2022-08-12','2022-08-08','2022-08-01','2022-01-01',30000.00,2,'LP0029','HP Elite Dragonfly',1,10,10),('IN0056','2022-01-15','2022-01-10','2022-01-01','2022-01-01',15000.00,1,'LP0011','Acer ConceptD 3 Ezel',2,10,10),('IN0057','2022-02-18','2022-02-14','2022-02-01','2022-01-01',37998.00,2,'LP0012','Predator Triton 17 X',1,10,10),('IN0058','2022-03-22','2022-03-21','2022-03-01','2022-01-01',12999.00,1,'LP0013','Predator Helios 18',1,10,10),('IN0059','2022-04-25','2022-04-25','2022-04-01','2022-01-01',17998.00,2,'LP0014','Predator Triton 14',2,10,10),('IN0060','2022-05-28','2022-05-23','2022-05-01','2022-01-01',36000.00,3,'LP0015','Asus ROG Zephyrus G14',1,10,10),('IN0061','2022-06-30','2022-06-27','2022-06-01','2022-01-01',12000.00,2,'LP0016','Asus TUF Gaming F15',1,10,10),('IN0062','2022-07-25','2022-07-25','2022-07-01','2022-01-01',24000.00,3,'LP0017','Asus ZenBook 14',1,10,10),('IN0063','2022-08-30','2022-08-29','2022-08-01','2022-01-01',7000.00,1,'LP0018','Asus VivoBook S14',1,10,10),('IN0064','2022-09-12','2022-09-12','2022-09-01','2022-01-01',27000.00,3,'LP0019','Asus ROG Strix G15',1,10,10),('IN0065','2022-10-28','2022-10-24','2022-10-01','2022-01-01',20000.00,2,'LP0020','Dell XPS 13',1,10,10),('IN0066','2022-11-05','2022-10-31','2022-11-01','2022-01-01',16000.00,2,'LP0021','Dell G5 15',1,10,10),('IN0067','2022-12-15','2022-12-12','2022-12-01','2022-01-01',10000.00,2,'LP0022','Dell Inspiron 15 5000',1,10,10),('IN0068','2022-01-30','2022-01-24','2022-01-01','2022-01-01',12000.00,1,'LP0023','Dell Latitude 7420',1,10,10),('IN0069','2022-02-20','2022-02-14','2022-02-01','2022-01-01',42000.00,3,'LP0024','Dell Alienware m15 R6',1,10,10),('IN0070','2022-03-28','2022-03-28','2022-03-01','2022-01-01',22000.00,2,'LP0025','HP Spectre x360 14',1,10,10),('IN0071','2022-04-25','2022-04-25','2022-04-01','2022-01-01',26000.00,2,'LP0026','HP Omen 15',2,10,10),('IN0072','2022-05-30','2022-05-30','2022-05-01','2022-01-01',12000.00,2,'LP0027','HP Pavilion x360',1,10,10),('IN0073','2022-06-28','2022-06-27','2022-06-01','2022-01-01',18000.00,2,'LP0028','HP Envy 13',1,10,10),('IN0074','2022-07-15','2022-07-11','2022-07-01','2022-01-01',30000.00,2,'LP0029','HP Elite Dragonfly',1,10,10),('IN0075','2022-08-29','2022-08-29','2022-08-01','2022-01-01',16000.00,2,'LP0030','Lenovo Legion 5 Pro',1,10,10),('IN0076','2022-09-22','2022-09-19','2022-09-01','2022-01-01',10000.00,1,'LP0031','Lenovo ThinkPad X1 Carbon Gen 9',1,10,10),('IN0077','2022-10-30','2022-10-24','2022-10-01','2022-01-01',18000.00,2,'LP0032','Lenovo Yoga 9i',1,10,10),('IN0078','2022-11-25','2022-11-21','2022-11-01','2022-01-01',36000.00,3,'LP0033','Lenovo IdeaPad 3',1,10,10),('IN0079','2022-12-31','2022-12-26','2022-12-01','2022-01-01',16000.00,2,'LP0034','Lenovo ThinkBook 14s Yoga',1,10,10),('IN0080','2022-01-15','2022-01-10','2022-01-01','2022-01-01',12469.00,1,'LP0035','Legion Pro 7i',2,10,10),('IN0081','2023-01-12','2023-01-09','2023-01-01','2023-01-01',15000.00,1,'LP0036','MSI GS66 Stealth',1,10,10),('IN0082','2023-02-25','2023-02-20','2023-02-01','2023-01-01',36000.00,2,'LP0037','MSI GE76 Raider',1,10,10),('IN0083','2023-03-20','2023-03-20','2023-03-01','2023-01-01',9000.00,1,'LP0038','MSI Prestige 14',1,10,10),('IN0084','2023-04-15','2023-04-10','2023-04-01','2023-01-01',15000.00,3,'LP0039','MSI Modern 14',1,10,10),('IN0085','2023-05-22','2023-05-22','2023-05-01','2023-01-01',28000.00,2,'LP0040','MSI Creator 15',1,10,10),('IN0086','2023-06-18','2023-06-12','2023-06-01','2023-01-01',30000.00,2,'LP0041','Razer Blade 15',1,10,10),('IN0087','2023-07-28','2023-07-24','2023-07-01','2023-01-01',12000.00,1,'LP0042','Razer Blade Stealth 13',1,10,10),('IN0088','2023-08-25','2023-08-21','2023-08-01','2023-01-01',13000.00,1,'LP0043','Razer Book 13',1,10,10),('IN0089','2023-09-22','2023-09-18','2023-09-01','2023-01-01',42000.00,3,'LP0044','Razer Blade 14',1,10,10),('IN0090','2023-10-15','2023-10-09','2023-10-01','2023-01-01',36000.00,2,'LP0045','Razer Blade Pro 17',1,10,10),('IN0091','2023-11-20','2023-11-20','2023-11-01','2023-01-01',24000.00,2,'LP0046','Huawei MateBook X Pro',1,10,10),('IN0092','2023-12-05','2023-12-04','2023-12-01','2023-01-01',27000.00,3,'LP0047','Huawei MateBook 14',1,10,10),('IN0093','2023-01-28','2023-01-23','2023-01-01','2023-01-01',10000.00,2,'LP0048','Huawei MateBook D 15',1,10,10),('IN0094','2023-02-15','2023-02-13','2023-02-01','2023-01-01',7000.00,1,'LP0049','Huawei MateBook 13',1,10,10),('IN0095','2023-03-30','2023-03-27','2023-03-01','2023-01-01',8000.00,1,'LP0050','Huawei MateBook X',1,10,10),('IN0096','2023-04-12','2023-04-10','2023-04-01','2023-01-01',24000.00,2,'LP0001','Acer Predator Helios 300',1,10,10),('IN0097','2023-05-20','2023-05-15','2023-05-01','2023-01-01',12000.00,2,'LP0002','Acer Swift 3',1,10,10),('IN0098','2023-06-25','2023-06-19','2023-06-01','2023-01-01',25000.00,5,'LP0003','Acer Aspire 5',2,10,10),('IN0099','2023-07-15','2023-07-10','2023-07-01','2023-01-01',18000.00,2,'LP0004','Acer Spin 5',1,10,10),('IN0100','2023-08-20','2023-08-14','2023-08-01','2023-01-01',35000.00,5,'LP0005','Acer Nitro 5',1,10,10);
/*!40000 ALTER TABLE `report` ENABLE KEYS */;
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
INSERT INTO `review` VALUES ('RV0001','IN0001','LP0018','timi','I love this laptop, omg!',5,'2024-08-26 05:58:10',NULL),('RV0002','IN0003','LP0013','wk','fits me well, good recommendation, memang kaw kaw',5,'2024-08-26 06:01:20',NULL),('RV0003','IN0004','LP0031','kh_888','good website, will use in future',5,'2024-08-26 06:04:42',NULL),('RV0004','IN0005','LP0027','kaiy','yes, good one, perfectly match my needs.',5,'2024-08-26 06:07:35',NULL),('RV0005','IN0006','LP0023','kaiy','this latop is nice one!',4,'2024-08-26 06:08:38',NULL),('RV0006','IN0007','LP0028','yh_22','nice laptop',5,'2024-08-26 06:12:37',NULL),('RV0007','IN0002','LP0016','timi','my friend love it',4,'2024-08-26 06:13:52',NULL),('RV0008','IN0008','LP0029','jh_33','okay',3,'2024-08-26 06:16:00',NULL),('RV0009','IN0009','LP0040','zx','wuhuuu, cannot wait to explore my laptop',5,'2024-08-26 06:19:11',NULL),('RV0010','IN0010','LP0020','sw_0418','useful laptop',4,'2024-08-26 06:21:20','Thank you for your feedback!');
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
INSERT INTO `search_history` VALUES ('SC0001','timi','lenovo','2024-08-26 06:53:26'),('SC0002','timi','acer','2024-08-26 06:53:30'),('SC0003','sw_0418','acer','2024-08-26 06:54:16'),('SC0004','sw_0418','asus','2024-08-26 06:54:20'),('SC0005','sw_0418','msi ','2024-08-26 06:54:27'),('SC0006','sw_0418','Predator Triton 14','2024-08-26 06:54:38'),('SC0007','jh_33','asus tuf','2024-08-26 06:56:05'),('SC0008','jh_33','nvidia','2024-08-26 06:56:09'),('SC0009','jh_33','dell','2024-08-26 06:56:16'),('SC0010','jh_33','hp','2024-08-26 06:56:22'),('SC0011','jh_33','Asus ROG Zephyrus G14','2024-08-26 06:56:34');
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
INSERT INTO `shipping` VALUES ('SH0001','IN0001','1 26 Jln Manis 1 Taman Segar, KL, 56100','timi wee','0102705103','pending','2024-08-26 05:57:01'),('SH0002','IN0002','1 26 Jln Manis 1 Taman Segar, KL, 56100','timi wee','0102705103','pending','2024-08-26 05:57:46'),('SH0003','IN0003','11 JLN SUNGEI PULUH 5 TAMAN UTAMA, Klang, 41400','wen kang','0166893432','pending','2024-08-26 06:00:56'),('SH0004','IN0004','Jalan Berhala, Brickfields, 50470 Kuala Lumpur','kai','0162574578','pending','2024-08-26 06:04:16'),('SH0005','IN0005','76 Jalan Raja Muda Abdul Aziz, Jln Tun Razak, 50300 Kuala Lumpur','vandy','0198876123','pending','2024-08-26 06:07:14'),('SH0006','IN0006','76 Jalan Raja Muda Abdul Aziz, Jln Tun Razak, 50300 Kuala Lumpur','vandyck','0198876123','pending','2024-08-26 06:08:12'),('SH0007','IN0007','5, Lorong Peel, Maluri, 55100 Cheras','hao','0167331846','pending','2024-08-26 06:10:57'),('SH0008','IN0008','No. 18 1St Floor Jln Ss5A/9 Ss5, Petaling Jaya, Selangor, 47301','johern','0163314206','pending','2024-08-26 06:15:44'),('SH0009','IN0009','8, Jalan Selesaria 3, Happy Garden, 58200 Kuala Lumpur','matthew','0165509209','pending','2024-08-26 06:18:48'),('SH0010','IN0010','213, Jln Tun Razak, Kuala Lumpur, 50450 Kuala Lumpur','shyn wei','0126675418','pending','2024-08-26 06:21:07');
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
  `status` tinyint(1) NOT NULL,
  PRIMARY KEY (`stf_id`),
  UNIQUE KEY `stf_id` (`stf_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff`
--

LOCK TABLES `staff` WRITE;
/*!40000 ALTER TABLE `staff` DISABLE KEYS */;
INSERT INTO `staff` VALUES ('SF0001','wenkang@111','wen kang','braynchongwenkang590@gmail.com','0125778910','2004-12-09','Jalan Stesen Sentral 5, Kuala Lumpur Sentral, 50470 Kuala Lumpur','0198886103','Admin',1),('SF0002','password123@','Alice Tan','alice.tan@example.com','0123456789','1985-07-12','21, Jalan Damansara, 50490 Kuala Lumpur','0198765432','Admin',1),('SF0003','securePass!','Brian Lee','brian.lee@example.com','0198765432','1980-05-18','12, Jalan Bangsar, 59200 Kuala Lumpur','0187654321','Admin',1),('SF0004','admin888!','Cheryl Lim','cheryl.lim@example.com','0171234567','1992-02-20','9, Jalan Ampang, 50450 Kuala Lumpur','0138765432','Admin',1),('SF0005','mypass789!','David Ong','david.ong@example.com','0165432109','1988-11-25','7, Jalan Pudu, 55100 Kuala Lumpur','0147654321','Admin',1),('SF0006','secret007!','Emily Wong','emily.wong@example.com','0143322110','1990-04-15','6, Jalan Tun Razak, 50400 Kuala Lumpur','0123456780','Admin',1),('SF0007','passme456@','Frankie Yeo','frankie.yeo@example.com','0192233445','1983-09-05','5, Jalan Imbi, 55100 Kuala Lumpur','0178765432','Admin',1),('SF0008','adminPass22!','Grace Teoh','grace.teoh@example.com','0181122334','1987-08-30','4, Jalan Raja Laut, 50350 Kuala Lumpur','0158765432','Admin',1),('SF0009','secureMe12!','Henry Goh','henry.goh@example.com','0122233445','1991-06-22','3, Jalan Sultan Ismail, 50250 Kuala Lumpur','0197654321','Admin',0),('SF0010','manager@2023','Ivy Chan','ivy.chan@example.com','0129988776','1982-01-14','8, Jalan Bukit Bintang, 55100 Kuala Lumpur','0139988776','Manager',1),('SF0011','manager@2024','Jack Lim','jack.lim@example.com','0176655443','1979-12-03','10, Jalan Tun Sambanthan, 50470 Kuala Lumpur','0123344556','Manager',1);
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
  `email` varchar(50) DEFAULT NULL,
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
INSERT INTO `user` VALUES ('jh_33','Johern@333','jo hern','johern@gmail.com','0163314206','2004-04-26','No. 18 1St Floor Jln Ss5A/9 Ss5, Petaling Jaya, Selangor, 47301','student',NULL),('kaiy','Kaiyong337@','vandy','vandyck@gmail.com','0198876123','2002-06-17','76 Jalan Raja Muda Abdul Aziz, Jln Tun Razak, 50300 Kuala Lumpur','software engineer',NULL),('kh_888','Kaihong@888','kai hong','kaihong@gmail.com','0162574578','2004-08-09','Jalan Berhala, Brickfields, 50470 Kuala Lumpur','student',NULL),('sw_0418','Shynwei@0418','shyn wei','sw0418@gmail.com','0126675418','2004-04-18','213, Jln Tun Razak, Kuala Lumpur, 50450 Kuala Lumpur','student',NULL),('timi','Timi@222','timi wee','timiweeyuetim@gmail.com','0102705103','2004-09-22','1 26 Jln Manis 1 Taman Segar, KL, 56100','student',NULL),('wk','Wenkang@111','wen kang','braynchongwenkang590@gmail.com','0166893432','2004-11-12','11 JLN SUNGEI PULUH 5 TAMAN UTAMA, Klang, 41400','student',NULL),('yh_22','Yunghao@22','yung hao','yyhao0422@gmail.com','0167331846','2004-04-22','5, Lorong Peel, Maluri, 55100 Cheras','cloud engineer',NULL),('ying_04','Ying@xin04','ying xin','yingxin@gmail.com','0122664228','2004-11-03','Jalan Besi Kawi, Taman Sungai Besi, 57100 Kuala Lumpur','student',NULL),('yumi','0612Yumi!','yumi','yumi0612@gmail.com','0138385108','2001-06-12','Residensi ViiA, Jalan Bangsar, KL Eco City, 59200 Kuala Lumpur','student',NULL),('zx','Zhixian999!','zhi xian','zhixian@gmail.com','0165509209','2004-12-05','8, Jalan Selesaria 3, Happy Garden, 58200 Kuala Lumpur','student',NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_tracking`
--

DROP TABLE IF EXISTS `user_tracking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_tracking` (
  `id` int NOT NULL,
  `previous_total_user` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_tracking`
--

LOCK TABLES `user_tracking` WRITE;
/*!40000 ALTER TABLE `user_tracking` DISABLE KEYS */;
INSERT INTO `user_tracking` VALUES (1,10);
/*!40000 ALTER TABLE `user_tracking` ENABLE KEYS */;
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

-- Dump completed on 2024-08-26 22:31:47
