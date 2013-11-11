import os,sys,yaml
from jinja2 import Environment
from localyaml import OrderedDictYAMLLoader
from heatmapr.db import dbconnection


if len(sys.argv)<2:
    print 'usage: python in.py <filename> [raw|num]'
    print 'imports csv file into db'
    print 'from meta in filename'
    print 'raw: imports to raw data'
    print 'num: imports to aggegrate data'
    sys.exit()


fname=sys.argv[1]
dumptype='raw'
if len(sys.argv)==3:
    dumptype=sys.argv[2]
    if dumptype not in('raw','num'):
        print "dumptype (arg 2) should be 'raw' or 'num'"
        sys.exit()

        
f=open(fname)
desc=f.read()
f.close()




def print_type (val, type_val):

    if type_val=='int':
        return str(int(val))
    if type_val=='decimal':
        return '%.4f' % val
    return str(val)



meta=yaml.load('{'+desc+'}', OrderedDictYAMLLoader)
metadict={}
for k,v in meta.items():
    metadict[k]=v
d=dbconnection(meta)

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

#print len(lines[0].strip().split(','))
ypixels=len(lines)-1
xpixels=len(lines[1].split(','))-1
ystep=(ymax-ymin)/(ypixels*1.0)
xstep=(xmax-xmin)/(xpixels*1.0)

#print xmin,xmax,xstep
#print ymin,ymax,ystep

header=meta['xcol']+','+meta['ycol']
if meta.has_key('selcol'):
    header+=','+meta['selcol']
if dumptype=='num':
    header+=',num'
header+='\n'
    
g.write (header)
y=ymin
for l in lines:
    cols=l.strip().split(',')
    x=xmin
   # print len(cols)
    
    for col in cols:        
        if col!='':
            s=''
            s+=print_type(x,xtype)
            s+=','
            s+=print_type(y,ytype)
            s+=','
            s+=print_type(selval,seltype)            
            if dumptype=='raw':     # 'num' uitvouwen naar num records
                s+='\n'
                numval=int(col)
                for i in range(numval):
                    g.write(s)
            if dumptype=='num':
                s+=','+col+'\n'
                g.write(s)
            x+=xstep
    y+=ystep

g.close()

metadict['curdir']=os.getcwd()
s="copy {{table}} from '{{curdir}}\\tmp.csv' DELIMITERS '{{delimiter}}' csv header;"
sql=Environment().from_string(s).render(metadict)
d.run_sql(sql)
