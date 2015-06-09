import sys, glob, datetime, gzip
from operator import itemgetter

 
datadir='t:\\ib\\'
#infile=datadir+'ib2010_1k.csv'
infile=datadir+'ib2010.csv2'
outfile='split/'
match=['srtadr=1','h_ink=1']
sep_in=';'
sep_out=','
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



def csv_select (infile, outfile, matchdict, matchtype):


    
    f=open (infile,'r')
    #f=gzip.open (infile,'r')

    
    keys=f.readline().strip().split(sep_in)
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
    for i in range(0,10):
        cols=f.readline().split(sep_in)        
        
    matchcols=[]
    matchvals=[]
    for matchkey, matchval in matchdict.items():        
        matchcols.append(keys.index(matchkey))
        matchvals.append(matchval)


            

    i=0
    j=0
    for line in f:
        i+=1
        if verbose==2 and i%1000==0:
            print i, j
        vals=line.strip().split(sep_in)
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
            val=vals[subcolnr[key]]
            f=filedict[key]
            f.write('%s\n' % val)
        

    for f in filedict.values():
        f.close()


matchdict, matchtype=prepmatch(match)
csv_select (infile, outfile, matchdict, matchtype)
