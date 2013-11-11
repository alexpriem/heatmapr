select {{xcol}}, 
		{{ycol}}, 
        {% if selcol %}
        {{selcol}},
        {% endif %}
        num
	from contourtab
    order by 1, 2