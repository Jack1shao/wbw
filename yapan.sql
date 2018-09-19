/*
Navicat MySQL Data Transfer

Source Server         : ss
Source Server Version : 50715
Source Host           : localhost:3306
Source Database       : mysql

Target Server Type    : MYSQL
Target Server Version : 50715
File Encoding         : 65001

Date: 2018-09-18 22:52:43
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for 澳盘明细原始
-- ----------------------------
DROP TABLE IF EXISTS `yapan`;
CREATE TABLE `yapan` (
  `idnm` int(11) NOT NULL,
  `xh` int(11) NOT NULL,
  `ypgs` varchar(255) DEFAULT NULL,
  `jzs` decimal(6,4) DEFAULT NULL,
  `jp` varchar(255) DEFAULT NULL,
  `jks` decimal(6,4) DEFAULT NULL,
  `czs` decimal(6,4) DEFAULT NULL,
  `cp` varchar(255) DEFAULT NULL,
  `cks` decimal(6,4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
