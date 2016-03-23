import os,sys, cjson, shutil, csv, glob
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt

import helpers, makehist, printer, heatmap
import plus.settings as settings



def expand_html (html, dataset):


    module_dir='..\\'
    newhtml=''
    cssfrags=html.split('<link href="')
    newhtml+=cssfrags[0]
   # cssfiles=[cssfrag.split('"')[0] for cssfrag in cssfrags[1:]]

    for cssfrag in cssfrags[1:]:
        cssfile=cssfrag.split('"')[0]
        print cssfile
        if cssfile=='/css/style_h1.css':
            continue   # skip css reset
        newhtml+='\n<style>\n'
        css=open(module_dir+'/'+cssfile,"r").read()
        newhtml+=css
        newhtml+='\n</style>\n'

    jsfrags=html.split('<script src="')
    for jsfrag in jsfrags[1:]:
        jsfile=jsfrag.split('"')[0]
        print jsfile
        newhtml+='\n<script type="text/javascript">\n'
        if ('js-data') in jsfile:
            print jsfile
            jsfile=jsfile.replace('/js-data/'+dataset,'e:\\data\\%s_info\\heatmaps' % dataset)

            js=open(jsfile,'r').read()
        else:
            js=open(module_dir+'\\'+jsfile,'r').read()

        newhtml+=js
        newhtml+='\n</script>\n'

    newhtml+="</head>\n"
    newhtml+="<body>\n"

    body=html.split("<body>")
    body=body[1]
    jsfrags=body.split('<script  src="')
    for jsfrag in jsfrags[1:]:
        jsfile=jsfrag.split('"')[0]
        js_end=jsfrag.split('\n')[0]

        js_txt='\n<script type="text/javascript">\n'
        js_txt+=open(module_dir+'/'+jsfile,'r').read()
        js_txt+='\n</script>\n'
      #  print js_txt
        body=jsfrags[0]+js_txt+jsfrags[1][len(js_end):]

    newhtml+=body

    return newhtml




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
    heatmapfiles=glob.glob(heatmapdir+'*.js')
    heatmaps=[]
    for h in heatmapfiles:        
        h=h[:-3]     # .js verwijderen
        h=h.split('\\')
        h=h[1]        
        parts=h.split('_')
        print parts
        if (len(parts)==4):  # meta / csv
            continue
        if (len(parts)==3):
            x,y,index=parts

        title='--'
        #print heatmapdir+h[:-3]+'_meta.csv'
        heatmapinfo=helpers.read_csv_dict(heatmapdir+h+'_meta.csv')
       # print heatmapinfo
        heatmaps.append({'x':x,'y':y,'index':index,
                         'title':title,
                         'filename':h,
                         'split1_var':heatmapinfo.get('split1_var',''),
                         'split2_var':heatmapinfo.get('split2_var','')})


    args={'dataset':dataset,'heatmaps':heatmaps}
    
    context = RequestContext(request, args)
    return HttpResponse(template.render(context))






@csrf_exempt
def view_heatmap(request, dataset, x_var, y_var, indexnr=None):

    print dataset
    if request.POST.get('print') is not None:
        print 'printing'
        p=printer.printert()
        filename=dataset+'_'+x_var+'_'+y_var
        url='/heatmap/'+filename
        p.do_print(url, filename,'png')
        data={'msg':'ok'}
        return HttpResponse(cjson.encode(data))

    return view__heatmap(request, dataset, x_var, y_var, indexnr, printert=False,publication=False)

@csrf_exempt
def print_heatmap(request, dataset, x_var, y_var, indexnr=None):

    print dataset
    if request.POST.get('print') is not None:
        print 'printing'
        p=printer.printert()
        filename=dataset+'_'+x_var+'_'+y_var
        url='/heatmap/'+filename
        p.do_print(url, filename,'png')
        data={'msg':'ok'}
        return HttpResponse(cjson.encode(data))

    return view__heatmap(request, dataset, x_var, y_var, indexnr, printert=True,publication=True)

@csrf_exempt
def view_pubmap(request, dataset, x_var, y_var, indexnr=None):

    print dataset
    if request.POST.get('print') is not None:
        print 'printing'
        p=printer.printert()
        filename=dataset+'_'+x_var+'_'+y_var
        url='/heatmap/'+filename
        p.do_print(url, filename,'png')
        data={'msg':'ok'}
        return HttpResponse(cjson.encode(data))

    return view__heatmap(request, dataset, x_var, y_var, indexnr, printert=False, publication=True)





def view__heatmap (request, dataset, x_var, y_var, indexnr, printert,publication=False):
    if indexnr is None:
        indexnr='0'

    infodir=settings.datadir+'/'+dataset+'_info'
    filename='%s_%s_%s' % (x_var, y_var, indexnr)
    args={'dataset':dataset,
          'x_var':x_var,
          'y_var':y_var,
          'filename':filename,
          'indexnr':indexnr,
          'infodir':infodir,
          'printing':printert}
    context = RequestContext(request, args)
    if publication==True:
        template = loader.get_template('pubmap.html')
    else:
        template = loader.get_template('heatmap.html')

    if request.POST.get('export') is not None:
        export_location='f:\\export_%s_%s_%s_%s.html' % (dataset, x_var, y_var, indexnr)
        print 'exporting to %s' % export_location
        html=template.render(context)

        newhtml=expand_html (html, dataset)
        f=open(export_location,'w')
        f.write(newhtml)
        f.close()


    return HttpResponse(template.render(context))





@csrf_exempt
def make_subsel(request, dataset):
    
    post=request.POST
    print post

    xvar=post['xvar']
    yvar=post['yvar']
    indexnr=int(post['heatmap_index'])
    num_annotaties=int(post['num_annotaties'])

    annotaties=[]
    for i in range(0,num_annotaties):
        a={}
        a['xvar']=xvar
        a['xmin']=float(post['xmin_%d' % i])
        a['xmax']=float(post['xmax_%d' % i])

        a['yvar']=yvar
        a['ymin']=float(post['ymin_%d' % i])
        a['ymax']=float(post['ymax_%d' % i])

        a['areatype']=post['areatype_%d' % i]
        a['indexnr']=int(post['heatmap_index'])
        a['connector_direction']=post['connector_direction_%d' % i]
        a['text_xpos']=post['text_xpos_%d' % i]
        a['text_ypos']=post['text_ypos_%d' % i]
        a['filename']=post['filename_%d' % i]
        a['txt']=post['txt_%d' % i]
        a['label']=post['label_%d' % i]
        annotaties.append(a)

    #print xvar,xmin,xmax
    #print yvar,ymin,ymax

    infodir=settings.datadir+'/'+dataset+'_info'

    print 'get_col_types'
    col_info, coltypes_bycol=helpers.get_col_types(infodir)
    selectiedir='%(infodir)s/selections/%(xvar)s_%(yvar)s_%(indexnr)s' % locals()

    print 'prepare_subsel'
    # duurt lang    , aparte optie voor maken om onderscheid tussen dataselectie en ui-selectie te maken
   # subsel=makehist.prepare_subsel (infodir, coltypes_bycol,  xvar,xmin,xmax, yvar,ymin,ymax)
   
    subsel=[]   
    print 'save_subsel'
    save_subsel (selectiedir, subsel, annotaties)

# bijwerken heatmap-javascript
    print 'bijwerken js'
    infile='%s_%s_%s' % (xvar, yvar, indexnr)
    h=heatmap.heatmap()
    h.infodir=infodir
    args=h.load_options_from_csv(infile)


    args['annotate']=annotaties
    for k,v in args.items():
        setattr(h,k,v)



    newjs=h.opties_to_js(args)
    f=open ('%s/heatmaps/%s_meta.js' %  (infodir, infile), 'w')
    newjs='var opties=[];\n'+newjs
    f.write(newjs)
    f.close()

    msg='ok'
    data={'msg':msg,'annotaties':annotaties}

    return HttpResponse(cjson.encode(data))




def save_subsel (selectiedir, subsel, annotaties):


    if not os.path.exists(selectiedir):
        os.makedirs(selectiedir)
        selnr=1
    else:
        try:
            selections=helpers.read_csv_list ('%s/meta.csv' % selectiedir)
            selnr=len(selections)+1
        except:
            selnr=1

    print 'save_subsel, selnr:', selnr    
    f=open('%s/ssel_%d.csv' % (selectiedir, selnr),'wb')
    for i in subsel:
        f.write('%d\n' % i )
    f.close()

    f=open('%s/meta2.csv' % selectiedir,'ab')
    c=csv.writer(f)
    for selnr, a in enumerate(annotaties):
        meta=[selnr, a['xvar'], a['xmin'],a['xmax'],
                     a['yvar'],a['ymin'],a['ymax'],
                      a['connector_direction'],
                      a['text_xpos'],a['text_ypos'],
                      a['label'],a['filename']]
        c.writerow(meta)
        g=open('%s/%s.txt' % (selectiedir, a['filename']),'w')
        g.write(a['txt'])
        g.close()
        
    f.close()



#    sel_js='%s/meta.js' % selectiedir
#    if os.path.isfile(sel_js):
#        f=open(sel_js, 'ab')
#    else:
#        f=open(sel_js,'w')
#        f.write('var annotations=[];\n')
#
#    meta="annotations.push({area:[[%(xmin)s, %(ymin)s],[%(xmax)s,%(ymax)s]],text_xpos:%(text_xpos)s, text_ypos:%(text_ypos)s, text:'%(txt)s',xvar:'%(xvar)s', yvar:'%(yvar)s', label:'%(label)s'});\n" % locals()
#    f.write(meta)
#    f.close()




# inladen van id's van subselectie

def load_subsel (infodir, subselnr):

     f=open('%s/selections/sel_%d.csv' % (infodir, selnr),'r')
     subsel=[int(line) for line in f]
     f.close()

     return subsel


@csrf_exempt
def make_histogram (request, dataset):

    varname=request.POST.get('histogram_var')
    part=request.POST.get('histogram_part')
    partvalue=request.POST.get('histogram_partvalue')
    print 'make_histogram', varname, part, partvalue
    msg='ok'
    data={'msg':msg}
    return HttpResponse(cjson.encode(data))


