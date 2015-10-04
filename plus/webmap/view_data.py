import os,sys, cjson, shutil, csv
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt


import csv_split
from dictify import dictify_all_the_things
from dict2type import typechecker

import helpers
import plus.settings as settings



def view_data (request, dataset):

    template = loader.get_template('data.html')

    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


def view_dataconfig (request, dataset):

    infodir=helpers.get_infodir(dataset)
    dataconfig=read_configfile (infodir)
    defaults=cjson.encode(dataconfig)

    template = loader.get_template('data-config.html')
    context = RequestContext(request, {'defaults':defaults,'dataset':dataset})

    return HttpResponse(template.render(context))


def view_data_filter (request, dataset):

    infodir=helpers.get_infodir(dataset)
    filterdict, filterset=read_filterfile (infodir)
    defaults=cjson.encode(filterset)

    template = loader.get_template('data-filter.html')
    context = RequestContext(request, {'defaults':defaults,'dataset':dataset})
    return HttpResponse(template.render(context))

def view_data_recode(request, dataset):

    infodir=helpers.get_infodir(dataset)
    recodedict, recodeset=read_recodefile (infodir)
    defaults=cjson.encode(recodeset)

    template = loader.get_template('data-recode.html')
    context = RequestContext(request, {'defaults':defaults,'dataset':dataset})

    return HttpResponse(template.render(context))





def read_configfile (infodir):

    #config=helpers.read_csv_file()
    f=open(infodir+'/data_config.csv')
    config=helpers.read_csv_file (infodir+'/data_config.csv')

    try:
        f=open(filename)
    except:
        pass
    print f
    if f is not None:
        c=csv.DictReader(f,delimiter=',')
        for line in c:
            config.append(line)
  #  config=[]
    return config


def read_filterfile (infodir):

    filename=infodir+'/filters.csv'
    f=None
    try:
        f=open(filename)
    except:
        pass
    matchui=[]
    matches=[]
    if f is not None:
        c=csv.DictReader(f,delimiter=',')
        for line in c:
            if len(line)==3:
                matchui.append(line)
                matches.append(line['key']+line['compare']+str(line['value']))
        f.close()
    return matches, matchui


def read_recodefile (infodir):

    filename=infodir+'/recodes.csv'
    f=None
    try:
        f=open(filename)
        f.readline()
    except:
        pass

    labelset=[]
    labeldict={}
    if f is not None:
        c=csv.reader(f,delimiter=',')
        for line in c:
            if len(line)==2:
                labelset.append({'value':line[0],'replacement':line[1]})
                labeldict[line[0]]=line[1]
        f.close()
    return labeldict,labelset






def split_csv_file (datadir, dataset, infodir, sep, match, global_recode):

    splitdir=infodir+'/split'
    if not os.path.exists(splitdir):
        os.makedirs(splitdir)        

    infile=datadir+'/'+dataset+'.csv'
    outfile=infodir+'/split/'
#        match=[]    # ['srtadr=1','h_ink=1']

    csv_split.csv_select (infile, outfile, sep, match, global_recode)











@csrf_exempt
def set_filter (request, dataset):

    print 'set_filter'
    datadir=settings.datadir
    print request.POST.keys()
    cols=request.POST.getlist('filtercols[]')
    comps=request.POST.getlist('filtercompares[]')
    values=request.POST.getlist('filtervalues[]')

    
    infodir=helpers.get_infodir(dataset)
    if not os.path.exists(infodir):
        os.makedirs(infodir)    

    f=open (infodir+'/filter.csv','wb')
    c=csv.writer(f, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)    
    c.writerow(['key','compare','value']);
    for col,comp,value in zip(cols,comps,values):        
        col=col.strip()
        comp=comp.strip()
        value=value.strip()
        if (col!='') and (comp in ['=','<','>', '<=','>=','!=']):
            c.writerow([col,comp,value])
    f.close()
    
    data={'msg':''}
    return HttpResponse(cjson.encode(data))


@csrf_exempt
def set_recode (request, dataset):

    print 'set_recode'
    datadir=settings.datadir
    print request.POST.keys()
    vals=request.POST.getlist('values[]')
    replacements=request.POST.getlist('replacements[]')
    
    infodir=helpers.get_infodir(dataset)
    if not os.path.exists(infodir):
        os.makedirs(infodir)    

    f=open (infodir+'/recodes.csv','wb')
    c=csv.writer(f, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
    c.writerow(['value','replacement']);
    for val,replacement in zip(vals,replacements):        
        val=val.strip()        
        replacement=replacement.strip()
        if (val!=''):
            c.writerow([val,replacement])
    f.close()
    
    data={'msg':''}
    return HttpResponse(cjson.encode(data))
        


@csrf_exempt
def dataset (request, dataset):
    
    action=request.GET.get('action')
    datadir=settings.datadir

    filter_set={}
    for k in request.GET.keys():        
        if k[:7]=='filter_':
            val=request.GET[k]
            if val=='true':
                filter_set[k[7:]]=True
            else:
                filter_set[k[7:]]=False
    #print filter_set
    msg=''
        

    # kijken of info-dir bestaat

    infodir=helpers.get_infodir(dataset)

    sep, cols=helpers.get_cols (datadir, dataset, infodir)



    if action=='split':
        matches, matchui=read_filterfile(infodir)
        recodes, recodeset=read_recodefile (infodir)
        split_csv_file (datadir, dataset, infodir, sep, match=matches, global_recode=recodes)

    if action=='dictify':        
        dictify_all_the_things (infodir, cols)

    if action=='dict2type':
        t=typechecker()
        t.sep=sep
        t.cols=cols
        t.filename=dataset
        t.infodir=infodir
        t.update_num_records(t.cols[0])
        t.analyse()                


    if action=='clear_all':  # full clean
        if os.path.exists(infodir+'/split'):        
            shutil.rmtree(infodir+'/split')
        if os.path.exists(infodir+'/hist'):
            shutil.rmtree(infodir+'/hist')
        if os.path.exists(infodir+'/splitbin'):        
            shutil.rmtree(infodir+'/splitbin')
        if os.path.exists(infodir+'/histo'):
            shutil.rmtree(infodir+'/histo') 
        os.remove(infodir+'/col_info.csv')
        msg='all cleared'
        sep, cols=get_cols (datadir, dataset, infodir) # kolommen opnieuw inlezen
        # rest als via init
 


    # read labels, filter/recode-rules

    labels=helpers.read_csv_dict (infodir+'/labels.csv')

    # read types


    col_info, coltypes_bycol=helpers.get_col_types(infodir)

    have_col_info= (len(col_info)>0)
    

      
    j=0
    columns=[]

    if not(have_col_info):
        for i,col in enumerate(cols):
            column={}
            column['nr']=i+1
            column['colname']=col
            column['enabled']=True
            column['label']=labels.get(col,'')            
            columns.append(column)
        
    col_info_length=len(col_info)
    if have_col_info:
        for i,col in enumerate(cols):   # aantal cols >=aantal cols in col_type.csv
            info=col_info[j]
          #  print col
            if (col!=info['colname']):
                continue
            j+=1
            if j>=col_info_length:
                msg='incomplete column list: (%d/%d/%d)' % (i,j,col_info_length)
              #  break
            if filter_set.get(info['datatype'])==False:
                continue

            column=info
            column['nr']=i+1
            column['enabled']=True
            column['label']=labels.get(col,'')
            columns.append(column)
     
        
    if action=='makeplot':        
        for i,rowinfo in enumerate(columns):            
            rowinfo=get_plot(infodir, rowinfo)
            columns[i]=rowinfo


    data={'dataset':dataset,
          'sep':sep,
          'columns':columns,
          'msg':msg,
          'action':action}
    
    return HttpResponse(cjson.encode(data))

