import os,sys, cjson, shutil, csv
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt


from csv_split import csv_select
from dictify import dictify_all_the_things
from dict2type import typechecker
from makehist import make_hist3, get_data, check_binsize
from helpers import get_col_types, read_csvfile
import heatmap


colormapnames=['blue','gray','cbs_blue','cbs_green','cbs_red','cbs_hot','terrain','coolwarm','hot','hot2','ygb']


def get_colnames_for_heatmap (infodir, heatmaptype, col_info):
        min_bins={'heatmap':50,'dotplot':2,'text':2}
        max_bins={'heatmap':1000,'dotplot':25,'text':25}

        bins_required=min_bins[heatmaptype]
        colnames=[]
        groupcolnames=[]
        for col in col_info:
            if (col['datatype']!='char') and (col['num_keys']>bins_required):
                colnames.append(col['colname'])
            if (col['num_keys']<20) and col['num_keys']>(1+col['empty']):
                groupcolnames.append(col['colname'])
        return colnames, groupcolnames




@csrf_exempt
def make_heatmap (request, dataset, x_var=None, y_var=None):

    datadir='e:/data'
    infodir=datadir+'/'+dataset+'_info'
    if not os.path.exists(infodir):
        os.makedirs(infodir)
    if not os.path.exists(infodir+'/heatmaps'):
        os.makedirs(infodir+'/heatmaps')

    col_info, coltypes_bycol=get_col_types(infodir)
   # print col_info
    # args['displaymode'] uit post peuteren.
    colnames, groupcolnames=get_colnames_for_heatmap (infodir,  'heatmap', col_info)
    if len(colnames)<2:
        msg='Geen heatmaps te maken van deze dataset'
        template = loader.get_template('makemap.html')
        context = RequestContext(request, {'msg':'msg','colnames':colnames, 'dataset':dataset})
        return HttpResponse(template.render(context))



    if request.is_ajax()==True:
        #print request.POST
        args={}
        cmd=request.POST['cmd']
        for key, val in request.POST.iteritems():
            if key=='cmd':
                continue
            try:
                v=float(val)                
                if v.is_integer():
                    args[key]=int(v)
                else:
                    args[key]=v
            except:                
                args[key]=val

        print 'x x y:',args['imgheight'], args['imgwidth']
        if cmd=='update':
            col_info, coltypes_bycol=get_col_types(infodir)
            colnames,groupcolnames=get_colnames_for_heatmap (infodir, args['displaymode'], col_info)
            data={'msg':'','colnames':colnames,'groupcolnames':groupcolnames}

        if cmd=='makemap':
            msg='ok'
            args['infodir']=infodir
            args['outfile']=args['x_var']+'_'+args['y_var']+'_0'
            x_types=coltypes_bycol[args['x_var']]   # info van variabelenaam x-kolom ophalen
            y_types=coltypes_bycol[args['y_var']]

            args['x_min']=x_types.get(args['x_min'],args['x_min'])
            args['y_min']=y_types.get(args['y_min'],args['y_min'])
            args['x_max']=x_types.get(args['x_max'],args['x_max'])
            args['y_max']=y_types.get(args['y_max'],args['y_max'])


            imgwidth=float(args['imgwidth'])
            imgheight=float(args['imgheight'])
            x_steps=int(args['x_steps'])
            y_steps=int(args['y_steps'])

            if not (imgwidth/4.0).is_integer():
                msg='imgwidth moet veelvoud van 4 zijn'
            if not (imgheight/4.0).is_integer():
                msg='imgheight moet veelvoud van 4 zijn'
            if x_steps>200 and not (x_steps/4.0).is_integer():
                msg='xsteps moet veelvoud van 4 zijn'
            if y_steps>200 and not (y_steps/4.0).is_integer():
                msg='ysteps moet veelvoud van 4 zijn'


               # print args['x_steps'],args['y_steps']
            print args['x_min'], args['x_max'], args['y_min'],args['y_max']
            if msg=='ok':
                h=heatmap.heatmap()
                h.make_heatmap(args)
            data={'msg':msg}
        return HttpResponse(cjson.encode(data))

    args=dict(
            sep=',',
            x_min='perc01',
            x_max='max',
            x_steps=500,

            y_min='perc01',
            y_max='max',
            y_steps=500,

            split1_var='AR19',
            split2_var='',
            gradmin=0,
            gradmax='max',
            gradsteps=20,
            colormap=colormapnames[0],

            displaymode='heatmap',
            imgwidth=500,
            imgheight=500
            )

    if x_var is None:
        args['x_var']=colnames[0]
    else:
        args['x_var']=str(x_var)

    if y_var is None:
        args['y_var']=colnames[1]
    else:
        args['y_var']=str(y_var)



    x_types=coltypes_bycol[args['x_var']]   # info van variabelenaam x-kolom ophalen
    y_types=coltypes_bycol[args['y_var']]

    args['x_min']=x_types.get(args['x_min'],args['x_min'])
    args['y_min']=y_types.get(args['y_min'],args['y_min'])
    args['x_max']=x_types.get(args['x_max'],args['x_max'])
    args['y_max']=y_types.get(args['y_max'],args['y_max'])


    x_min=args['x_min']
    x_max=args['x_max']
    y_min=args['y_min']
    y_max=args['y_max']
    dy=y_max-y_min
    steps_set=False
    if dy>20 and dy<150:
        steps_set=True
        args['y_steps']=dy
        args['x_steps']=dy
        if dy<70:
            args['imgheight']=8*dy
            args['imgwidth']=8*dy
        else:
            args['imgheight']=4*dy
            args['imgwidth']=4*dy
    if (steps_set==False) and (dx>20 and dx<150):
        steps_set=True
        args['y_steps']=dx
        args['x_steps']=dx
        if dx<70:
            args['imgheight']=8*dx
            args['imgwidth']=8*dx
        else:
            args['imgheight']=4*dx
            args['imgwidth']=4*dx

    if steps_set==False:
        xkeys=args['x_steps']       # autorange steps op aantal keys
        setkeys=False
        x_types=coltypes_bycol[args['x_var']]   # info van variabelenaam x-kolom ophalen
        y_types=coltypes_bycol[args['y_var']]
        if x_types['num_keys']<args['x_steps']:
            xkeys=x_types['num_keys']
            setkeys=True
        ykeys=args['y_steps']
        if y_types['num_keys']<args['y_steps']:
            ykeys=y_types['num_keys']
            setkeys=True
        if setkeys:
            keys=xkeys
            if ykeys<xkeys:
                keys=ykeys

            width=args['imgwidth']
            stepsizes=[]
            for i in range(50,0,-1):
                if (width/(i*1.0))==int(width/i):
                    stepsizes.append(int(width/i))

            prevk=stepsizes[0]
            for k in stepsizes[1:]:
                if keys<k:
                    keys=prevk
                    break
                prevk=k
            args['x_steps']=keys
            args['y_steps']=keys

    labels=read_csvfile (infodir+'/labels.csv')
    col_x=x_types['colname']
    col_y=y_types['colname']
    args['x_label']=labels.get(col_x,col_x)
    args['y_label']=labels.get(col_y,col_y)
    args['title']=labels.get(col_x,col_x)+' vs '+labels.get(col_y,col_y)

    print args['y_steps']
    args_json=cjson.encode(args)
    template = loader.get_template('makemap.html')    
    context = RequestContext(request, {'colnames':colnames,
                                       'groupcolnames':groupcolnames,
                                       'dataset':dataset,
                                       'defaults':args,'defaults_json':args_json,
                                       'colormapnames':colormapnames})
    return HttpResponse(template.render(context))

