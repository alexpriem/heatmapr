import os,sys,yaml
from jinja2 import Environment
from localyaml import OrderedDictYAMLLoader
from heatmapr.db import dbconnection


if len(sys.argv)!=2:
    print 'usage: python in.py <filename>'
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




def print_type (val, type_val):

    if type_val=='int':
        return str(int(val))
    if type_val=='decimal':
        return '%.4f' % val
    return str(val)



csv=meta['csv']
delimiter=meta['delimiter']


f=open(csv)
lines=f.readlines()
f.close()
g=open('tmp.csv','w')


ymin=meta['ymin']
ymax=meta['ymax']
xmin=meta['xmin']
xmax=meta['xmax']
selval=meta['sel']
xtype=meta['xtype']
ytype=meta['xtype']
seltype=meta['seltype']

print len(lines[0].strip().split(','))
ypixels=len(lines)
xpixels=len(lines[1].split(','))-1
ystep=(ymax-ymin)/(ypixels*1.0)
xstep=(xmax-xmin)/(xpixels*1.0)

print xmin,xmax,xstep
y=ymin
for l in lines:
    cols=l.strip().split(',')
    x=xmin
    print len(cols)
    
    for c in cols:
        
        if c!='':
            s=''
            s+=print_type(x,xtype)
            s+=','
            s+=print_type(y,ytype)
            s+=','
            s+=print_type(selval,seltype)
            s+='\n'          
            g.write(s)
            x+=xstep
    y+=ystep

g.close()

metadict['curdir']=os.getcwd()
s="copy {{table}} from '{{curdir}}\\tmp.csv' DELIMITERS '{{delimiter}}' csv header;"
sql=Environment().from_string(s).render(metadict)
d.run_sql(sql)
