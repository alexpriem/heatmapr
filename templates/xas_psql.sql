DROP TABLE if exists xas;

select distinct {{xcol}}=number * {{xfactor}}
              into xas
	from numbers
	where number>({{xmin}} / {{xfactor}}) and number<=({{xmax}} / {{xfactor}});