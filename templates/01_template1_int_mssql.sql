IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'selectie') AND type in (N'U'))
DROP TABLE selectie


select  {% if logx %}
            {{xcol}}=round(
                    case when {{xcol}}>0 then log10({{xcol}})
                         when {{xcol}}=0 then 0
                         when {{xcol}}<0 then -log10(-{{xcol}})
                    end
                / {{xfactor}},0)
                * {{xfactor}}            
        {% else %}
            {{xcol}}=round({{xcol}}/ {{xfactor}},0)* {{xfactor}}, 
        {% endif %}
        {% if logy %}
            {{ycol}}=round(
                    case when {{ycol}}>0 then log10({{ycol}})
                         when {{ycol}}=0 then 0
                         when {{ycol}}<0 then -log10(-{{ycol}})
                    end
                / {{yfactor}},0)
                * {{yfactor}}
        {% else %}
            {{ycol}}=round({{ycol}} / {{yfactor}},0) * {{yfactor}}
        {% endif %}
        {% if selcol %}
        , {{selcol}} 
        {% endif %}
into selectie
from {{tabel}}