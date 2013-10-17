DROP TABLE if exists yas;

select distinct {{ycol}}=number* {{yfactor}}
                into yas
from numbers
where number>({{ymin}}  / {{yfactor}}) and number<=({{ymax}} / {{yfactor}});