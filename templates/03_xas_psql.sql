DROP TABLE if exists xas;

select distinct number * {{xfactor}} as {{xcol}}
              into xas
	from numbers
	where number>({{xmin}} / {{xfactor}}) and number<=({{xmax}} / {{xfactor}});