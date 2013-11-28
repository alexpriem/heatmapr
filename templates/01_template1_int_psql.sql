DROP TABLE if exists selectie;
 
select  {% if logx %}
			round((sign{{xcol}}*log({{xcol}})/ {{xfactor}}):numeric,0)* {{xfactor}} as {{xcol}}, 			
		{% else %}
			round({{xcol}}/{{xfactor}},0)* {{xfactor}} as {{xcol}},
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
where {{xcol}}!=0 and {{ycol}}!=0;