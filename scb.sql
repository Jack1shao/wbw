/*
Navicat MySQL Data Transfer

Source Server         : ss
Source Server Version : 50715
Source Host           : localhost:3306
Source Database       : mysql

Target Server Type    : MYSQL
Target Server Version : 50715
File Encoding         : 65001

Date: 2018-09-19 00:11:02
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for 赛程表原始
-- ----------------------------
DROP TABLE IF EXISTS `scb`;
CREATE TABLE `scb` (
  `idnm` int(11) NOT NULL,
  `zd` varchar(255) NOT NULL,
  `kd` varchar(255) NOT NULL,
  `nd` varchar(255) DEFAULT NULL,
  `ls` varchar(255) DEFAULT NULL,
  `lc` int(11) DEFAULT NULL,
  `zjq` int(11) DEFAULT NULL,
  `kjq` int(11) DEFAULT NULL,
  `bstime` varchar(255) DEFAULT NULL
  PRIMARY KEY (`idnm`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
