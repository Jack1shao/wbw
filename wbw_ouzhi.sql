/*
Navicat MySQL Data Transfer

Source Server         : 127.0.0.1
Source Server Version : 50714
Source Host           : localhost:3306
Source Database       : mysql

Target Server Type    : MYSQL
Target Server Version : 50714
File Encoding         : 65001

Date: 2018-09-17 16:46:40
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for 欧赔明细原始
-- ----------------------------
DROP TABLE IF EXISTS `ouzhi`;
CREATE TABLE `ouzhi` (
  `idnm` int(11) NOT NULL,
  `xh` int(11) NOT NULL,
  `bcgs` varchar(255) NOT NULL,

  `cz3` decimal(5,2) NOT NULL,
  `cz1` decimal(5,2) NOT NULL,
  `cz0` decimal(5,2) NOT NULL,
  
  `jz3` decimal(5,2) NOT NULL,
  `jz1` decimal(5,2) NOT NULL,
  `jz0` decimal(5,2) NOT NULL,
  
  `cgl3` decimal(5,2) DEFAULT NULL,
  `cgl1` decimal(5,2) DEFAULT NULL,
  `cgl0` decimal(5,2) DEFAULT NULL,
  
  `jgl3` decimal(5,2) DEFAULT NULL,
  `jgl1` decimal(5,2) DEFAULT NULL,
  `jgl0` decimal(5,2) DEFAULT NULL,
  `chf` decimal(5,2) DEFAULT NULL,
  `jhf` decimal(5,2) DEFAULT NULL,
  
  `ck3` decimal(5,2) DEFAULT NULL,
  `ck1` decimal(5,2) DEFAULT NULL,
  `ck0` decimal(5,2) DEFAULT NULL,
  
  `jk3` decimal(5,2) DEFAULT NULL,
  `jk1` decimal(5,2) DEFAULT NULL,
  `jk0` decimal(5,2) DEFAULT NULL

) ENGINE=InnoDB DEFAULT CHARSET=utf8;
