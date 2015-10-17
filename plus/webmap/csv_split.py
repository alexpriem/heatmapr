import os, sys, glob, datetime, gzip, csv
import helpers
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

def split_batch (csvfile, splitdir, batchkeys, keys, colnr, matchcolnrs, matchvals, matchtypes, global_recode):

    filedict={}
    for key in batchkeys:
        filedict[key]=open(splitdir+key+'.csv','w')

    i=0
    j=0
    for line in csvfile:
        if verbose==2 and i%1000==0:
            print i, j
        i+=1
    #    if i>10000:
     #       break

        vals=line
        if global_recode is not None:
            vals=[global_recode.get(val, val) for val in vals]

       # print vals
        match=True
        for matchkey, matchtype, matchval in zip(matchcolnrs,matchtypes,matchvals):
            val=vals[matchkey]
          #  print '[%s][%s], %s' % (val, v, matchcolname), val==v, matchtyp
            if matchtype=='=' and val!=matchval:
                match=False
                break
            if matchtype=='!' and val==matchval:
                match=False
                break
            if matchtype=='>' and val<=matchval:
                match=False
                break
            if matchtype=='>=' and val<matchval:
                match=False
                break
            if matchtype=='<=' and val>matchval:
                match=False
                break
            if matchtype=='<' and val>=matchval:
                match=False
                break
        if match==False:
            continue

        j+=1

        # data uitschrijven

        for key in batchkeys:
            try:
                val=vals[colnr[key]]
            except:
                print 'Line %d, Exception looking for:%s' % (i, key)
                print 'index:', colnr.get(key,'key undefined'), 'len vals:', len(vals)
                return

            f=filedict[key]
            f.write('%s\n' % val)


    for f in filedict.values():
        f.close()





def csv_select (datadir, dataset, infodir, sep_in):

    splitdir=infodir+'/split/'
    if not os.path.exists(splitdir):
        os.makedirs(splitdir)

    matches=helpers.read_filterfile(infodir)
    recodes, recodeset=helpers.read_recodefile (infodir)

    print 'MATCHES'
    print matches
    print 'MATCHES'

    config=helpers.read_configfile(infodir)

    name2colnr={}
    enabled_keys=[]
    keys=[]
    for i,row in enumerate(config):
        colname=row['colname'].lower()
        print i,colname
        keys.append(colname)
        name2colnr[colname]=i
        if int(row['enabled'])==1:
            enabled_keys.append(colname)

    print '#variabelen naar csv-files:',len(enabled_keys)

    matchcolnrs=[]
    matchvals=[]
    matchtypes=[]
    for m in matches:

        matchcolnrs.append(name2colnr(m['key'].lower()))
        matchtypes.append(m['compare'])
        matchvals.append(m['value'])

    infile=datadir+'/'+dataset+'.csv'
    f=open (infile)
    #f=gzip.open (infile,'r')
    c=csv.reader(f,delimiter=sep_in)

    print matchcolnrs, matchvals, matchtypes

    startkey=0
    batchsize=500
    batchkeys=enabled_keys[startkey:startkey+batchsize]
    print 'name2colnr:',name2colnr

    while len(batchkeys)!=0:
        print startkey, len(batchkeys)
        split_batch(c, splitdir, batchkeys, keys, name2colnr, matchcolnrs, matchvals, matchtypes,recodes)
        f.seek(0,0)
        f.readline()
        startkey+=batchsize
        batchkeys=enabled_keys[startkey:startkey+batchsize]

