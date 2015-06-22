import os, sys



def dictify(infodir, colname):
    
    f=open(infodir+'\\split\\%s.csv' % colname,'r')

    hist={}
    l=f.readline()
    for line in f:
        k=line.strip()
        hist[k]=hist.get(k,0)+1

    histdir=infodir+'\\hist'
    if not os.path.exists(histdir):
        os.makedirs(histdir)        

    outfile=histdir+'\\%s.csv' % colname

    f=open (outfile,'w')
    f.write('%s:num\n' % colname)
    for k in sorted (hist.keys()):        
        f.write('%s:%d\n' % (k,hist[k]))


def dictify_all_the_things(infodir, cols):
    for col in cols:
        print col
        dictify(infodir,col)

    
        
