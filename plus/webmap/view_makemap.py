import os,sys, cjson, shutil, csv, ast, glob
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt

import helpers
import heatmap
import plus.settings as settings

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
            if (col['num_keys']<20) and col['num_keys']>(1+col['missing']):
                groupcolnames.append(col['colname'])
        return colnames, groupcolnames


def get_all_colnames (infodir, heatmaptype, col_info):
    colnames=[]
    for col in col_info:
        colnames.append(col['colname'])
    return colnames, colnames




@csrf_exempt
def make_heatmap (request):

    print 'make_heatmap'
    if request.is_ajax()==True:
        args={}
        cmd=request.POST['cmd']
        dataset=request.POST['dataset']
        infodir=helpers.get_infodir(dataset)

        # overzetten van waardes uit POST naar args-dict.
        for key, val in request.POST.iteritems():
            if key=='cmd' or key=='dataset':
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
            col_info, coltypes_bycol=helpers.get_col_types(infodir)
            colnames,groupcolnames=get_colnames_for_heatmap (infodir, args['displaymode'], col_info)
            data={'msg':'','colnames':colnames,'groupcolnames':groupcolnames}

        if cmd=='makemap':
            msg='ok'

            col_info, coltypes_bycol=helpers.get_col_types(infodir)
            new_heatmap=args.get('add_new_heatmap',u'true')            
            if new_heatmap==u'true':
                add_new_heatmap=True
            else:
                add_new_heatmap=False

            print 'add new heatmap:', new_heatmap, add_new_heatmap
            indexnr=args.get('heatmap_indexnr','0')
            print 'INDEXNR',indexnr, type(indexnr)
            args['infodir']=infodir
            if add_new_heatmap:
                print 'add new heatmap'
                filename='%(infodir)s\heatmaps\%(x_var)s_%(y_var)s_meta.js' % args
                print filename
                heatmaps=glob.glob(filename)
                print heatmaps
                indexnr=len(heatmaps)

            print 'indexnr:', indexnr

            args['heatmap_indexnr']=indexnr
            outfile='%(x_var)s_%(y_var)s_%(heatmap_indexnr)s' % args
            
            args['outfile']=outfile
            print coltypes_bycol.keys()[:10]
            x_types=coltypes_bycol[args['x_var']]   # info van variabelenaam x-kolom ophalen
            y_types=coltypes_bycol[args['y_var']]

   #         args['x_min']=x_types.get(args['x_min'],args['x_min'])
  #          args['y_min']=y_types.get(args['y_min'],args['y_min'])
 #           args['x_max']=x_types.get(args['x_max'],args['x_max'])
#            args['y_max']=y_types.get(args['y_max'],args['y_max'])

            for key,value in args.items():
                if value=='true':
                    value=True
                    args[key]=value
                    continue
                if value=='false':
                    value=False
                    args[key]=value
                    continue
                try:
                    value=ast.literal_eval(value)
                except:
                    pass
                args[key]=value



            # kijk of we een nieuwe heatmap moeten uitrekenen
            data={'msg':msg, 'heatmap_index':indexnr,
                  'x_var':args['x_var'],'y_var':args['y_var']}
            
            do_recalc=True
            h=heatmap.heatmap()
            h.check_args(args)
            print add_new_heatmap
            if add_new_heatmap==False:
                
                csvfile='%(infodir)s\heatmaps\%(x_var)s_%(y_var)s_%(heatmap_indexnr)s_meta' % args
                old_args=h.load_options_from_csv(csvfile+'.csv')

                do_not_recalc_args=['x_label', 'y_label',
                                    'gradmin','gradmax','gradsteps',
                                    'colormap','title', 'do_recalc',
                                    'plot_mean', 'plot_mean_pixelsize', 'plot_mean_color',
                                    'plot_median', 'plot_median_pixelsize', 'plot_median_color']
                changed=False
                do_recalc=False
                print args['plot_mean'], old_args['plot_mean']
                old_args['do_recalc']=False
                new_args=old_args.copy()
                for k,v in args.items():
                    new_args[k]=v
                    if old_args[k]!=args[k]:
                        new_args[k]=args[k]
                        print 'veranderd:%s, %s->%s' % ( k,old_args[k],args[k])
                        changed=True
                        if not(k in do_not_recalc_args):
                            do_recalc=True                        
                if not changed:
                    return HttpResponse(cjson.encode(data))
                if do_recalc==False:
                    optiejs=h.opties_to_js(new_args)
                    f=open(csvfile+'.js','w')
                    f.write ('var opties=[];\n');
                    f.write(optiejs)
                    f.close()
                    
                    h.save_options_to_csv(new_args, csvfile+'.csv')
                    return HttpResponse(cjson.encode(data))
                
            args['do_recalc']=do_recalc
            
            h.make_heatmap(args)
            
            
        return HttpResponse(cjson.encode(data))

    # shouldn't get here

    return HttpResponse('')



@csrf_exempt
def show_heatmap_form (request, dataset, x_var=None, y_var=None):

    infodir=helpers.get_infodir(dataset)
    if not os.path.exists(infodir):
        os.makedirs(infodir)
    if not os.path.exists(infodir+'/heatmaps'):
        os.makedirs(infodir+'/heatmaps')

    col_info, coltypes_bycol=helpers.get_col_types(infodir)

    # args['displaymode'] uit post peuteren.
    colnames, groupcolnames=get_colnames_for_heatmap (infodir,  'heatmap', col_info)
    colnames, groupcolnames=get_all_colnames (infodir,  'heatmap', col_info)
    #print 'colnames:', len(colnames), colnames
    if len(colnames)<2:
        msg='Geen heatmaps te maken van deze dataset'
        template = loader.get_template('makemap.html')
        context = RequestContext(request, {'msg':'msg','colnames':colnames, 'dataset':dataset})
        return HttpResponse(template.render(context))



    h=heatmap.heatmap()

    args={}
    for defaultval in h.defaults:
        args[defaultval[0]]=defaultval[1]



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

    print 'xmin/xmax:',args['x_min'],args['x_max']
    x_min=float(args['x_min'])
    x_max=float(args['x_max'])
    y_min=float(args['y_min'])
    y_max=float(args['y_max'])
    dx=x_max-x_min
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

    labels=helpers.read_csv_dict (infodir+'/labels.csv')
    col_x=x_types['colname']
    col_y=y_types['colname']
    args['x_label']=labels.get(col_x,col_x)
    args['y_label']=labels.get(col_y,col_y)
    args['title']=labels.get(col_x,col_x)+' vs '+labels.get(col_y,col_y)

    filename='%(infodir)s\heatmaps\%(x_var)s_%(y_var)s_*meta.js' % locals()
    heatmaps=glob.glob(filename)
    add_new_heatmap=False
    if len(heatmaps)>0:
        add_new_map=True
    heatmap_indexnr=len(heatmaps)
    args['heatmap_indexnr']=heatmap_indexnr

    args_json=cjson.encode(args)
    defaults_json=args_json.replace('False','false').replace('True','true')


    template = loader.get_template('makemap.html')    
    context = RequestContext(request, {'colnames':colnames,
                                       'add_new_heatmap':add_new_heatmap,
                                       'groupcolnames':groupcolnames,
                                       'dataset':dataset,
                                       'defaults_json':args_json,
                                       'simple_vars':h.simple_vars,
                                       'no_rebuild':h.no_rebuild,
                                       'booleans':h.booleans,
                                       'colormapnames':colormapnames})
    return HttpResponse(template.render(context))








@csrf_exempt
def edit_heatmap (request, dataset, filename):

    infodir=helpers.get_infodir(dataset)
    if not os.path.exists(infodir+'/heatmaps'):
        os.makedirs(infodir+'/heatmaps')


    args=helpers.read_csv_dict('%s/heatmaps/%s_meta.csv' % (infodir,filename))
    print '%s/heatmaps/%s_meta.csv' % (infodir, filename)

    h=heatmap.heatmap()

    col_info, coltypes_bycol=helpers.get_col_types(infodir)
    colnames,groupcolnames=get_colnames_for_heatmap (infodir, args.get('displaymode','heatmap'), col_info)

    template = loader.get_template('makemap.html')
    args_json=cjson.encode(args)
    context = RequestContext(request, {'colnames':colnames,
                                       'add_new_heatmap':True,
                                       'groupcolnames':groupcolnames,
                                       'dataset':dataset,
                                       'defaults_json':args_json,
                                       'simple_vars':h.simple_vars,
                                       'no_rebuild':h.no_rebuild,
                                       'booleans':h.booleans,
                                       'colormapnames':colormapnames})

    return HttpResponse(template.render(context))
