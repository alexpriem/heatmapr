import sys

if len(sys.argv)==3:
    sep=sys.argv[2]
    f=open(sys.argv[1],'r')
    headerline=f.readline()
else:
    f=open(sys.argv[1],'r')
    headerline=f.readline()
    sep=','
    if len(headerline.split(sep))==1:
        sep=';'
        if len(headerline.split(';'))==1:
            raise RuntimeError ('unknown separator')        


print 'filename=%s ' % sys.argv[1]
print 'sep=%s' % sep

cols=[col.strip() for col in headerline.split(sep)]

types=[]
for line in f:    
    data=[d.strip() for d in line.split(sep)]

    newtypes=[]
    for d in data:
        t='float'
        try:
            v=float(d)
        except:
            t='ascii'
        if t=='float':
            if not ('.' in d):
                t='int'
        newtypes.append(t)
    if len(types)==0:
        types=newtypes
        continue
    types2=[]
    for t,newt in zip(types, newtypes):
        val=t
        if newt=='float' and t=='int':
            val='float'
        if newt=='ascii' and t=='float':
            val='ascii '
        types2.append(val)
    types=types2

for col,t in zip(cols,types):
    print '%s:%s' % (col,t)
        
        

    
    


