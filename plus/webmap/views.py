import os,sys, cjson, shutil
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from csv_split import csv_select



# Create your views here.


def top (request):

    template = loader.get_template('top.html')

    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

    

def heatmap (request, dataset):

    print request.path
    print request #.META
    
    #print dataset
    template = loader.get_template('bitmap.html')

    context = RequestContext(request, {})
    return HttpResponse(template.render(context))





def split_csv_file (datadir, dataset, infodir):

    splitdir=infodir+'/split'
    if not os.path.exists(splitdir):
        os.makedirs(splitdir)
        state=0  # empty


    infile=datadir+'/'+dataset+'.csv'
    outfile=infodir+'/split/'
    sep=','
    match=[] # ['srtadr=1','h_ink=1']

        
    csv_select (infile, outfile, sep, match)



def read_header (filename,sep=None):


    f=open(filename,'r')
    headerline=f.readline()
    if sep is None:
        sep=','
        if len(headerline.split(sep))==1:
            sep=';'
            if len(headerline.split(';'))==1:
                raise RuntimeError ('unknown separator')
            
    cols=[col.strip() for col in headerline.split(sep)]    
    return sep, cols






def dataset (request, dataset):

    #print request.GET['dataset']
    action=request.GET['action']    
    datadir=request.GET['datadir']
    msg=''
        

    # kijken of info-dir bestaat

    infodir=datadir+'/'+dataset+'_info'

    if action=='split':
        split_csv_file (datadir, dataset, infodir)


    if action=='clear1':  # full clean
        shutil.rmtree(infodir)
        msg='all cleared'

    if not os.path.exists(infodir):
        os.makedirs(infodir)
        state=0  # empty


    

    try:
        f=open(infodir+'/col_info.csv','r')
        sep=f.readline().strip()[4:]
        cols=[]
        for line in f:
            cols.append(line.strip())
    except:        
        sep,cols=read_header(datadir+'/'+dataset+'.csv')        
        f=open(infodir+'/col_info.csv','w')
        f.write('sep=%s\n' % sep)
        for col in cols:
            f.write(col+'\n')
        f.close()
    
    columns=[]
    for col in cols:
         columns.append({'colname':col, 'type':'--','label':'--','enabled':True})
        
        
        
    data={'dataset':dataset, 'sep':sep, 'columns':columns, 'msg':msg}
    return HttpResponse(cjson.encode(data))

