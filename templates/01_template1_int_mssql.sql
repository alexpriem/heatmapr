IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'selectie') AND type in (N'U'))
DROP TABLE selectie


select  {{xcol}}=round({{xcol}}/ {{xfactor}},0)* {{xfactor}}, 
        {{ycol}}=round({{ycol}}/ {{yfactor}},0)* {{yfactor}}
        {% if selcol %}
        , {{selcol}} 
        {% endif %}
into selectie
from {{tabel}}