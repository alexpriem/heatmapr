DROP TABLE if exists selectie;

select  {{xcol}}=round({{xcol}}/ {{xfactor}},0)* {{xfactor}}, 
        {{ycol}}=round({{ycol}}/ {{yfactor}},0)* {{yfactor}}
        {% if selcol %}
        , {{selcol}} 
        {% endif %}
into selectie
from {{tabel}};