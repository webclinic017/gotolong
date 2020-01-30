-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.4.11-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             10.2.0.5599
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for gotolong
DROP DATABASE IF EXISTS `gotolong`;
CREATE DATABASE IF NOT EXISTS `gotolong` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `gotolong`;

-- Dumping structure for table gotolong.amfi
DROP TABLE IF EXISTS `amfi`;
CREATE TABLE IF NOT EXISTS `amfi` (
  `sno` text DEFAULT NULL,
  `company_name` text DEFAULT NULL,
  `isin` text DEFAULT NULL,
  `bse_symbol` text DEFAULT NULL,
  `nse_symbol` text DEFAULT NULL,
  `avg_mcap` text DEFAULT NULL,
  `cap_type` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table gotolong.demat_summary
DROP TABLE IF EXISTS `demat_summary`;
CREATE TABLE IF NOT EXISTS `demat_summary` (
  `stock_symbol` text DEFAULT NULL,
  `company_name` text DEFAULT NULL,
  `isin_code` text DEFAULT NULL,
  `qty` text DEFAULT NULL,
  `acp` text DEFAULT NULL,
  `cmp` text DEFAULT NULL,
  `pct_change` text DEFAULT NULL,
  `value_cost` text DEFAULT NULL,
  `value_market` text DEFAULT NULL,
  `realized_pl` text DEFAULT NULL,
  `unrealized_pl` text DEFAULT NULL,
  `unrealized_pl_pct` text DEFAULT NULL,
  `unused1` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table gotolong.demat_txn
DROP TABLE IF EXISTS `demat_txn`;
CREATE TABLE IF NOT EXISTS `demat_txn` (
  `stock_symbol` text DEFAULT NULL,
  `company_name` text DEFAULT NULL,
  `isin_code` text DEFAULT NULL,
  `action` text DEFAULT NULL,
  `quantity` text DEFAULT NULL,
  `txn_price` text DEFAULT NULL,
  `brokerage` text DEFAULT NULL,
  `txn_charges` text DEFAULT NULL,
  `stamp_duty` text DEFAULT NULL,
  `segment` text DEFAULT NULL,
  `stt` text DEFAULT NULL,
  `remarks` text DEFAULT NULL,
  `txn_date` text DEFAULT NULL,
  `exchange` text DEFAULT NULL,
  `unused1` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table gotolong.isin
DROP TABLE IF EXISTS `isin`;
CREATE TABLE IF NOT EXISTS `isin` (
  `company_name` text DEFAULT NULL,
  `industry_name` text DEFAULT NULL,
  `symbol_ticker` text DEFAULT NULL,
  `series` text DEFAULT NULL,
  `isin_code` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table gotolong.plan
DROP TABLE IF EXISTS `plan`;
CREATE TABLE IF NOT EXISTS `plan` (
  `comp_industry` text DEFAULT NULL,
  `comp_name` text DEFAULT NULL,
  `comp_ticker` text DEFAULT NULL,
  `comp_selected` text DEFAULT NULL,
  `comp_desc` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table gotolong.screener
DROP TABLE IF EXISTS `screener`;
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
  `ic` text DEFAULT NULL,
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
DROP TABLE IF EXISTS `trendlyne`;
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

-- Dumping structure for table gotolong.weight
DROP TABLE IF EXISTS `weight`;
CREATE TABLE IF NOT EXISTS `weight` (
  `comp_ticker` text DEFAULT NULL,
  `comp_weight_type` text DEFAULT NULL,
  `comp_weight_units` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
