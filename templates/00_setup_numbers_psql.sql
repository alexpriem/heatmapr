DROP TABLE if exists numbers;

create table numbers (number int);
copy numbers from 'f:\cbs\heatmapr\numbers.csv' DELIMITERS ',' csv;