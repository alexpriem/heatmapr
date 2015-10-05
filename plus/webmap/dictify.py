import os, csv
import helpers


def dictify(infodir, colname):
    
    f=open(infodir+'\\split\\%s.csv' % colname,'r')

    hist={}
    for line in f:
        k=line[:-1]
        hist[k]=hist.get(k,0)+1

    histdir=infodir+'\\hist'
    if not os.path.exists(histdir):
        os.makedirs(histdir)        

    outfile=histdir+'\\%s.csv' % colname

    f=open (outfile,'wb')
    c=csv.writer(f, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
    c.writerow([colname,'num'])
    for k in sorted (hist.keys()):        # alfabetisch gesorteerd, dwz 10<2 !!!
        c.writerow([k,hist[k]])
    f.close()


def dictify_all_the_things(infodir, cols):

    enabled_cols=helpers.get_enabled_cols(infodir)
    for col in enabled_cols:
        print col
        dictify(infodir,col)

    
        
