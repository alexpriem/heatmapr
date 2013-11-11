 IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'xas') AND type in (N'U'))
DROP TABLE yas

select distinct {{ycol}}=number* {{yfactor}}
                into yas
from numbers
where number>=({{ymin}}  / {{yfactor}}) and number<({{ymax}} / {{yfactor}})