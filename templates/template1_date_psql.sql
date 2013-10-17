--leeftijd

DROP TABLE if exists selectie;

select  {{xcol}}=round(datediff(day,{{xcol}},'20120101')/365.0*{{xfactorinv}},0)/{{xfactorinv}}, 
         {{ycol}}=round({{ycol}}/{{yfactor}},0)* {{yfactor}}
         {% if selcol %}
         , {{selcol}} 
           {% endif %}    
into selectie
from {{tabel}};