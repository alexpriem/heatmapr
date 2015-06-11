import sys


filename=sys.argv[1]
if len(sys.argv)==3:
    sep=sys.argv[2]
    f=open(filename,'r')
    headerline=f.readline()
else:
    f=open(filename,'r')
    headerline=f.readline()
    sep=','
    if len(headerline.split(sep))==1:
        sep=';'
        if len(headerline.split(';'))==1:
            raise RuntimeError ('unknown separator')        


infodir=filename.strip()[:-4]
if not os.path.exists(infodir):
    os.makedirs(infodir)

f=open(infodir+'\\header.txt','w')
f.write('filename=%s ' % filename)
f.write('sep=%s' % sep)

cols=[col.strip() for col in headerline.split(sep)]
for col in cols:
    f.write ('%s' % (col))
        
        

    
    


