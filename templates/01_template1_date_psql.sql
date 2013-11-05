--leeftijd

DROP TABLE if exists selectie;

select  round(datediff(day,{{xcol}},'20120101')/365.0*{{xfactorinv}},0)/{{xfactorinv}} as {{xcol}}, 
         round({{ycol}}/{{yfactor}},0)* {{yfactor}} as {{ycol}}
         {% if selcol %}
         , {{selcol}} 
           {% endif %}    
into selectie
from {{tabel}};