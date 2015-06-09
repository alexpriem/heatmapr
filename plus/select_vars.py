import sys, array


def parse_header (headerfile):
    f=open(headerfile,'r')
    filename=f.readline().split('=')[1].strip()
    sep=f.readline().split('=')[1].strip()
    cols=[]
    cols=[col.strip().lower() for col in f]
    f.close()
    return filename, sep, cols


def parse_header2 (header2file):
    f=open(header2file,'r')
    filename=f.readline().split('=')[1].strip()
    sep=f.readline().split('=')[1].strip()
    cols=[]
    types=[]
    subtypes=[]
    typecodes=[]
    minvals=[]
    maxvals=[]
   # c=[col.strip().split(',') for col in f]
   # print c
    lines=[col.strip().split(',') for col in f]
    for line in lines:
        cols.append(line[0].lower())
        types.append(line[1])
        subtypes.append(line[2])
        typecodes.append(line[3])
        minvals.append(line[4])
        maxvals.append(line[5])
    
    f.close()
    return filename, sep, cols, types, subtypes, typecodes, minvals, maxvals




headerfile=sys.argv[1]
#filename, sep, cols=parse_header(headerfile)
filename, sep, cols, types, subtypes, typecodes, minvals, maxvals=parse_header2(headerfile+'2')

indexfile=sys.argv[2]
f=open(indexfile)
indexlist=[int(line[:-1]) for line in f]
#print indexlist[:10]
f.close()






for col, typecode in zip(cols, typecodes):
    print col, typecode
    try:
        f=open('splitbin\\%s.info' % col, 'r' )
    except:
        f.close()
        print 'skipping %s, no data' % col
        continue
    minx=f.readline().strip()
    minx=float(minx.split(':')[1])
    maxx=f.readline().strip()
    maxx=float(maxx.split(':')[1])
    delta=f.readline().strip()
    delta=float(delta.split(':')[1])
    num_keys=f.readline().strip()
    try:
        num_keys=int(num_keys.split(':')[1])
    except:
        num_keys=1000
    f.close()
    
    #data=array.array(typecode)
    if num_keys<256:
        data=array.array('B')
    else:
        data=array.array('H')
    f=open('splitbin\\%s.bin' % col, 'rb' )
    data.fromstring(f.read())
    data=data.tolist()    
    f.close()
    hist={}
    g=open('sel\\%s.csv' % col,'w')
    g.write('key,x,num\n')
    for i in indexlist:
        d=data[i]
        hist[d]=hist.get(d,0)+1
    for k in sorted(hist.keys()):
        g.write('%s,%s,%s\n' % (k,k*delta+minx,hist[k]))
    g.close()
   # sys.exit()    

