DROP TABLE if exists contourtab;

select  a.{{xcol}},
        a.{{ycol}},
        {% if selcol %}
        b.{{selcol}},
        {% endif %}
        coalesce(b.num,0) as num
        into contourtab
        from xy a
        left join selectie2  b
        on a.{{xcol}}=b.{{xcol}} and a.{{ycol}}=b.{{ycol}}
        {% if selcol %}
        and a.{{selcol}}=b.{{selcol}}
        {% endif %};
