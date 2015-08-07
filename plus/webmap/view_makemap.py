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




def get_colnames_for_heatmap (infodir, heatmaptype, col_info):
        min_bins={'heatmap':50,'dotplot':2,'text':2}
        max_bins={'heatmap':1000,'dotplot':25,'text':25}

        bins_required=min_bins[heatmaptype]
        colnames=[]
        for col in col_info:
            if (col['datatype']!='char') and (col['num_keys']>bins_required):
                colnames.append(col['colname'])
        return colnames




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
          x_min='perc01',
          x_max='max',
          x_steps=500,

          y_min='perc01',
          y_max='max',
          y_steps=500,

          gradmin=0,
          gradmax=20,
          gradsteps=20,
          displaymode='heatmap'
            )

    col_info, coltypes_bycol=get_col_types(infodir)
   # print col_info
    colnames=get_colnames_for_heatmap (infodir,  defaults['displaymode'], col_info)
    if len(colnames)<2:
        msg='Geen heatmaps te maken van deze dataset'
        context = RequestContext(request, {'msg':'msg','colnames':colnames, 'dataset':dataset})
        return HttpResponse(template.render(context))


    defaults['x_var']=colnames[0]
    defaults['y_var']=colnames[1]
    if request.is_ajax()==True:
        #print request.POST
        args={}
        cmd=request.POST['cmd']
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

        if cmd=='update':
            col_info, coltypes_bycol=get_col_types(infodir)
            colnames=get_colnames_for_heatmap (infodir, args['displaymode'], col_info)
            data={'msg':'','colnames':colnames}

        if cmd=='makemap':
            args['infodir']=infodir
            args['outfile']=args['x_var']+'_'+args['y_var']+'_0'
            x_types=coltypes_bycol[args['x_var']]
            y_types=coltypes_bycol[args['y_var']]
            args['x_min']=x_types.get(args['x_min'],args['x_min'])
            args['y_min']=x_types.get(args['y_min'],args['y_min'])
            args['x_max']=x_types.get(args['x_max'],args['x_max'])
            args['y_max']=x_types.get(args['y_max'],args['y_max'])


            print args['x_min'],args['x_max'],args['y_min'],args['y_max']
            h=heatmap.heatmap()
            h.make_heatmap(args)
            data={'msg':'ok'}
        return HttpResponse(cjson.encode(data))

    defaults_json=cjson.encode(defaults)
    template = loader.get_template('makemap.html')    
    context = RequestContext(request, {'colnames':colnames, 'dataset':dataset,'defaults':defaults,'defaults_json':defaults_json})
    return HttpResponse(template.render(context))

