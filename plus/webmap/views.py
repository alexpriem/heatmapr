import os,sys, cjson, shutil, csv
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt


from csv_split import csv_select
from dictify import dictify_all_the_things
from dict2type import typechecker
from makehist import make_hist2
import heatmap



# Create your views here.


def top (request):

    template = loader.get_template('top.html')

    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


@csrf_exempt
def make_heatmap (request, dataset):


    datadir='e:/data'
    infodir=datadir+'/'+dataset+'_info'
    if not os.path.exists(infodir):
        os.makedirs(infodir)
    if not os.path.exists(infodir+'/heatmaps'):
        os.makedirs(infodir+'/heatmaps')

    #print request.path
    #print request #.META
    defaults=dict(          
            sep=',',
          x_var='AR66',
          x_min=0,
          x_max=500000,
          x_steps=500,

          y_var='AR67',
          y_min=0,
          y_max=500000,
          y_steps=500,

          gradmin=0,
          gradmax=20,
          gradsteps=20
            )

    if request.is_ajax()==True:
        #print request.POST
        args={}    
        for k in defaults.keys():
            val=request.POST[k]
            try:
                v=float(val)                
                if v.is_integer():
                    args[k]=int(v)                    
                else:
                    args[k]=v                    
            except:                
                args[k]=val
        args['infodir']=infodir
        args['outfile']=args['x_var']+'_'+args['y_var']+'_0'
        print args
        h=heatmap.heatmap()
        h.make_heatmap(args)        
        data={'msg':'ok'}
        return HttpResponse(cjson.encode(data))
    #print dataset
    col_info, coltypes_bycol=get_col_types(infodir)
    #print col_info
    colnames=[]
    for col in col_info:
        if col['num_keys']>20:
            colnames.append(col['colname'])

    defaults_json=cjson.encode(defaults)
    template = loader.get_template('makemap.html')    
    context = RequestContext(request, {'colnames':colnames, 'dataset':dataset,'defaults':defaults,'defaults_json':defaults_json})
    return HttpResponse(template.render(context))



def serve_heatmap_js (request, dataset, path):

    datadir='e:/data'
    js_file='%s/%s_info/heatmaps/%s' % (datadir,dataset, path)
    print js_file
    f=open(js_file)
    txt=f.read()
    f.close()
    
    print 'filesize:', len(txt)
    return HttpResponse(txt, content_type='application/liquid')


def view_heatmaps (request, dataset):

    #print request.path
    #print request #.META
    
    #print dataset
    template = loader.get_template('heatmaps.html')
    datadir='e:/data'
    heatmapdir=datadir+'/'+dataset+'_info/heatmaps/'
    heatmapfiles=os.listdir(heatmapdir)
    heatmaps=[]
    for h in heatmapfiles:
        x,y,index=h.split('_')
        title='--'
        heatmaps.append({'x':x,'y':y,'title':title,'filename':h})
    args={'dataset':dataset,'heatmaps':heatmaps}
    
    context = RequestContext(request, args)
    return HttpResponse(template.render(context))


def view_heatmap(request, dataset, x_var, y_var, indexnr=None):

    #print request.path
    #print request #.META
    
    #print dataset
    if indexnr is None:
        indexnr=0
    template = loader.get_template('heatmap.html')
    datadir='e:/data'
    infodir=datadir+'/'+dataset+'_info'
    args={'dataset':dataset,'x_var':x_var,'y_var':y_var,'indexnr':indexnr,'infodir':infodir}
    context = RequestContext(request, args)
    return HttpResponse(template.render(context))


def view_data (request, dataset):

    #print request.path
    #print request #.META
    
    #print dataset
    template = loader.get_template('data.html')

    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


# helperfunction to read simple csv-file to a dict

def read_csvfile (filename):
    f=None
    try:
        f=open(filename)
    except:
        pass
    labels={}
    if f is not None:    
        c=csv.reader(f,delimiter=',')
        for line in c:
            labels[line[0]]=line[1]
        f.close()
    return labels


def read_filterfile (filename):
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


def read_recodefile (filename):
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



def get_col_types(infodir):
    f=None
    col_info=[]
    coltypes_bycol={}
    try:
        f=open(infodir+'/col_types.csv')
    except:
        pass
    if f is not None:
        f.readline()
        f.readline()
        int_cols=['num_keys','empty','unique_index',
              'float_t','int_t','str_t','int_min','int_max']
        float_cols=['float_min','float_max','min','max']
        bool_cols=['sparse1','sparse2','string_garbage','single_value','bi_value']
        c=csv.DictReader(f,delimiter=',')
        linenr=0
        for row in c:
          #  print line            
            for c in int_cols:
                try:
                    row[c]=int(float(row[c]))
                except:
                    row[c]=''
            for c in float_cols:
                try:
                    row[c]=float(row[c])
                except:
                    row[c]=''


            for c in bool_cols:
                if row[c]=='True':
                    row[c]=True
                if row[c]=='False':
                    row[c]=False
            row['colnr']=linenr
            col_info.append(row)
            colname=row['colname']
            coltypes_bycol[colname]=row
            linenr+=1
        f.close()


    return col_info,coltypes_bycol



def split_csv_file (datadir, dataset, infodir, match, global_recode):

    splitdir=infodir+'/split'
    if not os.path.exists(splitdir):
        os.makedirs(splitdir)        

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



def get_plot_alphanumeric (infodir,variable, rowinfo):

    print 'get_plot_alphanumeric'
    f=open(infodir+'/hists/%s.csv' % variable,'r')
    f.readline()
    c=csv.reader(f,delimiter=',')
    data=[]
    maxnum=0
    for row in c:
        x,num=row[0],row[1]
        try:
            x=float(x)
            if x.is_integer():
                x=int(x)
        except:
            pass
        num=int(num)
        if num>maxnum:
            maxnum=num
        data.append([x,num])
    f.close()
    rowinfo['data']=data

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
    print type(coltypes_bycol)
    print type(rowinfo)
    print 'get_plot:',variable

    try:
        print infodir+'/hista/%s.csv' % variable
        f=open(infodir+'/hista/%s.csv' % variable,'r')        
    except:
        return get_plot_alphanumeric(infodir, variable, rowinfo)

    # numerieke data
    
    f.readline()
    c=csv.reader(f,delimiter=':')
    plot=[]

    # FIXME: bijwerken met info uit coltypes
    minx,miny=c.next()    #  1st row contains minx, miny
    rowinfo['minx'], rowinfo['miny']=float(minx), float(miny)
    maxx,maxy=c.next()    #  2nd row contains maxx, maxy
    rowinfo['maxx'], rowinfo['maxy']=float(maxx), float(maxy)
    maxy2,maxy3=c.next()
    rowinfo['maxy2'], rowinfo['maxy3']=float(maxy2),float(maxy3)  #  2nd row contains maxx, maxy

    for row in c:
        x,num=row[0],row[1]
        x=float(x)
        if x.is_integer():
            x=int(x)
        num=int(num)
        plot.append([x,num])
    f.close()
    print variable+':[%d]' % (len(plot))
    rowinfo['data']=plot
    return rowinfo






@csrf_exempt
def histogram (request, dataset, variable):

    datadir='e:/data'
    infodir=datadir+'/'+dataset+'_info'
    if not os.path.exists(infodir):
        os.makedirs(infodir)    
    col_info, coltypes_bycol=get_col_types(infodir)
    rowinfo=coltypes_bycol[variable]

    if request.is_ajax()==True:
        cmd=request.GET['cmd']            
        if cmd=='reset':           
            rowinfo=get_plot(infodir, variable,col_info, coltypes_bycol)
            data={'action':'makeplot','data':rowinfo}  # plus histogram
        if cmd=='resize':
            minx=float(request.GET.get('minx',0))
            maxx=float(request.GET.get('maxx',100))
            bins=int(request.GET.get('bins',100))
            print 'RESIZE',minx,maxx,bins
            rowinfo=get_plot(infodir, variable,col_info, coltypes_bycol)
            rowinfo['minx']=minx
            rowinfo['maxx']=maxx

            
            histogram, sorted_hist=make_hist2 (infodir, variabele,minx,maxx,bins)
            plotdata['data']=histogram            
            rowinfo['maxy']=sorted_hist[-1]
            rowinfo['maxy2']=sorted_hist[-2]
            rowinfo['maxy3']=sorted_hist[-3]

            data={'action':'makeplot','data':plotdata}
        
        return HttpResponse(cjson.encode(data))

    template = loader.get_template('histogram.html')
    if not(rowinfo['datatype']=='char' and rowinfo['num_keys']>100):
        rowinfo=get_plot(infodir, variable,col_info, coltypes_bycol) # plus histogram

    colnr=rowinfo['colnr']
    prevvar=''
    if colnr>0:
        prevvar=col_info[colnr-1]['colname']
    nextvar=''
    if colnr<len(col_info):
        nextvar=col_info[colnr+1]['colname']

    print 'got rowinfo'
    histogram_json=cjson.encode(rowinfo)
    context = RequestContext(request, {'dataset':dataset,
                                       'prevcolname':prevvar,
                                       'colname':variable,
                                       'nextcolname':nextvar,
                                       'histogram':histogram_json})
    print 'got context'    
    return HttpResponse(template.render(context))


@csrf_exempt
def set_filter (request, dataset):

    print 'set_filter'
    datadir=request.POST['datadir']
    print request.POST.keys()
    cols=request.POST.getlist('filtercols[]')
    comps=request.POST.getlist('filtercompares[]')
    values=request.POST.getlist('filtervalues[]')

    
    infodir=datadir+'/'+dataset+'_info'    
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
    datadir=request.POST['datadir']
    print request.POST.keys()
    vals=request.POST.getlist('values[]')
    replacements=request.POST.getlist('replacements[]')
    
    infodir=datadir+'/'+dataset+'_info'    
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

    #print request.GET['dataset']
    action=request.GET['action']    
    datadir=request.GET['datadir']

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

    infodir=datadir+'/'+dataset+'_info'    
    if not os.path.exists(infodir):
        os.makedirs(infodir)

    sep, cols=get_cols (datadir, dataset, infodir)


    g={'ND,1':'', 'ND,2':'', 'ND,3':'', 'ND,4':'', 'ND,5':'', 'ND,6':''}
    if action=='split':
        split_csv_file (datadir, dataset, infodir, match=None, global_recode=g)

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

    labels=read_csvfile (infodir+'/labels.csv')
    filterdict, filterset=read_filterfile (infodir+'/filters.csv')
    recodedict, recodeset=read_recodefile (infodir+'/recodes.csv')
    
    # read types


    col_info, coltypes_bycol=get_col_types(infodir)

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
                msg='incomplete column list'
                break
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
          'action':action,
          'filters':filterset,
          'recodes':recodeset}
    
    return HttpResponse(cjson.encode(data))

