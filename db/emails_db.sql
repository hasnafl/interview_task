-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.3.29-MariaDB-1:10.3.29+maria~xenial-log - mariadb.org binary distribution
-- Server OS:                    debian-linux-gnu
-- HeidiSQL Version:             11.0.0.5919
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for emails_db
CREATE DATABASE IF NOT EXISTS `emails_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
USE `emails_db`;

-- Dumping structure for table emails_db.emails
CREATE TABLE IF NOT EXISTS `emails` (
  `event_id` int(11) DEFAULT NULL,
  `email_subject` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email_content` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table emails_db.emails: ~0 rows (approximately)
/*!40000 ALTER TABLE `emails` DISABLE KEYS */;
INSERT INTO `emails` (`event_id`, `email_subject`, `email_content`, `timestamp`) VALUES
	(1, 'Email Subject 1', 'This is Email Content 1', '2022-05-07 01:07:00'),
	(2, 'Email Subject 2', 'This is Email Content 2', '2022-05-07 01:07:00'),
	(3, 'Email Subject 3', 'Email Content 3', '2022-05-07 12:22:00');
/*!40000 ALTER TABLE `emails` ENABLE KEYS */;

-- Dumping structure for table emails_db.email_recipients
CREATE TABLE IF NOT EXISTS `email_recipients` (
  `id` int(11) DEFAULT NULL,
  `email_address` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table emails_db.email_recipients: ~0 rows (approximately)
/*!40000 ALTER TABLE `email_recipients` DISABLE KEYS */;
INSERT INTO `email_recipients` (`id`, `email_address`) VALUES
	(1, 'hasnafairuzl98@gmail.com');
/*!40000 ALTER TABLE `email_recipients` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
