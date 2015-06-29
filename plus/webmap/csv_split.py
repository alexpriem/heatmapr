import sys, glob, datetime, gzip, csv
from operator import itemgetter

 
verbose=2
       
def prepmatch (matches):

    matchdict={}
    matchtype={}
    for m in matches:
        if '=' in m:
            k,v=m.split('=')
            matchtyp='='
        if '!' in m:
            k,v=m.split('!')
            matchtyp='!'
        if '>' in m:
            k,v=m.split('>')
            matchtyp='>'
        if '<' in m:
            k,v=m.split('<')
            matchtyp='<'

            
        matchdict[k.lower()]=v.lower()
        matchtype[k.lower()]=matchtyp
        
    return matchdict, matchtype



# todo:
# 1-kolommen overnemen uit externe file.
# 2-meer dan 500 kolommen: opslitsten in batches, multiple passes doen.
# 3-subselecties aangeven (match)

def csv_select (infile, outfile, sep_in, match=None, global_recode=None):


    sep_out=','
    if match is None:
        matchdict, matchtype=prepmatch(match)
    else:
        matchdict={}
        matchtype={}
    f=open (infile)
    #f=gzip.open (infile,'r')


    c=csv.reader(f,delimiter=sep_in)
    
    keys=c.next()
    keys=[k.lower() for k in keys]    

    subkeys=[]
    subcolnr={}
    for key in keys:
        if key[0]!='y':
            subkeys.append(key)
            subcolnr[key]=keys.index(key)            
    print '#variabelen naar csv-files:',len(subkeys)
    filedict={}
    for key in subkeys:        
        filedict[key]=open(outfile+key+'.csv','w')

#    sys.exit()
#    for i in range(0,10):
#        cols=f.readline().split(sep_in)        
        
    matchcols=[]
    matchvals=[]
    for matchkey, matchval in matchdict.items():        
        matchcols.append(keys.index(matchkey))
        matchvals.append(matchval) 
           

    i=0
    j=0
    for line in c:        
        if verbose==2 and i%1000==0:
            print i, j
        i+=1
            
        vals=line
        if global_recode is not None:
            vals=[global_recode.get(val, val) for val in vals]
                    
       # print vals
        match=True
        for k,v in zip(matchcols,matchvals):
            matchcolname=keys[k]
            matchtyp=matchtype[matchcolname]
            val=vals[k]
          #  print '[%s][%s], %s' % (val, v, matchcolname), val==v, matchtyp
            if matchtyp=='=' and val!=v:
                match=False
                break        
            if matchtyp=='!' and val==v:
                match=False
                break        
            if matchtyp=='>' and val<=v:
                match=False
                break        
            if matchtyp=='<' and val>=v:
                match=False                
                break        
        if match==False:
            continue

        j+=1

        # data uitschrijven
        
        for key in subkeys:
            try:
                val=vals[subcolnr[key]]
            except:
                print j, key                
            f=filedict[key]
            f.write('%s\n' % val)
        

    for f in filedict.values():
        f.close()


