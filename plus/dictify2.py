import sys



def dictify(colname):

    f=open('split\\%s.csv' % colname,'r')

    hist={}
    l=f.readline()
    for line in f:
        k=line.strip()
        hist[k]=hist.get(k,0)+1
    
    outfile='hist\\%s.csv' % colname

    f=open (outfile,'w')
    f.write('%s:num\n' % colname)
    for k in sorted (hist.keys()):        
        f.write('%s:%d\n' % (k,hist[k]))


# parse headerfile


def parse_header (headerfile):
    f=open(headerfile,'r')
    filename=f.readline().split('=')[1].strip()
    sep=f.readline().split('=')[1].strip()
    cols=[]
    cols=[col.strip() for col in f]
    f.close()
    return filename, sep, cols


filename, sep, cols=parse_header(sys.argv[1])
for col in cols:
    print col
    if col=='.':
        break        
    dictify(col)

    
        
