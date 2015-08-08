import os,sys, cjson, shutil, csv
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt


from csv_split import csv_select
from dictify import dictify_all_the_things
from dict2type import typechecker
from makehist import make_hist3, get_data, check_binsize
from helpers import get_col_types
import heatmap




def get_label(filehandle, labeldict):
        c=csv.reader(filehandle,delimiter=',')
        for row in c:
            key,label=row[0],row[1]
            try:
                key=float(key)
                if key.is_integer():
                    key=int(key)
            except:
                pass
            labeldict[key]=label
        return labeldict


def get_labels (infodir, variabele):

    f=None
    try:
        f=open(infodir+'/labels/defaults.csv','r')
    except:
        pass
    labels={}
    if f is not None:
        labels=get_label(f, labels)

    f=None
    try:
        f=open(infodir+'/labels/%s.csv' % variabele,'r')
    except:
        pass
    if f is not None:
        labels=get_label(f, labels)
    return labels




def get_plot_alphanumeric (infodir,variable, rowinfo):

    print 'get_plot_alphanumeric'
    f=open(infodir+'/hists/%s.csv' % variable,'r')
    f.readline()
    c=csv.reader(f,delimiter=',')
    data=[]
    stringdata=[]
    maxnum=0
    for row in c:
        key,num=row[0],row[1]
        num=int(num)
        if len(key)>=2:
            if key[0]=='0' and key[1].isdigit():    # voorloopnul -> string ipv int/float
                stringdata.append([key,num])
                continue

        if num>maxnum:
            maxnum=num
        try:
            numeric_key=float(key)
            if numeric_key.is_integer():
                numeric_key=int(numeric_key)
        except:
            stringdata.append([key,num])
            continue
        data.append([numeric_key,num])
    f.close()
    #print data
   # print stringdata
    rowinfo['bins']=len(data)
    rowinfo['data']=data
    rowinfo['stringdata']=stringdata

    num_keys=rowinfo['num_keys']
    if num_keys<14:
        rowinfo['minx'], rowinfo['miny']=rowinfo['min'],0
        rowinfo['maxx'], rowinfo['maxy']=rowinfo['max'],maxnum
        rowinfo['maxy2'], rowinfo['maxy3']=maxnum,maxnum
    else:
        rowinfo['minx'], rowinfo['miny']=rowinfo['min'],0
        rowinfo['maxx'], rowinfo['maxy']=rowinfo['max'],maxnum
        rowinfo['maxy2'], rowinfo['maxy3']=maxnum,maxnum

    return rowinfo




def get_plot (infodir, variable, col_info=None, coltypes_bycol=None):

    if col_info is None:
        col_info, coltypes_bycol=get_col_types(infodir)

    rowinfo=coltypes_bycol[variable]
    print 'get_plot:',variable

    try:
        f=open(infodir+'/hista/%s.csv' % variable,'r')
    except:
        return get_plot_alphanumeric(infodir, variable, rowinfo)

    # numerieke data
    
    f.readline()
    c=csv.reader(f,delimiter=':')


    # FIXME: bijwerken met info uit coltypes
    minx,miny=c.next()    #  1st row contains minx, miny
    rowinfo['minx'], rowinfo['miny']=float(minx), float(miny)
    maxx,maxy=c.next()    #  2nd row contains maxx, maxy
    rowinfo['maxx'], rowinfo['maxy']=float(maxx), float(maxy)
    maxy2,maxy3=c.next()
    rowinfo['maxy2'], rowinfo['maxy3']=float(maxy2),float(maxy3)  #  2nd row contains maxx, maxy

    data=[]
    for row in c:
        x,num=row[0],row[1]
        x=float(x)
        if x.is_integer():
            x=int(x)
        num=int(num)
        data.append([x,num])
    f.close()

    # string garbage ophalen. Optimalizatie: naar aparte file in /hista
    f=open(infodir+'/hists/%s.csv' % variable,'r')
    f.readline()
    c=csv.reader(f,delimiter=',')
    stringdata=[]
    for row in c:
       # print row
        key,num=row[0],row[1]
        try:
            key=float(key)
        except:
            stringdata.append([key,int(num)])
    rowinfo['bins']=100
    rowinfo['data']=data
    rowinfo['stringdata']=stringdata
    return rowinfo



def test_heatmap (col_info):

    colname=col_info['colname']

    if (col_info['datatype']!='int') and (col_info['datatype']!='float'):
        return None
    if (col_info['num_keys']<10):
        return None
    if (col_info['num_valid']<10):
        return None

    return colname


@csrf_exempt
def histogram (request, dataset, variable):

    datadir='e:/data'
    infodir=datadir+'/'+dataset+'_info'
    if not os.path.exists(infodir):
        os.makedirs(infodir)    
    col_info, coltypes_bycol=get_col_types(infodir)
    rowinfo=coltypes_bycol[variable]
    rowinfo['labels']=get_labels(infodir,variable)


    if request.is_ajax()==True:
        cmd=request.GET['cmd']            
        if cmd=='reset':           
            rowinfo=get_plot(infodir, variable,col_info, coltypes_bycol)
            data={'action':'makeplot','data':rowinfo}  # plus histogram
        if cmd=='resize':
            minx=float(request.GET.get('minx',0))
            maxx=float(request.GET.get('maxx',100))
            miny=float(request.GET.get('miny',0))
            maxy=float(request.GET.get('maxy',100))
            bins=int(request.GET.get('bins',100))
            print 'RESIZE',minx,maxx,bins
            rowinfo=get_plot(infodir, variable,col_info, coltypes_bycol)
            rowinfo['minx']=minx
            rowinfo['maxx']=maxx
            rowinfo['miny']=miny
            rowinfo['maxy']=maxy

            data=get_data(infodir, variable)
            bins=check_binsize(data,minx,maxx,bins)
            histogram, sorted_hist=make_hist3 (data,minx,maxx,bins)
            rowinfo['data']=histogram
            #rowinfo['maxy']=sorted_hist[-1]
            rowinfo['maxy2']=sorted_hist[-2]
            rowinfo['maxy3']=sorted_hist[-3]
            rowinfo['bins']=bins

            data={'action':'makeplot','data':rowinfo}

        if cmd=='check_heatmap':

            heatmaps=['ab','cd','ef']
            heatmapcols=[]
            for col in col_info:
                heatmapcol=test_heatmap(col)
                if heatmapcol is not None:
                    heatmapcols.append(heatmapcol)

            data={'action':'check_heatmap','data':heatmapcols}


        
        return HttpResponse(cjson.encode(data))


    template = loader.get_template('histogram.html')
    if (rowinfo['datatype']=='char' and rowinfo['num_keys']>100):
        rowinfo['data']=[]              # dummies
        rowinfo['stringdata']=[]
    else:
        rowinfo=get_plot(infodir, variable,col_info, coltypes_bycol) # plus histogram

    colnr=rowinfo['colnr']
    prevvar1=''
    prevvar2=''
    if colnr>0:
        prevvar1=col_info[colnr-1]['colname']
    if colnr>1:
        prevvar2=col_info[colnr-2]['colname']

    nextvar1=''
    nextvar2=''
    if colnr<len(col_info)-1:
        nextvar1=col_info[colnr+1]['colname']
    if colnr<len(col_info)-2:
        nextvar2=col_info[colnr+2]['colname']



    print 'got rowinfo'
    histogram_json=cjson.encode(rowinfo)
    context = RequestContext(request, {'dataset':dataset,
                                       'prevcolname2':prevvar2,
                                       'prevcolname1':prevvar1,
                                       'colname':variable,
                                       'nextcolname1':nextvar1,
                                       'nextcolname2':nextvar2,
                                       'histogram':histogram_json})
    print 'got context'    
    return HttpResponse(template.render(context))

