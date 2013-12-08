--# STN,YYYYMMDD,   TG,   PG,   NG,   UG


drop table if exists knmi_1995;
create table knmi_1995 (
 station int,
 datum int,
 tg smallint,
 pg smallint,
 ng smallint,
 ug smallint);

 copy knmi_1995 from 'f:\data\heatseries\data\knmi_1995_2013.csv' csv header delimiter ',' NULL AS '     ';
 select  * from knmi_1995 limit 100;

drop table if exists knmi_1995b;
 select station,datum,to_timestamp(datum::text,'YYYYMMDD') as datum2, tg,pg,ng,ug 
	into knmi_1995b
	from knmi_1995;

drop table if exists knmi_1995c;
select station, 
	datum, 
	datum2, 
	EXTRACT(day FROM datum2 - '19940101' )::int as dag1994,
	tg,
	pg,
	ng,
	ug
	into knmi_1995c
	 from knmi_1995b;
	
select max(dag1994), min(tg),max(tg), min(pg), max(pg) from knmi_1995c limit 100;


--select * from numbers  where number<0 limit 10;
--insert into numbers select -number from numbers where number!=0;
