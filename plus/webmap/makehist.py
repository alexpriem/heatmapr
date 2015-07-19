import sys, csv, array
from collections import defaultdict



def make_hist (infodir, variabele):

    try:
        f=open(infodir+'\\splitbin\\%s.info' % variabele, 'r' )
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
        f=open(infodir+'splitbin\\%s.bin' % variabele,'r')
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
    histdir=infodir+'/histo' 
    if not os.path.exists(histdir ):
        os.makedirs(histdir)
    f=open(histdir+'/%s.csv' % variabele , 'w')
    for k in sorted(counts.keys()):
        v=counts[k]
        f.write('%s,%s\n' % (k,v))
    f.close()



          

def make_hist2 (infodir, variabele, minx, maxx, bins):
    
    f=open(infodir+'/hists/%s.csv' % variabele)
    f.readline()
    print type(minx), type(maxx), type(bins)
    c=csv.reader(f, delimiter=':')
    binsize=(maxx-minx)/(bins*1.0)
    histogram=[0]*(bins+1)
    for row in c:
        try:
            x=float(row[0])
        except:
            pass
        val=int(row[1])
       
        if (x<minx) or (x>maxx):
            continue        
        hx=int((x-minx)/binsize)
        try:
            histogram[hx]+=val
        except:
            print 'hx:',hx,binsize
            raise RuntimeError
    sorted_hist=sorted(histogram)
    
    histogram=[[(minx+i*binsize),h] for i,h in enumerate(histogram)]
#    for x in histogram:
        #print x[0],x[1]
    return histogram, sorted_hist
        
            
        
    
