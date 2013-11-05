{% if selcol %} 
create  index contourtab_i1 on  contourtab( {{selcol}}, {{xcol}}, {{ycol}})    
{% else %}
create  index contourtab_i1 on  contourtab( {{xcol}}, {{ycol}})    
{% endif %}