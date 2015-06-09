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

for col in cols:
    print '%s' % (col)
        
        

    
    


