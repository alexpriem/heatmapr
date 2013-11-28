--leeftijd

DROP TABLE if exists selectie;

select  {% if logx %}		
        	round(datediff(day,{{xcol}},'20120101')/365.0*{{xfactorinv}},0)/{{xfactorinv}} as {{xcol}}, 
        {% else %}
         	round( sign(datediff(day,{{xcol}},'20120101') )*log(datediff(day,{{xcol}},'20120101')/365.0)*{{xfactorinv}},0)/{{xfactorinv}} as {{xcol}}, 
        {% endif %}
		
        {% if logy %}		
        	round((sign({{ycol}})* log({{ycol}})/ {{yfactor}})::numeric,0)* {{yfactor}} as {{ycol}}
        {% else %}
         	round({{ycol}}/{{yfactor}},0)* {{yfactor}} as {{ycol}}
        {% endif %}
         {% if selcol %}
         , {{selcol}} 
           {% endif %}    
into selectie
from {{tabel}} 
where {{ycol}}!=0;