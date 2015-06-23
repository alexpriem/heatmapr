import sys
import array
from collections import defaultdict





def parse_header (headerfile):
    f=open(headerfile,'r')
    filename=f.readline().split('=')[1].strip()
    sep=f.readline().split('=')[1].strip()    
    cols=[col.strip() for col in f]    
    f.close()   
    return filename, sep, cols




def make_hist (variabele):

    try:
        f=open('splitbin\\%s.info' % variabele, 'r' )
    except:        
        print 'skipping %s, no data' % variabele
        return
    minx=f.readline()
    minx=float(minx.split(':')[1])
    maxx=f.readline()
    maxx=float(maxx.split(':')[1])
    delta=f.readline()
    delta=float(delta.split(':')[1])
    num_keys=f.readline()    
    try:
        num_keys=int(num_keys.split(':')[1])
    except:
        num_keys=1000
    f.close()
    print num_keys
    
    try:
        f=open('splitbin\\%s.bin' % variabele,'r')
    except:
        return
    if num_keys<256:
        a=array.array('B')
    else:
        a=array.array('H')
    a.fromstring(f.read())
    f.close()
    data=a.tolist()
    print len(data), num_keys
    counts=defaultdict(int)
    for d in range(0,num_keys):
        counts[d]=0
    for d in data:
        counts[d]+=1
    print '%s done' % variabele
    f=open('histo\\%s.csv' % variabele , 'w')
    for k in sorted(counts.keys()):
        v=counts[k]
        f.write('%s,%s\n' % (k,v))
    f.close()
          


filename, sep, cols=parse_header(sys.argv[1])
for col in cols:
    make_hist(col)
