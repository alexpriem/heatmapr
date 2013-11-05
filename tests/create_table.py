import os,sys,yaml
from jinja2 import Environment
from localyaml import OrderedDictYAMLLoader
from heatmapr.db import dbconnection


if len(sys.argv)!=2:
    print 'usage: python %s <filename>' % (argv[0])
    print 'imports csv file into db'
    print 'from meta in filename'
    sys.exit()


fname=sys.argv[1]

f=open(fname)
desc=f.read()
f.close()

meta=yaml.load('{'+desc+'}', OrderedDictYAMLLoader)
metadict={}
for k,v in meta.items():
    metadict[k]=v


s="""
drop table if exists {{table}};
create table {{table}}(
    {{xcol}} {{xtype}},
    {{ycol}} {{ytype}}
    {% if selcol %}
    , {{selcol}} {{seltype}}
    {% endif %}
    );
""" 
  

sql=Environment().from_string(s).render(metadict)


d=dbconnection(meta)
d.run_sql (sql)
