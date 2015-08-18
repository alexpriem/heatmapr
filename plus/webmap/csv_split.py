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



# helperfunction for csv_select

def split_batch (csvfile, outfile, batchkeys, subcolnr, global_recode, matchcols, matchvals):


    filedict={}
    for key in batchkeys:
        filedict[key]=open(outfile+key+'.csv','w')

    i=0
    j=0
    for line in csvfile:
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

        for key in batchkeys:
            try:
                val=vals[subcolnr[key]]
            except:
                print 'Exception:%s,%s' % (j, key)
                print subcolnr

            f=filedict[key]
            f.write('%s\n' % val)


    for f in filedict.values():
        f.close()


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

    matchcols=[]
    matchvals=[]
    for matchkey, matchval in matchdict.items():
        matchcols.append(keys.index(matchkey))
        matchvals.append(matchval)

    numcols=len(subkeys)
    startkey=0
    batchsize=500
    batch=subkeys[startkey:startkey+batchsize]
    while len(batch)!=0:
        print startkey, len(batch)
        split_batch(c, outfile, batch, subcolnr, global_recode, matchcols, matchvals)
        f.seek(0,0)
        f.readline()
        startkey+=batchsize
        batch=subkeys[startkey:startkey+batchsize]

