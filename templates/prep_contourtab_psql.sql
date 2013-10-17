DROP TABLE if exists contourtab;

select  a.{{xcol}},
        a.{{ycol}},
        {% if selcol %}
        b.{{selcol}},
        {% endif %}
        num=isnull(b.num,0)
        into contourtab
        from xy a
        left join selectie2  b
        on a.{{xcol}}=b.{{xcol}} and a.{{ycol}}=b.{{ycol}}
        {% if selcol %}
        and a.{{selcol}}=b.{{selcol}}
        {% endif %};
