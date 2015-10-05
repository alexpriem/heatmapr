import os,sys, cjson, shutil, csv
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt

import csv_split
import dictify
import dict2type

import helpers
import plus.settings as settings



def view_data (request, dataset):

    template = loader.get_template('data.html')

    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


def view_dataconfig (request, dataset):

    infodir=helpers.get_infodir(dataset)
    dataconfig=helpers.read_configfile (infodir)
    defaults=cjson.encode(dataconfig)


    template = loader.get_template('data-config.html')
    context = RequestContext(request, {'defaults':defaults,'dataset':dataset})

    return HttpResponse(template.render(context))


def view_data_filter (request, dataset):

    infodir=helpers.get_infodir(dataset)
    filterset=helpers.read_filterfile (infodir)
    defaults=cjson.encode(filterset)

    template = loader.get_template('data-filter.html')
    context = RequestContext(request, {'defaults':defaults,'dataset':dataset})
    return HttpResponse(template.render(context))

def view_data_recode(request, dataset):

    infodir=helpers.get_infodir(dataset)
    recodedict, recodeset=helpers.read_recodefile (infodir)
    defaults=cjson.encode(recodeset)

    template = loader.get_template('data-recode.html')
    context = RequestContext(request, {'defaults':defaults,'dataset':dataset})

    return HttpResponse(template.render(context))












@csrf_exempt
def set_config (request, dataset):

    print 'set_config'
    datadir=settings.datadir
    enabled=request.POST.getlist('enabled[]')
    cols=request.POST.getlist('colnames[]')
    typehints=request.POST.getlist('typehint[]')
    formats=request.POST.getlist('format[]')

    print enabled, cols

    infodir=helpers.get_infodir(dataset)
    if not os.path.exists(infodir):
        os.makedirs(infodir)

    f=open (infodir+'/data_config.csv','wb')
    c=csv.writer(f, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
    c.writerow(['enabled','colname','typehint','format']);
    for enabled,col,typehint,format in zip(enabled, cols,typehints,formats):
        col=col.strip()
        enabled=enabled.strip()
        typehint=typehint.strip()
        format=format.strip()
        c.writerow([enabled,col,typehint,format])
    f.close()

    data={'msg':'saved config'}
    return HttpResponse(cjson.encode(data))





@csrf_exempt
def set_filter (request, dataset):

    datadir=settings.datadir
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
    
    data={'msg':'Recodes opgeslagen'}
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
    msg=''
        
    infodir=helpers.get_infodir(dataset)
    sep, cols=helpers.get_cols (datadir, dataset, infodir)
    enabled_cols=helpers.get_enabled_cols(infodir)

    if action=='split':
        csv_split.csv_select (datadir, dataset, infodir, sep)

    if action=='dictify':        
        dictify.dictify_all_the_things (infodir)

    if action=='dict2type':
        t=dict2type.typechecker()
        t.sep=sep
        t.cols=cols
        t.filename=dataset
        t.infodir=infodir

        t.update_num_records(t.cols[0])
        t.analyse(enabled_cols)


    if action=='clear_all':  # full clean
        if os.path.exists(infodir):
            shutil.rmtree(infodir)
        msg='all cleared'
        sep, cols=helpers.get_cols (datadir, dataset, infodir) # kolommen opnieuw inlezen


    # read labels, filter/recode-rules

    labels=helpers.read_csv_dict (infodir+'/labels.csv')
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
            if filter_set.get(info['datatype'])==False:
                continue

            column=info
            column['nr']=i+1
            column['enabled']=True
            column['label']=labels.get(col,'')
            columns.append(column)
            j+=1
            if j>=len(col_info):
                break

     
        
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

