IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'contourtab') AND type in (N'U'))
DROP TABLE contourtab

  select  a.{{xcol}},
        a.{{ycol}},
        {% if selcol %}
        b.{{selcol}},
        {% endif %}
        num=isnull(b.num,0)
        into contourtab
        from xy a
        left join selectie2  b
        on convert(bigint, 1000*a.{{xcol}})=convert(bigint, 1000*b.{{xcol}}) and 
            convert(bigint,1000*a.{{ycol}})=convert(bigint,1000*b.{{ycol}})        --- rounding errrors prevent joining. converting floats to ints seems to fix it.
        {% if selcol %}
        and a.{{selcol}}=b.{{selcol}}
        {% endif %}
