#

--足球数据清理

--查看记录条数
SELECT count(*) from scb a where  a.nd=18 and a.ls='意甲'


--
SELECT B.idnm,B.`主进球`-B.`客进球`,B.`赛果`,Y.`必发交易量比例`,Y.`必发市场指数`,C.*
FROM `必发原始` Y,`赛程表原始` B,(SELECT A.idnm,MAX(A.`必发市场指数`),MIN(A.`必发市场指数`) FROM `必发原始` A GROUP BY A.idnm) C

WHERE Y.idnm=B.idnm AND Y.idnm=C.idnm

--必发市场指数最小打出情况
SELECT B.idnm,Y.`序号`,B.`主进球`-B.`客进球`,B.`赛果`,Y.`必发交易量比例`,Y.`必发市场指数`,C.*,
		case when y.序号=2 AND B.`赛果`=1 then 1
					when y.`序号`-3=B.`赛果` then 0
					when y.`序号`+2=B.`赛果` then 3
		else ''
		end t 

FROM `必发原始` Y,`赛程表原始` B,(SELECT A.idnm,MAX(A.`必发市场指数`) D,MIN(A.`必发市场指数`) X FROM `必发原始` A GROUP BY A.idnm) C
WHERE Y.idnm=B.idnm AND Y.idnm=C.idnm
	AND C.X=Y.`必发市场指数`

##--
DROP VIEW  if  EXISTS vv;
CREATE VIEW vv AS
SELECT B.idnm,Y.`序号`,B.`主进球`,B.`客进球`,B.`主进球`-B.`客进球` qc,B.`赛果`,Y.`买家挂牌价位`,Y.`必发交易量比例`,Y.`必发市场指数`,Y.`必发盈亏指数`
FROM `必发原始` Y,`赛程表原始` B,`澳盘明细原始` M
WHERE Y.idnm=B.idnm  AND M.idnm=B.idnm AND M.`序号`=0;

--必发打出情况
select *,case when vv.`必发市场指数`=c.D then 'max'
							when vv.`必发市场指数`=c.X then  'min'
							ELSE 'M'
				END zsqk
	,		case when vv.`序号`=2 AND vv.`赛果`=1 then 1
					when vv.`序号`=1 and vv.`赛果`=3 then 3
					when vv.`序号`=3 and vv.`赛果`=0 then 0
		else -11
		end dcqk 
from vv LEFT JOIN 
(SELECT A.idnm,MAX(A.`必发市场指数`) D,MIN(A.`必发市场指数`) X FROM `必发原始` A GROUP BY A.idnm) c
ON c.idnm=vv.idnm


select *,case when vv.`必发市场指数`=c.D then 'max'
							when vv.`必发市场指数`=c.X then  'min'
							ELSE 'M'
				END zsqk
	,		case when vv.`序号`=2 AND vv.`赛果`=1 then 1
					when vv.`序号`=1 and vv.`赛果`=3 then 3
					when vv.`序号`=3 and vv.`赛果`=0 then 0
		else -11
		end dcqk 
from vv LEFT JOIN 
(SELECT A.idnm,MAX(A.`必发市场指数`) D,MIN(A.`必发市场指数`) X,SUM(A.成交量) cjl FROM `必发原始` A GROUP BY A.idnm) c
ON c.idnm=vv.idnm
WHERE vv.盘='半球'


#清理数据库
DELETE y.* FROM ouzhi y where y.idnm in (select idnm from scb a where not EXISTS (select 1 from yapan b where a.idnm=b.idnm))

delete a.*
from scb a 
where not EXISTS (select 1 from yapan b where a.idnm=b.idnm) 
				and not EXISTS (select 1 from ouzhi b where a.idnm=b.idnm)