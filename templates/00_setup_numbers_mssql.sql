-- geen sql uitvoeren omdat sql server geen csv kan importeren vanaf command prompt
--IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'numbers') AND type in (N'U'))
--DROP TABLE numbers

--create table numbers (number int)
--BULK INSERT numbers fROM  'f:\cbs\heatmapr\numbers.csv' ( 
--	FIELDTERMINATOR = ',',  --CSV field delimiter
--    ROWTERMINATOR = '\n',   --Use to shift the control to next row
--    TABLOCK
-- )
