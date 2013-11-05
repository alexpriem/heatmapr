--leeftijd

IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'selectie') AND type in (N'U'))
DROP TABLE selectie

select  {{xcol}}=round(datediff(day,{{xcol}},'20120101')/365.0*{{xfactorinv}},0)/{{xfactorinv}}, 
         {{ycol}}=round({{ycol}}/{{yfactor}},0)* {{yfactor}}
         {% if selcol %}
         , {{selcol}} 
           {% endif %}    
into selectie
from {{tabel}}