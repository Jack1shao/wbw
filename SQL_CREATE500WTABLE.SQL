#CREATE TABLE

SET FOREIGN_KEY_CHECKS=0;
-- ----------------------------
-- Table structure for 赛程表原始
-- ----------------------------
#DROP TABLE IF EXISTS `scb`;
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


-- ----------------------------
-- Table structure for 必发热度分析
-- ----------------------------
#DROP TABLE IF EXISTS `bifa`;
CREATE TABLE `bifa` (
  `idnm` int(11) NOT NULL,
  `xh` int(11) NOT NULL,
  `xm` varchar(255) NOT NULL,

  `pl` decimal(5,2) NOT NULL,#
  `gl` decimal(5,2) NOT NULL,#概率
  `bd` decimal(5,2) NOT NULL,#
  
  `bf` decimal(5,2) NOT NULL,#
  `cjj` decimal(5,2) NOT NULL,#成交价
  `cjl` int(11) NOT NULL,#成交量
  
  `zjyk` int(11) DEFAULT NULL,#庄家盈亏
  `bfzs` decimal(5,2) DEFAULT NULL,
  `lrzs` decimal(5,2) DEFAULT NULL,
  
  `ykzs` decimal(5,2) DEFAULT NULL
  
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- ----------------------------
-- Table structure for 必发数据提点
-- ----------------------------
#DROP TABLE IF EXISTS `sjtdbf`;
CREATE TABLE `sjtdbf` (
  `idnm` int(11) NOT NULL,
  `sjtd` varchar(255) DEFAULT NULL,
  `s1` varchar(255) DEFAULT NULL,
  `s2` varchar(255) DEFAULT NULL,
  `s3` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


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

-- ----------------------------
-- Table structure for 亚盘明细原始
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