-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.4.11-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             10.3.0.5771
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for gotolong
CREATE DATABASE IF NOT EXISTS `gotolong` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `gotolong`;

-- Dumping structure for table gotolong.auth_group
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table gotolong.auth_group_permissions
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table gotolong.auth_permission
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table gotolong.auth_user
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table gotolong.auth_user_groups
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table gotolong.auth_user_user_permissions
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table gotolong.django_admin_log
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table gotolong.django_content_type
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table gotolong.django_migrations
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table gotolong.django_session
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table gotolong.global_amfi
CREATE TABLE IF NOT EXISTS `global_amfi` (
  `comp_rank` int(11) DEFAULT NULL,
  `comp_name` text DEFAULT NULL,
  `comp_isin` text DEFAULT NULL,
  `bse_symbol` text DEFAULT NULL,
  `nse_symbol` text DEFAULT NULL,
  `avg_mcap` text DEFAULT NULL,
  `cap_type` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table gotolong.global_isin
CREATE TABLE IF NOT EXISTS `global_isin` (
  `comp_name` text DEFAULT NULL,
  `comp_industry` text DEFAULT NULL,
  `comp_ticker` text DEFAULT NULL,
  `series` text DEFAULT NULL,
  `comp_isin` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table gotolong.global_nach
CREATE TABLE IF NOT EXISTS `global_nach` (
  `name` text DEFAULT NULL,
  `ticker` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table gotolong.global_weight
CREATE TABLE IF NOT EXISTS `global_weight` (
  `cap_type` text DEFAULT NULL,
  `cap_weight` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table gotolong.plan
CREATE TABLE IF NOT EXISTS `plan` (
  `comp_industry` text DEFAULT NULL,
  `comp_name` text DEFAULT NULL,
  `comp_ticker` text DEFAULT NULL,
  `comp_selected` text DEFAULT NULL,
  `comp_desc` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table gotolong.screener
CREATE TABLE IF NOT EXISTS `screener` (
  `name` text DEFAULT NULL,
  `bse_code` text DEFAULT NULL,
  `nse_code` text DEFAULT NULL,
  `industry` text DEFAULT NULL,
  `cmp` text DEFAULT NULL,
  `filter` text DEFAULT NULL,
  `filter_52w_low` text DEFAULT NULL,
  `up_52w_low` text DEFAULT NULL,
  `low_52w` text DEFAULT NULL,
  `high_52w` text DEFAULT NULL,
  `sales` text DEFAULT NULL,
  `np` text DEFAULT NULL,
  `mcap` text DEFAULT NULL,
  `d2e` text DEFAULT NULL,
  `roe3` text DEFAULT NULL,
  `roce3` text DEFAULT NULL,
  `dp3` text DEFAULT NULL,
  `pe` text DEFAULT NULL,
  `pe5` text DEFAULT NULL,
  `peg` text DEFAULT NULL,
  `opm` text DEFAULT NULL,
  `icr` text DEFAULT NULL,
  `ev` text DEFAULT NULL,
  `nw` text DEFAULT NULL,
  `reserves` text DEFAULT NULL,
  `roa3` text DEFAULT NULL,
  `p2bv` text DEFAULT NULL,
  `p2ocf` text DEFAULT NULL,
  `p2sales` text DEFAULT NULL,
  `ev2ebitda` text DEFAULT NULL,
  `dp` text DEFAULT NULL,
  `dy` text DEFAULT NULL,
  `cr` text DEFAULT NULL,
  `sales5` text DEFAULT NULL,
  `profit5` text DEFAULT NULL,
  `pledge` text DEFAULT NULL,
  `prom_hold` text DEFAULT NULL,
  `piotski` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table gotolong.trendlyne
CREATE TABLE IF NOT EXISTS `trendlyne` (
  `comp_name` text DEFAULT NULL,
  `comp_isin` text DEFAULT NULL,
  `comp_bat` text DEFAULT NULL,
  `comp_bar` text DEFAULT NULL,
  `comp_der` text DEFAULT NULL,
  `comp_roce3` text DEFAULT NULL,
  `comp_dpr2` text DEFAULT NULL,
  `comp_pledge` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table gotolong.user_demat_sum
CREATE TABLE IF NOT EXISTS `user_demat_sum` (
  `stock_symbol` text DEFAULT NULL,
  `comp_name` text DEFAULT NULL,
  `isin_code_id` text DEFAULT NULL,
  `qty` text DEFAULT NULL,
  `acp` text DEFAULT NULL,
  `cmp` text DEFAULT NULL,
  `pct_change` text DEFAULT NULL,
  `value_cost` text DEFAULT NULL,
  `value_market` text DEFAULT NULL,
  `days_gain` text DEFAULT NULL,
  `days_gain_pct` text DEFAULT NULL,
  `realized_pl` text DEFAULT NULL,
  `unrealized_pl` text DEFAULT NULL,
  `unrealized_pl_pct` text DEFAULT NULL,
  `unused1` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table gotolong.user_demat_txn
CREATE TABLE IF NOT EXISTS `user_demat_txn` (
  `stock_symbol` text DEFAULT NULL,
  `comp_name` text DEFAULT NULL,
  `isin_code` text DEFAULT NULL,
  `action` text DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `txn_price` float DEFAULT NULL,
  `brokerage` text DEFAULT NULL,
  `txn_charges` text DEFAULT NULL,
  `stamp_duty` text DEFAULT NULL,
  `segment` text DEFAULT NULL,
  `stt` text DEFAULT NULL,
  `remarks` text DEFAULT NULL,
  `txn_date` date DEFAULT NULL,
  `exchange` text DEFAULT NULL,
  `unused1` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table gotolong.user_dividend
CREATE TABLE IF NOT EXISTS `user_dividend` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `div_date` date DEFAULT NULL,
  `remarks` text DEFAULT NULL,
  `amount` text DEFAULT NULL,
  `ticker` text DEFAULT NULL,
  `isin` text DEFAULT NULL,
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10616 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table gotolong.user_weight
CREATE TABLE IF NOT EXISTS `user_weight` (
  `comp_ticker` text DEFAULT NULL,
  `comp_weight_type` text DEFAULT NULL,
  `comp_weight_units` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
