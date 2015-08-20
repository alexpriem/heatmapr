import os,sys, cjson, shutil, csv
from django.http import HttpResponse
from django.template import RequestContext, loader

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
        if (len(parts)==4):
            continue
        if (len(parts)==3):
            x,y,index=parts

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
    infodir=settings.datadir+'/'+dataset+'_info'
    args={'dataset':dataset,'x_var':x_var,'y_var':y_var,'indexnr':indexnr,'infodir':infodir}
    context = RequestContext(request, args)
    return HttpResponse(template.render(context))

