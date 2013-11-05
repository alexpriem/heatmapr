DROP TABLE if exists selectie;

select  round({{xcol}}/ {{xfactor}},0)* {{xfactor}} as {{xcol}}, 
        round({{ycol}}/ {{yfactor}},0)* {{yfactor}} as {{ycol}}
        {% if selcol %}
        , {{selcol}} 
        {% endif %}
into selectie
from {{tabel}};