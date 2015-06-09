import sys
from array import array


def transform(val,coltype):

    if coltype=='int':
        return(int(val))
    if coltype=='float':
        return(float(val))    
    return val

    


f=open(sys.argv[1],'r')
filename=f.readline().split('=')[1].strip()
sep=f.readline().split('=')[1].strip()
cols=[]
coltypes=[]
for col in f:
    col, coltype=col.strip().split(':')    
    cols.append(col)
    coltypes.append(coltype)
f.close()


f=open(filename,'r')
header=f.readline().strip().split(sep)
colnrs=[header.index(c) for c in cols]
print colnrs

csvfiles=[open(col+'.csv','w') for c in cols]
binfiles=[open(col+'.bin','wb') for c in cols]




for line in f:
    data=line.strip().split(sep)
    datasel=[data[nr] for nr in colnr]
    for val,coltype,csvfile,binfile in zip(datasel,coltypes,csvfile,binfile):
        csvfile.write('%s\n',val)
        if coltype=='tinyint':
            data_array=array('%b',[val])
        if coltype=='smallint':
            data_array=array('%i',[val])
        if coltype=='int':
            data_array=array('%L',[val])
        if coltype=='float':
            data_array=array('%f',[val])
        if coltype=='ascii':
            data_array=array('c',val)

        data_array.tofile(binfile)
        
    
      
        
