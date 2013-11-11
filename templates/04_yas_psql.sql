DROP TABLE if exists yas;

select distinct number* {{yfactor}} as {{ycol}}
                into yas
from numbers
where number>=({{ymin}}  / {{yfactor}}) and number<({{ymax}} / {{yfactor}});