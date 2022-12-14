-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.4.24-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for servers
CREATE DATABASE IF NOT EXISTS `servers` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `servers`;

-- Dumping structure for table servers.server_info
CREATE TABLE IF NOT EXISTS `server_info` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `IP` varchar(50) NOT NULL DEFAULT '',
  `Port` int(11) NOT NULL,
  `Query_Port` int(11) NOT NULL,
  `Game` text NOT NULL,
  `Server Name` text NOT NULL,
  `channelID` bigint(20) NOT NULL DEFAULT 0,
  `messageID` bigint(20) NOT NULL DEFAULT 0,
  `server_location` varchar(50) NOT NULL DEFAULT ':flag_us: US',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;

-- Dumping data for table servers.server_info: ~9 rows (approximately)
REPLACE INTO `server_info` (`ID`, `IP`, `Port`, `Query_Port`, `Game`, `Server Name`, `channelID`, `messageID`, `server_location`) VALUES
	(0, '45.35.73.111', 27030, 27030, '7 Days to Die', '7 Days to Die', 0, 0, ':flag_us: US'),
	(1, '45.35.98.59', 28500, 28515, 'DayZ', 'DayZ', 0, 0, ':flag_us: US'),
	(2, '51.161.52.174', 7781, 27020, 'DeadPoly', 'DeadPoly', 0, 0, ':flag_us: US'),
	(3, '104.129.132.73', 25642, 25642, 'Minecraft', 'Minecraft', 0, 0, ':flag_us: US'),
	(4, '208.52.153.61', 27032, 27032, 'Unturned', 'Unturned | Elver | PvE', 0, 0, ':flag_us: US'),
	(5, '147.135.105.231', 27036, 27036, 'Unturned', 'Unturned | Arid | PvE', 0, 0, ':flag_us: US'),
	(6, '208.52.153.61', 27037, 27037, 'Unturned', 'Unturned | Inone | PvE', 0, 0, ':flag_us: US'),
	(7, '104.129.132.73', 27042, 27042, 'Unturned', 'Unturned | Inone | PvP', 0, 0, ':flag_us: US'),
	(8, '173.237.17.100', 28000, 28400, 'Rust', 'Rust', 0, 0, ':flag_us: US');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
