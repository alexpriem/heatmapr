import argparse, random
from math import log10


def safelog10 (x):
    if x==0:
        return 0
    if x>0:
        return log10(x)
    return -log10(-x)
        
        



class contour:
    def __init__(self):
        pass


    def check_args(self, args):    # alleen defaults zetten.

        defaults=[
            ['infile',';',True,''],
            ['y','',True,''],
            ['x','',True,''],
            ['sep',';',False,''],
            ['convert_comma',False,False,''],
            ['fuzzx',0,False,''],
            ['fuzzy',0,False,''],
            ['logx',False,False,''],
            ['logy',False,False,''],
            ['gradmin',0,False,''],
            ['gradmax','max',False,''],
            ['gradsteps',40,False,''],
            ['imgwidth',500,False,''],
            ['imgheight',500,False,''],
            ['outfile','',True,''],
            ['xlabel',None,False,''],
            ['ylabel',None,False,''],
            ['title',None,False,''],
            ['dump_html',True,False,'full html output'],
            ['dump_js',True,False,'full html output'],
            ['default_colormap','cbs_blue',False,''],
            ['default_size','1',False,''],
            ['default_transform','linear',False,''],
            
            ['plot_mean', False, False,''],
            ['plot_median_pixelsize',2, False,''],
            ['plot_mean_color',[0,0,0], False,''],
            
            ['plot_median', False, False,''],
            ['plot_mean_pixelsize',2, False,''],
            ['plot_median_color',[0,0,0], False,''],
            
            ['info_datafile',None,False,''],
            ['info_pixelsize',2, False,''],
            ['info_color',[255,0,0], False,''],

            ['debuglevel',0, False,''],            
        ]


        default_colormaps=['blue','gray',
                           'cbs_blue','cbs_green', 'cbs_red', 'cbs_hot',
                            'terrain', 'coolwarm',
                            'hot', 'hot2','ygb']
        default_colormap=args['default_colormap']
        if default_colormap not in default_colormaps:
            raise RuntimeError ('allowed colormaps: %s' % default_colormaps)

        default_transforms=['linear','sqrt','log2','log10']
        default_transform=args['default_transform']
        if default_transform not in default_transforms:
            raise RuntimeError ('allowed colormaps: %s' % default_transforms)


                           
        for varinfo in defaults:
            varname=varinfo[0]
            defaultval=varinfo[1]
            required=varinfo[2]
            helptxt=varinfo[3]
            
            if not (varname in args):
                if required:
                    raise RuntimeError('Missing %s' % varname)
                args[varname]=defaultval
                                        
        for k,v in args.items():
            setattr(self,k,v)

        
        #parser.add_argument('-html', dest='dump_html',  help='html output', required=False, default=True, action='store_true')
        #parser.add_argument('-nohtml', dest='dump_html',  help='html output', required=False, action='store_false')
        #parser.add_argument('-js', dest='dump_js',  help='javascript output', required=False, default=False, action='store_true')
        #parser.add_argument('-nojs', dest='dump_js',  help='javascript output', required=False, action='store_false')        



    def run_contour (self, args):


        self.check_args(args)
                        
        sep=self.sep
        f=open(self.infile)
        line=f.readline()        
        cols=line.strip().split(sep)
        numcols=len(cols)

        x=self.x.strip().split(',')
        if len(x)!=4:
            raise RuntimeError ("-x: expected col, min,max, steps, got %x", str(x))
        y=self.y.strip().split(',')
        if len(x)!=4:
            raise RuntimeError ("-y: expected col, min,max, steps")
        xcol,xmin, xmax, xpixels=[xx.strip() for xx in x]
        ycol,ymin, ymax, ypixels=y=[yy.strip() for yy in y]


        xcolnr=cols.index(xcol)
        ycolnr=cols.index(ycol)
        xmin=int(xmin)
        xmax=int(xmax)
        xpixels=int(xpixels)
        if self.logx:            
            xmin=safelog10(xmin)
            xmax=safelog10(xmax)

        ymin=int(ymin)
        ymax=int(ymax)
        ypixels=int(ypixels)
        if self.logy:            
            ymin=safelog10(ymin)
            ymax=safelog10(ymax)

        xfactor= (xmax-xmin)/ (1.0*xpixels)
        yfactor= (ymax-ymin)/ (1.0*ypixels)
        xfactorinv= (1.0*xpixels)/(xmax-xmin)
        yfactorinv= (1.0*ypixels)/(ymax-ymin)

        self.xmin=xmin
        self.ymin=ymin
        self.xmax=xmax
        self.ymax=ymax
        self.xpixels=xpixels
        self.ypixels=ypixels

        if self.xlabel is None:
            self.xlabel=xcol
        if self.ylabel is None:
            self.ylabel=ycol            

        heatmap=[[0]*xpixels for i in range(ypixels)]
        
        fuzzx=float(self.fuzzx)
        fuzzy=float(self.fuzzy)


        linenr=0
        #f.seek(0)
        keys_x={}
        keys_y={}
        total=0
        for line in f:
            if self.convert_comma:
                line=line.replace(',','.')
            linenr+=1
            if linenr % 10000==0:
                print linenr
            
            cols=line.split(sep)
            try:
                x=float(cols[xcolnr])
                y=float(cols[ycolnr])
            except ValueError:
                if (',' in cols[xcolnr]) or (',' in cols[ycolnr]):
                    self.convert_comma=True 
                    line=line.replace(',','.')
                    cols=line.split(sep)                    
                    x=float(cols[xcolnr])
                    y=float(cols[ycolnr])
                    
            val=1
           # print x,y
            if numcols==3:
                val=float(cols[2])
            if numcols==4:
                val=float(cols[2])*float(cols[3])            
            if (x>xmin and x<xmax):
                hx=int((x-xmin)/xfactor)
                if fuzzx!=0:
                    hx+=int(random.random()*fuzzx)
                    if hx>=xpixels:
                        hx=xpixels-1                
            else:
                continue
            
            if self.plot_median or self.plot_mean:
                x_hist=keys_x.get(hx,{})
                num=x_hist.get(y,0)                
                x_hist[y]=num+val
                keys_x[hx]=x_hist
                
            if (y>ymin and y<ymax):
                hy=int((y-ymin)/yfactor)
                if fuzzy!=0:
                    hy+=int(random.random()*fuzzy)                
                    if hy>ypixels:
                        hy=ypixels
                
            total+=val           
            heatmap[hx][hy]+=val

        self.heatmap=heatmap
        if self.plot_mean:
            avg_x={}
            for xpixel in range(0,xpixels):
                x_hist=keys_x.get(xpixel,None)
                
                if x_hist is None:
                    avg_x[xpixel]=0
                    continue
                
                avg=sum([k*v for k,v in x_hist.items()])/sum(x_hist.values())            
                avg_in_pixels=int((avg-ymin)/yfactor)            
                #print xpixel, avg, avg_in_pixels
                avg_x[xpixel]=avg_in_pixels

        if self.plot_median:
            med_x={}
            for xpixel in range(0,xpixels):
                x_hist=keys_x.get(xpixel,None)                
                if x_hist is None:
                    med_x[xpixel]=0
                    continue
                medval=sum(x_hist.values())/2
                sumv=0
                for k in sorted(x_hist.keys()):
                    if sumv>=medval:
                        med=k                                
                med_in_pixels=int((med-ymin)/yfactor)
               # print xpixel, med, med_in_pixels
                med_x[xpixel]=med_in_pixels
            

        extradata=[]        
        if self.info_datafile is not None:
            f=open(self.info_datafile)
            f.readline()
            for line in f:
                x,y=line.split(sep)
                x=float(x.strip())
                y=float(y.strip())
                xpixel=int((x-xmin)/xfactor) 
                ypixel=int((y-ymin)/yfactor) 
            extradata.append([xpixel,ypixel])

        nonzerocount=0
        for x in range(0,xpixels):
            for y in range(0,ypixels):
                 nonzerocount+=(heatmap[x][y]!=0)
                   
        print '%d records, %d bins filled, %d binvolume over img with %d pixels' % ( linenr, nonzerocount, total, xpixels*ypixels)
        print 'coverage: %.3f%% max, %.3f%% actual' % (100.0*linenr/(xpixels*ypixels*1.0), 100.0*nonzerocount/(1.0*xpixels*ypixels))        


# dump data
               
        js="var data=["

        gradmin=self.heatmap[0][0]
        gradmax=gradmin
        s=''
        for row in self.heatmap:            
            js+=','.join([str(col) for col in row])+',\n'
            minrow=min(row)
            maxrow=max(row)            
            if minrow<gradmin:
                gradmin=minrow
            if maxrow>gradmax:
                gradmax=maxrow                    
        js=js[:-2]+'];\n\n'


        

        self.datamin=gradmin
        self.datamax=gradmax
        
        if getattr(self,'gradmax') is None:
            self.gradmax=gradmax
        
        
        vlist=['gradmin','gradmax','gradsteps',
               'datamin','datamax',
               'xmin','xmax','logx',
               'ymin','ymax','logy',
               'xpixels','ypixels',
               'imgwidth','imgheight',               
               'xlabel','ylabel','title',
               'default_colormap','default_size','default_transform']
        for k in vlist:
            v=getattr(self,k)
            if self.debuglevel==1:
                print k,v
            if v==None:
                js+='var %s="";\n' % (k)
                continue
            t=type(v)
            if t==str:            
                js+='var %s="%s";\n' % (k,v)
                continue
            if t==bool:
                if v:
                    js+='var %s=true;\n' % (k)
                else:                    
                    js+='var %s=false;\n' % (k)
                continue            
            js+="var %s=%s;\n" % (k,v)


        js+='var opties={'
        for k,v in args.items():
            if v is None:
                js+='"%s":null,\n' % (k)                
                continue
            t=type(v)
            if t==str:            
                js+='"%s":"%s",\n' % (k,v)
                continue
            if t==bool:
                if v:
                    js+='"%s":true,\n' % (k)
                else:                    
                    js+='"%s":false,\n' % (k)
                continue
            js+='"%s":%s,\n' % (k,v)
        js+='};\n\n'

        if self.plot_mean:
            js+='var mean_x=['
            txt=''
            nr=0
            for xpixel in sorted(avg_x.keys()):                
                if nr>9:
                    txt+='\n'
                    nr=0
                nr+=1
                txt+=str(avg_x[xpixel])+','
                
            js+=txt[:-1]+'];\n\n'

        if self.plot_median:
            js+='var median_x=['
            txt=''
            nr=0
            for xpixel in sorted(med_x.keys()):                
                if nr>9:
                    txt+='\n'
                    nr=0
                nr+=1
                txt+=str(med_x[xpixel])+','
                
            js+=txt[:-1]+'];\n\n'


        if self.info_datafile:
            js+='var extradata=['
            txt=''
            nr=0
            for xpixel,ypixel in extradata:
                if nr>9:
                    txt+='\n'
                    nr=0
                nr+=1
                txt+='[%d,%d],' % (xpixel, ypixel)
                
            js+=txt[:-1]+'];\n'
                    
                
                    
            

        if self.dump_js:
            f=open(self.outfile+'.js','w')
            f.write(js)
            f.close()        

        self.js=js
        if self.dump_html==False:
            f=open("js/data.js","w")
            f.write(js)
            f.close()

        


#    def write_html (self, args):
        
        if self.dump_html:
            html=open ("bitmap.html",'r').read()
            
            g=open(self.outfile+'.html','w')
            cssfrags=html.split('<link href="')
            g.write(cssfrags[0])
            cssfiles=[cssfrag.split('"')[0] for cssfrag in cssfrags[1:]]            

            for cssfrag in cssfrags[1:]:
                cssfile=cssfrag.split('"')
                if self.debuglevel==2:
                    print cssfile[0]
                g.write('\n<style>\n')
                css=open(cssfile[0],"r").read()
                g.write(css)
                g.write('\n</style>\n')

            g.write('\n<script type="text/javascript">\n')            
            g.write(self.js)
            g.write('\n</script>\n')
            
            jsfrags=html.split('<script src="')            
            for jsfrag in jsfrags[1:]:
                jsfile=jsfrag.split('"')
                if jsfile[0]=='js/data.js':
                    continue
                if self.debuglevel==2:
                    print jsfile[0]
                g.write('\n<script type="text/javascript">\n')
                js=open(jsfile[0],'r').read()    
                g.write(js)
                g.write('\n</script>\n')

            body=html.split("<body>")

            g.write("</head>\n")
            g.write("<body>\n")


            body=body[1]
            jsfrags=body.split('<script  src="')
            for jsfrag in jsfrags[1:]:                
                jsfile=jsfrag.split('"')
                js_end=jsfrag.split('\n')[0]                
              #  print jsfile[0]
                js_txt='\n<script type="text/javascript">\n'
                js_txt+=open(jsfile[0],'r').read()    
                js_txt+='\n</script>\n'
              #  print js_txt
                body=jsfrags[0]+js_txt+jsfrags[1][len(js_end):]
                
            g.write(body)
            g.close()




