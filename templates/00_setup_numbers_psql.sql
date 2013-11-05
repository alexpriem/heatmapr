DROP TABLE if exists numbers;

create table numbers (number int);
copy numbers from 'E:\src\heatmapr\numbers.csv' DELIMITERS ',' csv;