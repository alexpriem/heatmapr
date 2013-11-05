 IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'selectie2') AND type in (N'U'))
DROP TABLE selectie2

select {{xcol}},
       {{ycol}},
       {% if selcol %}
       {{selcol}},
       {% endif %}
       num=count(*)
into selectie2
from selectie
group by {{xcol}}, {{ycol}}
        {% if selcol %}
        , rollup({{selcol}})
        {% endif %}