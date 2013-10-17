{% if selcol %} 
create clustered index i1 on  contourtab( {{selcol}}, {{xcol}}, {{ycol}})    
{% else %}
create clustered index i1 on  contourtab( {{xcol}}, {{ycol}})    
{% endif %}