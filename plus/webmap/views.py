import os,sys, cjson, shutil
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from csv_split import csv_select
from dictify import dictify_all_the_things



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





def split_csv_file (datadir, dataset, infodir, match, global_recode):

    splitdir=infodir+'/split'
    if not os.path.exists(splitdir):
        os.makedirs(splitdir)
        state=0  # empty


    infile=datadir+'/'+dataset+'.csv'
    outfile=infodir+'/split/'
    sep=','
    if match is None:
        match=[]    # ['srtadr=1','h_ink=1']

        
    csv_select (infile, outfile, sep, match, global_recode)



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


def get_cols (datadir, dataset, infodir):
    
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
    return sep, cols





def dataset (request, dataset):

    #print request.GET['dataset']
    action=request.GET['action']    
    datadir=request.GET['datadir']
    msg=''
        

    # kijken of info-dir bestaat

    infodir=datadir+'/'+dataset+'_info'
    if not os.path.exists(infodir):
        os.makedirs(infodir)
        state=0  # empty   

    sep, cols=get_cols (datadir, dataset, infodir)


    g={'ND,1':'', 'ND,2':'', 'ND,3':'', 'ND,4':'', 'ND,5':'', 'ND,6':''}
    if action=='split':
        split_csv_file (datadir, dataset, infodir, match=None, global_recode=g)

    if action=='dictify':        
        dictify_all_the_things (infodir, cols)

    if action=='dictify':        
        dict2type (infodir, cols)


    if action=='clear_all':  # full clean
        if os.path.exists(infodir+'/split'):        
            shutil.rmtree(infodir+'/split')
        if os.path.exists(infodir+'/hist'):
            shutil.rmtree(infodir+'/hist')        
        os.remove(infodir+'/col_info.csv')
        msg='all cleared'
        sep, cols=get_cols (datadir, dataset, infodir) # kolommen opnieuw inlezen
        # rest als via init
 


    
    
    columns=[]
    for col in cols:
         columns.append({'colname':col, 'type':'--','label':'--','enabled':True})
        
        
        
    data={'dataset':dataset, 'sep':sep, 'columns':columns, 'msg':msg}
    return HttpResponse(cjson.encode(data))

