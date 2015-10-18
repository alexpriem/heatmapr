import os, sys, csv, array
from collections import defaultdict
import helpers


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
    c=csv.reader(f, delimiter=',')
    binsize=(maxx-minx)/(bins*1.0)
    histogram=[0]*(bins+1)
    for row in c:
        #print row
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
   # for x in histogram:
   #     print x[0],x[1]
    return histogram, sorted_hist
        



def prep_hist_subsel (infodir, variabele, minx, maxx, bins, subsel):



# stage 1: selectie maken en binnen naar key/values
# stage 2: histogram maken opbv /selhists
    data=helpers.read_csvfile (infodir, variabele)
    f=open(infodir+'/hists/%s.csv' % variabele)
    f.readline()
    c=csv.reader(f, delimiter=',')
    binsize=(maxx-minx)/(bins*1.0)
    histogram=[0]*(bins+1)
    for row in c:
        #print row
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
   # for x in histogram:
   #     print x[0],x[1]
    return histogram, sorted_hist




        

def get_data(infodir, variabele):

    f=open(infodir+'/hists/%s.csv' % variabele)
    f.readline()
    c=csv.reader(f, delimiter=',')
    data=[]
    for row in c:
        x,num=row[0],row[1]
        try:
            x=float(row[0])
            if x.is_integer():
                x=int(x)
        except:
            pass
        data.append([x,int(num)])
    return data




def make_hist3 (data, minx, maxx, bins):

    binsize=(maxx-minx)/(bins*1.0)
    histogram=[0]*(bins+1)
    for row in data:
        x,num=row[0],row[1]
        if (x<minx) or (x>maxx):
            continue
        hx=int((x-minx)/binsize)
        try:
            histogram[hx]+=num
        except:
            print 'histogram out of bounds:',hx,binsize
            raise RuntimeError
    sorted_hist=sorted(histogram)
    histogram=[[(minx+i*binsize),h] for i,h in enumerate(histogram)]
   # for x in histogram:
   #     print x[0],x[1]
    return histogram, sorted_hist



def check_binsize(data,minx,maxx,bins):

    num_keys=0
    for row in data:
        x=row[0]
        if ((x<minx) or (x>maxx)):
            continue
        num_keys+=1
    if num_keys<bins:
        bins=num_keys
    return bins







def prepare_subsel (infodir, coltypes_bycol, xvar,xmin,xmax,  yvar,ymin,ymax):

    print xvar, yvar

    xinfo=coltypes_bycol[xvar]
    yinfo=coltypes_bycol[yvar]

    xvals=helpers.read_and_convert_csvfile (infodir, xvar, xinfo['datatype'])
    yvals=helpers.read_and_convert_csvfile (infodir, yvar, xinfo['datatype'])

    subsel=[]
    for i,(x,y) in enumerate(zip(xvals,yvals)):

        if (x>xmin) and (x<xmax):
           # print xmin, xmax, x, ymin, ymax, y
            if (y>ymin) and (y<ymax):
                subsel.append(i)
    print len(subsel)
    return subsel




def prepare_missing (infodir, coltypes_bycol, varname):

    info=coltypes_bycol[varname]
    f=open('%s/split/%s.csv' % (infodir,varname))

    if info['missing']<0.5*info['total']:
        missings=[]
        for i, row in enumerate(f):
            if row=='':
                missings.append(i)
        return True,missings

    nonmissings=[]
    for i, row in enumerate(f):
        if row!='':
            nonmissings.append(i)


    return False,nonmissings



def prepare_subselection (infodir, coltypes_bycol, xvar,xmin,xmax,  yvar,ymin,ymax):

    xinfo=coltypes_bycol[xvar]
    yinfo=coltypes_bycol[yvar]
    xind=xinfo['bin_indirect']
    xcode=xinfo['bin_typecode'].strip()
    yind=yinfo['bin_indirect']
    ycode=yinfo['bin_typecode'].strip()

    xvals=array.array(xcode)
    yvals=array.array(ycode)

    xfile=open('%s/splitbin/%s.bin' % (infodir,xvar), 'rb' )
    xvals.fromstring(xfile.read())
    xfile.close()


    yfile=open('%s/splitbin/%s.bin' % (infodir, yvar) ,'rb')
    yvals.fromstring(yfile.read())
    yfile.close()


    if xind:
        i=0
      #  print '%s/hist/%s.csv' % (infodir, xvar)
        xhist=helpers.read_list('%s/hist/%s.csv' % (infodir, xvar),skipheader=True)
    if yind:
        i=0
        yhist=helpers.read_list('%s/hist/%s.csv' % (infodir,yvar),skipheader=True)
    sel=[0]*len(xvals)
    i=0
    j=0
    print xvar,'hist',xhist[:10]

    for x,y in zip(xvals,yvals):
        j+=1
        if xind:
            print x
            x=float(xhist[x-1])
        if yind:
            try:
                y=float(yhist[y-1])
            except:
                print y, len(yhist)

        if j<0:
            print xvar,xmin,xmax,x,'  ',  yvar,ymin,ymax,y
        if (x>xmin) and (x<xmax) and (y>ymin) and (y<ymax):
            sel[i]=1
        i+=1

    if not os.path.exists(infodir+'/selecties'):
        os.makedirs(infodir+'/selecties')
    print 'found:',len(sel)

    h=open(infodir+'/selecties/selectie_%s_%s.csv' % (xvar, yvar),'w')
    for nr in sel:
        h.write('%d\n' % nr )  # tzt ook binair opsplaan
    h.close()






