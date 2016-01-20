import os,sys, cjson, shutil, csv, glob
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt

import helpers, makehist, printer, heatmap
import plus.settings as settings



def expand_html (html, exportmode):


    module_dir='..\\'
    newhtml=''
    cssfrags=html.split('<link href="')
    newhtml+=cssfrags[0]
   # cssfiles=[cssfrag.split('"')[0] for cssfrag in cssfrags[1:]]

    for cssfrag in cssfrags[1:]:
        cssfile=cssfrag.split('"')[0]
        print cssfile
        if cssfile=='/css/style_h1.css' and exportmode=='include':
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
            jsfile=jsfile.replace('/js-data/best2010','e:\\data\\best2010_info\\heatmaps')
            print jsfile
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

    if exportmode=='include':
        newhtml='\n'.join(newhtml.split('\n')[2:-1])   # skip DOCTYPE, <html> and </html>

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
        export_location='f:\\export.html'
        print 'exporting to %s' % export_location
        html=template.render(context)

        newhtml=expand_html (html,'full')
        f=open(export_location,'w')
        f.write(newhtml)
        f.close()


    return HttpResponse(template.render(context))





@csrf_exempt
def make_subsel(request, dataset):

    post=request.POST
    xvar=post['xvar']
    xmin=float(post['xmin'])
    xmax=float(post['xmax'])

    yvar=post['yvar']
    ymin=float(post['ymin'])
    ymax=float(post['ymax'])
    filename=post['filename']
    txt=post['txt']

    if ymin>ymax:
        ymax,ymin=ymin,ymax

    print xvar,xmin,xmax
    print yvar,ymin,ymax

    infodir=settings.datadir+'/'+dataset+'_info'

    col_info, coltypes_bycol=helpers.get_col_types(infodir)
    subsel=makehist.prepare_subsel (infodir, coltypes_bycol,  xvar,xmin,xmax, yvar,ymin,ymax)

    save_subsel (infodir, subsel, xvar,xmin,xmax, yvar,ymin,ymax,filename,txt)

# bijwerken heatmap-javascript

    infile='%s_%s_%s' % (post['heatmap_xvar'], post['heatmap_yvar'], post['heatmap_index'])
    h=heatmap.heatmap()
    h.infodir=infodir
    args=h.load_options_from_csv(infile)

    f=open('%s/selections/meta.csv' % infodir,'r')
    c=csv.reader(f)
    annotaties={}
    for row in c:
        filename=row[7]
        f=open('%s/selections/%s.txt' % (infodir, row[7]))
        txt=f.read()
        f.close()
        ann_meta={'area':[[float(row[2]), float(row[5])],
                          [float(row[3]), float(row[6])]],
                 'text':txt}
        annotaties[filename]=ann_meta

    args['annotate']=annotaties
    for k,v in args.items():
        setattr(h,k,v)

    newjs=h.opties_to_js(args)
    f=open ('%s/heatmaps/%s_meta2.js' %  (infodir, infile), 'w')
    newjs='var opties=[];\n'+newjs
    f.write(newjs)
    f.close()

    msg='ok'
    data={'msg':msg}

    return HttpResponse(cjson.encode(data))




def save_subsel (infodir, subsel,
                    xvar,xmin,xmax,
                    yvar,ymin,ymax,
                    filename, txt):

    if not os.path.exists(infodir+'/selections'):
        os.makedirs(infodir+'/selections')
        selnr=1
    else:
        try:
            selections=helpers.read_csv_list ('%s/selections/meta.csv' % infodir)
            selnr=len(selections)+1
        except:
            selnr=1

    print 'selnr:', selnr

    f=open('%s/selections/sel_%d.csv' % (infodir, selnr),'wb')
    for i in subsel:
        f.write('%d\n' % i )
    f.close()

    f=open('%s/selections/meta.csv' % infodir,'ab')

    meta=[selnr, xvar,xmin,xmax, yvar,ymin,ymax,filename]
    c=csv.writer(f)
    c.writerow(meta)
    f.close()




    f=open('%s/selections/%s.txt' % (infodir, filename),'w')
    f.write(txt)
    f.close()



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


