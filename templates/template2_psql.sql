 DROP TABLE if exists selectie2;

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
        {% endif %};