import os,sys, cjson, shutil, csv
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from csv_split import csv_select
from dictify import dictify_all_the_things
from dict2type import typechecker
from makehist import make_hist



# Create your views here.


def top (request):

    template = loader.get_template('top.html')

    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

    

def heatmap (request, dataset):

    #print request.path
    #print request #.META
    
    #print dataset
    template = loader.get_template('data.html')

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




def get_plot (infodir, rowinfo):

    variable=rowinfo['colname']
    try:
        f=open(infodir+'/hista/%s.csv' % variable,'r')
    except:
        print variable+':[]'
        rowinfo['data']=[]
        return rowinfo
    f.readline()
    c=csv.reader(f,delimiter=':')
    plot=[]
            
    rowinfo['minx'], rowinfo['miny']=c.next()    #  1st row contains minx, miny
    rowinfo['maxx'], rowinfo['maxy']=c.next()    #  2nd row contains maxx, maxy
    rowinfo['maxy2'], rowinfo['maxy3']=c.next()    #  2nd row contains maxx, maxy
    
   
    for row in c:        
        plot.append([row[0],row[1]])
    f.close()
    print variable+':[%d]' % (len(plot))
    rowinfo['data']=plot
    return rowinfo


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
        state=0  # empty   

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
 


    # read labels

    f=None
    try:
        f=open(infodir+'/labels.csv')
    except:
        pass
    labels={}
    if f is not None:    
        c=csv.reader(f,delimiter=',')
        for line in c:
            labels[line[0]]=line[1]
        f.close()
                
    # read types

    f=None
    col_info=[]
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
        c=csv.DictReader(f,delimiter=',')        
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
            row['sparse1']=False                    
            if row['sparse1']=='True':
                row['sparse1']=True
            row['sparse2']=False                    
            if row['sparse2']=='True':
                row['sparse2']=True            
                
            col_info.append(row)

    have_col_info= (len(col_info)>0)
    
    # sorthist kan pas als je types van kolommen hebt
    # 

    if action=='sorthist' and len(col_info)>0:
        for col in cols:
            make_hist(infodir, col)
            
      
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

        
    data={'dataset':dataset, 'sep':sep, 'columns':columns, 'msg':msg, 'action':action}
    return HttpResponse(cjson.encode(data))

