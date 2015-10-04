import os,sys, cjson, shutil, csv
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt

import helpers, makehist
import plus.settings as settings



def get_colnames_for_heatmap (infodir, heatmaptype, col_info):
        min_bins={'heatmap':50,'dotplot':2,'text':2}
        max_bins={'heatmap':1000,'dotplot':25,'text':25}

        bins_required=min_bins[heatmaptype]
        colnames=[]
        for col in col_info:
            if (col['datatype']!='char') and (col['num_keys']>bins_required):
                colnames.append(col['colname'])
        return colnames






def serve_heatmap_js (request, dataset, path):

    js_file='%s/%s_info/heatmaps/%s' % (settings.datadir,dataset, path)
    print js_file
    f=open(js_file)
    txt=f.read()
    f.close()
    
    print 'filesize:', len(txt)
    return HttpResponse(txt, content_type="application/x-javascript")


def view_heatmaps (request, dataset):

    #print request.path
    #print request #.META
    
    #print dataset
    template = loader.get_template('heatmaps.html')

    heatmapdir=settings.datadir+'/'+dataset+'_info/heatmaps/'
    if not os.path.exists(heatmapdir):
        os.makedirs(heatmapdir)  
    heatmapfiles=os.listdir(heatmapdir)
    heatmaps=[]
    for h in heatmapfiles:
        parts=h.split('_')
        if (len(parts)==4):  # meta / csv
            continue
        if (len(parts)==3):
            x,y,index=parts


        title='--'
        #print heatmapdir+h[:-3]+'_meta.csv'
        heatmapinfo=helpers.read_csv_dict(heatmapdir+h[:-3]+'_meta.csv')
       # print heatmapinfo
        heatmaps.append({'x':x,'y':y,'title':title,'filename':h,'split1_var':heatmapinfo.get('split1_var',''), 'split2_var':heatmapinfo.get('split2_var','')})


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
    infodir=settings.datadir+'/'+dataset+'_info'
    filename='%s_%s_%d' % (x_var, y_var, indexnr)
    args={'dataset':dataset,
          'x_var':x_var,
          'y_var':y_var,
          'filename':filename,
          'indexnr':indexnr,
          'infodir':infodir}
    context = RequestContext(request, args)
    return HttpResponse(template.render(context))

@csrf_exempt
def make_subsel(request, dataset):

    xvar=request.POST['xvar']
    xmin=float(request.POST['xmin'])
    xmax=float(request.POST['xmax'])

    yvar=request.POST['yvar']
    ymin=float(request.POST['ymin'])
    ymax=float(request.POST['ymax'])
    if ymin>ymax:
        ymax,ymin=ymin,ymax

    print xvar,xmin,xmax
    print yvar,ymin,ymax

    infodir=settings.datadir+'/'+dataset+'_info'

    col_info, coltypes_bycol=helpers.get_col_types(infodir)
    makehist.prepare_subselection(infodir, coltypes_bycol,  xvar,xmin,xmax, yvar,ymin,ymax,)
    msg='ok'
    data={'msg':msg}

    return HttpResponse(cjson.encode(data))