import sys

f=open('split\\'+sys.argv[1],'r')

hist={}
for line in f:
    k=line[:-1]
    hist[k]=hist.get(k,0)+1


outfile='hist\\%s' % sys.argv[1]

f=open (outfile,'w')
for k in sorted (hist.keys()):
    f.write('%s:%d\n' % (k,hist[k]))

    
        
