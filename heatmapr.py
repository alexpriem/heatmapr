import random, os, sys, inspect, json, bisect, gzip
from math import log10
import datetime #.datetime.strptime as strptime
#from datetime.datetime import strptime


def safelog10 (x):
    if x==0:
        return 0
    if x>0:
        return log10(x)
    return -log10(-x)
        
        



class heatmap:
    def __init__(self):
        pass


    def check_args(self, args):    # alleen defaults zetten.

        defaults=[
            ['infile',';',True,''],
            ['sep',';',False,''],
            ['convert_comma',False,False,''],

            ['x_fixedfile_startpos',None,False,''],
            ['x_fixedfile_endpos',None,False,''],
            
            ['x_var','',True,''],
            ['x_min','',True,''],
            ['x_max','',True,''],
            ['x_steps','',True,''],
            ['x_fuzz',0,False,''],
            ['x_fill',0,False,''],
            ['x_log',False,False,''],
            ['x_data_type','nominal',False,''],
            ['x_dateformat','%Y%m%d',False,''],
            ['x_relative', False,False,''],
            ['x_relative_min', 0,False,''],
            ['x_relative_max', 100,False,''],


            ['y_fixedfile_startpos',None,False,''],
            ['y_fixedfile_endpos',None,False,''],
            
            ['y_var','',True,''],
            ['y_min','',True,''],
            ['y_max','',True,''],
            ['y_steps','',True,''],
            ['y_fuzz',0,False,''],
            ['y_fill',0,False,''],
            ['y_log',False,False,''],
            ['y_data_type','nominal',False,''],
            ['y_dateformat','%Y%m%d',False,''],
            ['y_relative', False,False,''],
            ['y_relative_min', 0,False,''],
            ['y_relative_max', 100,False,''],
            
            ['weight_var',None,False,''],

            
            

            ['gradmin',0,False,''],
            ['gradmax','max',False,''],
            ['gradsteps',40,False,''],
            
            ['gradient_invert',False,False,''],
            ['gradcenter',50,False,''],
            ['gradient_bimodal',False,False,''],
            
            
            ['imgwidth',500,False,''],
            ['imgheight',500,False,''],
            ['outfile','',True,''],
            ['xlabel',None,False,''],
            ['ylabel',None,False,''],
            ['fontsize',16,False,''],
            ['numticks',None,False,''],
            
            
            ['title',None,False,''],
            ['dump_html',True,False,'full html output'],            
            ['dump_csv',False,False,'dump output to csv'],    
            ['colormap','blue',False,''],
            ['missing_color','min',False,''],
            ['size','1',False,''],
            ['transform','linear',False,''],
            ['log_min',1,False,''],
            

            ['displaymode','heatmap',False,''],
            ['stats_enabled', True, False,''],
            ['plot_mean', False, False,''],
            ['plot_mean_pixelsize',2, False,''],
            ['plot_mean_color',[0,0,0,255], False,''],
            
            ['plot_median', False, False,''],
            ['plot_median_pixelsize',2, False,''],
            ['plot_median_color',[0,0,255,255], False,''],

            ['info_datafile',None,False,''],
            ['info_pixelsize',2, False,''],
            ['info_color',[255,0,0,255], False,''],
                    
            ['dot_color','blue',False,''],
            ['dot_dotsize',5,False,''],
            ['dot_boxsize',0.6,False,''],
            ['dot_use_gradient',False,False,''],
            ['dot_show_background',True,False,''],
            
            ['text_show_background',True,False,''],
            
            ['weighx',False,False,''],
            ['weighy',False,False,''],


            ['multimap', [],False,''],
            ['multimap_labels',{},False,''],
            
            ['multi_nr', 0,False,''],
            ['multi_cols', 5,False,''],
            
            
            ['controltype','notflat', False,''], 
            ['debuglevel',0, False,''],            
        ]


        self.module_dir=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
      
        
        defaultvars=[]
        for varinfo in defaults:
            varname=varinfo[0]
            defaultvars.append(varname)
            defaultval=varinfo[1]
            required=varinfo[2]
           # helptxt=varinfo[3]
            
            if not (varname in args):
                if required:
                    raise RuntimeError('Missing required variable %s' % varname)
                args[varname]=defaultval

        for varname in args.keys():
            if varname not in defaultvars:
                raise RuntimeError('Unknown variable: %s' % varname)


        colormaps=['blue','blue_white', 'blue_black','green', 'red','gray',
                    'terrain', 'coolwarm',
                    'hot', 'hot2','hot3', 'ygb','qualitative',
                    'qualitative14','qualitative28']
        colormap=args['colormap']
        if colormap not in colormaps:
            raise RuntimeError ('allowed colormaps: %s' % colormaps)

        transforms=['linear','sqrt','log']
        transform=args['transform']
        if transform not in transforms:
            raise RuntimeError ('allowed transforms: %s' % transforms)

                                        
        for k,v in args.items():
            setattr(self,k,v)


        if args['x_steps']>args['imgwidth']:
            raise RuntimeError ('\n\nx_steps > imgwidth: (%s>%s)' % (args['x_steps'],args['imgwidth']))
        if args['y_steps']>args['imgheight']:
            raise RuntimeError ('\n\ny_steps > imgheight: (%s>%s)' % (args['y_steps'],args['imgheight']))


        if int(args['x_steps'])>2000:
            raise RuntimeError ('\n\nx_steps too large (>2000). (x_steps:%s)' % (args['x_steps']))
        if int(args['y_steps'])>2000:
            raise RuntimeError ('\n\ny_steps too large (>2000). (y_steps:%s)' % (args['y_steps']))
        if int(args['imgwidth'])>2000:
            raise RuntimeError ('\n\imgwidth too large (>2000). (imgwidth:%s)' % (args['imgwidth']))
        if int(args['imgheight'])>2000:
            raise RuntimeError ('\n\imgheight too large (>2000). (imgheight:%s)' % (args['imgheight']))
        


    def munge_date (self, d, datatype, date_min):

            if datatype=='date_year':
                    return d.year-date_min.year
            if datatype=='date_quarter':
                    return (d.year-date_min.year)*4+(d.month)/4-(date_min.month)/4  
            if datatype=='date_month':
                    return (d.year-date_min.year)*12+d.month-date_min.month
            if datatype=='date_week':                     
                    return ((d-date_min).days)/7
            if datatype=='date_day':
                    return (d-date_min).days            

            raise RuntimeError("x_data_type/y_datatype should be date_year, date_quarter, date_month, date_week or date_day, not '%s'" % datatype)
            





    def heatmap_to_js (self, heatmap):        
        gradmin=self.gradmin
        gradmax=self.gradmax
        
        js='data.push([';
        for row in heatmap:            
            js+=','.join([str(col) for col in row])+',\n'
            minrow=min(row)
            maxrow=max(row)            
            if minrow<gradmin:
                gradmin=minrow
            if maxrow>gradmax:
                gradmax=maxrow   
        js=js[:-2]+']);\n\n'
        
        return js


    def heatmap_to_csv (self, heatmap, filename):        
        gradmin=self.gradmin
        gradmax=self.gradmax
        f=open (filename,'w')
        for row in heatmap:            
            f.write(','.join([str(col) for col in row])+'\n')
            minrow=min(row)
            maxrow=max(row)            
            if minrow<gradmin:
                gradmin=minrow
            if maxrow>gradmax:
                gradmax=maxrow
        f.close()
        

    def bin_keyvalues_to_hist (self, histdict, step):
        pos=[]
        sumk=0
        histlist=sorted(histdict.keys())
        for k in histlist:
         #   print k, sumk, step                        
            sumk+=histdict[k]
            if sumk>step:
                while (sumk>step):
#                    print len(pos),k
                    pos.append(k)
                    sumk=sumk-step
        if sumk!=0:
            pos.append(k)
        return pos





    def make_heatmap (self, args):


        self.check_args(args)
                        
        sep=self.sep
        if self.infile[-3:]=='.gz':
            f=gzip.open(self.infile)
        else:
            f=open(self.infile)
        line=f.readline()        
        cols=[c.lower().strip() for c in line.split(sep)]
       
        
        xcol=self.x_var.lower()
        xmin=self.x_min
        xmax=self.x_max
        xpixels=int(self.x_steps)

        ycol=self.y_var.lower()
        ymin=self.y_min
        ymax=self.y_max
        ypixels=int(self.y_steps)
        

        x_data_type=self.x_data_type
        y_data_type=self.y_data_type
        x_dateformat=self.x_dateformat
        y_dateformat=self.y_dateformat
        try:
            xcolnr=cols.index(xcol)
            ycolnr=cols.index(ycol)
        except:
            print 'column not found'
            print 'xcolumn:',xcol, 
            print 'ycolumn:',ycol
            print 'columns:',cols
            sys.exit()
        if x_data_type=='nominal':
        	xmin=float(xmin)
        	xmax=float(xmax)
        else:
            xmin_date=datetime.datetime.strptime(xmin,x_dateformat)	    	
            xmax_date=datetime.datetime.strptime(xmax,x_dateformat)
            self.xmin_date=xmin_date
            self.xmax_date=xmax_date
            xmin=0
            xmax=self.munge_date(xmax_date, x_data_type, xmin_date)
        
        if y_data_type=='nominal':
        	ymin=float(ymin)
        	ymax=float(ymax)
        else:
            ymin_date=datetime.datetime.strptime(ymin,y_dateformat)	    	
            ymax_date=datetime.datetime.strptime(ymax,y_dateformat)
            self.ymin_date=ymin_date
            self.ymax_date=ymax_date
            ymin=0
            ymax=self.munge_date(ymax_date, y_data_type, ymin_date)
       
        x_log=self.x_log
        if x_log:            
            xmin=safelog10(xmin)
            xmax=safelog10(xmax)
        y_log=self.y_log
        if y_log:            
            ymin=safelog10(ymin)
            ymax=safelog10(ymax)        
        
        self.xmin=xmin
        self.ymin=ymin
        self.xmax=xmax
        self.ymax=ymax
        self.xpixels=xpixels
        self.ypixels=ypixels
        
        xfactor= (xmax-xmin)/ (1.0*(xpixels-1))
        yfactor= (ymax-ymin)/ (1.0*(ypixels-1))

        if self.xlabel is None:
            self.xlabel=xcol
        if self.ylabel is None:
            self.ylabel=ycol            

        do_fixed=False
        if x_fixedfile_startpos is not None and x_fixedfile_endpos is not None:
            do_fixed=True
    
        weightcolnr=None
        if self.weight_var is not None and do_fixed is False:
            weightcolnr=cols.index(self.weight_var)
            

        do_multimap=False
        if len(self.multimap)>0:
            multicols=[cols.index(m) for m in self.multimap]
            do_multimap=True


        heatmaps={}
        heatmap=[[0]*ypixels for i in range(xpixels)]
        self.heatmap=heatmap
        
        x_fuzz=int(self.x_fuzz)
        y_fuzz=int(self.y_fuzz)
        x_fill=int(self.x_fill)
        y_fill=int(self.y_fill)
        no_fill=False
        if x_fill==0 and y_fill==0:
        	no_fill=True


        if self.x_relative or self.y_relative:
            x_fullhist={}
            y_fullhist={}        
            linenr=0
            for line in f:
                linenr+=1
                if linenr % 10000==0:
                    print linenr
                
                if self.convert_comma:
                    line=line.replace(',','.')

                val=1                
                if not do_fixed:
                    cols=line.split(sep)
                    x_txt=cols[xcolnr]
                    y_txt=cols[ycolnr]
                    if weightcolnr is not None:
                        val=float(cols[weightcolnr])
                else:
                    x_txt=line[x_fixedfile_startpos:x_fixedfile_endpos]
                    y_txt=line[y_fixedfile_startpos:y_fixedfile_endpos]
                    if weight_fixedfile_startpos is not None:
                        val=float(line[weight_fixedfile_startpos:weight_fixedfile_endpos])
		        
                if x_data_type=='nominal':
                    x=float(x_txt)
                else:
                    x=datetime.datetime.strptime(x_txt,x_dateformat)
                    x=self.munge_date(x, x_data_type, xmin_date)

                if y_data_type=='nominal':
                    y=float(y_txt)
                else:
                    y=datetime.datetime.strptime(y_txt,y_dateformat)
                    y=self.munge_date(y, y_data_type, ymin_date)

                
                
                if self.x_relative:
                    x_fullhist[x]=x_fullhist.get(x,0)+val
                if self.y_relative:                    
                    y_fullhist[y]=y_fullhist.get(y,0)+val
            f.seek(0,0)
            f.readline()
            
            if self.debuglevel==3:
                print 'x-hist'
                for k,v in x_fullhist.items():
                    print k,v
                print 'y-hist'
                for k,v in y_fullhist.items():
                    print k,v
            if self.x_relative:
                xhist=sorted(x_fullhist.keys())
                N=sum(x_fullhist.values())
                xhistpos=self.bin_keyvalues_to_hist (x_fullhist, N/(1.0*xpixels))
                xhistpos_fuzz=[]
                for x in sorted(xhistpos):
                    xhistpos_fuzz.append(xhistpos.count(x))

            if self.y_relative:
                N=sum(y_fullhist.values())
                yhist=sorted(y_fullhist.keys())
                yhistpos=self.bin_keyvalues_to_hist (y_fullhist, N/(1.0*ypixels))                
                yhistpos_fuzz=[]
                for y in sorted(yhistpos):
                    yhistpos_fuzz.append(yhistpos.count(y))

        
            

                  


        linenr=0
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
                val=1                
                if not do_fixed:
                    cols=line.split(sep)
                    x_txt=cols[xcolnr]
                    y_txt=cols[ycolnr]
                    if weightcolnr is not None:
                        val=float(cols[weightcolnr])
                else:
                    x_txt=line[x_fixedfile_startpos:x_fixedfile_endpos]
                    y_txt=line[y_fixedfile_startpos:y_fixedfile_endpos]
                    if weight_fixedfile_startpos is not None:
                        val=float(line[weight_fixedfile_startpos:weight_fixedfile_endpos])

                
                if x_data_type=='nominal':
                    x=float(x_txt)
                else:                  
                    if x_txt!='':
                        x=datetime.datetime.strptime(x_txt,x_dateformat)
                    else:
                        x=xmin_date
                   # print x
                    x=self.munge_date(x, x_data_type, xmin_date)
                    #print x

                if y_data_type=='nominal':
        	    y=float(y_txt)
                else:
                    if y_txt!='':
                        y=datetime.datetime.strptime(y_txt,y_dateformat)
                    else:
                        y=ymin_date
                      y=self.munge_date(y, y_data_type, ymin_date)
            except ValueError:
                if (',' in cols[xcolnr]) or (',' in cols[ycolnr]):
                    self.convert_comma=True 
                    line=line.replace(',','.')
                    cols=line.split(sep)                    
                if x_data_type=='nominal':                    
                    if x_txt!='':
                        x=float(x_txt)
                    else:
                        x=0
                else:                   
                    if x_txt!='':
                        x=datetime.datetime.strptime(x_txt,x_dateformat)
                    else:
                        x=xmin_date
                    x=self.munge_date(x, x_data_type, xmin_date)


                if y_data_type=='nominal':                    
                    if y_txt!='':
                        y=float(s)
                    else:
                        y=0
                else:                
                    if y_txt!='':                        
                        y=datetime.datetime.strptime(y_txt,y_dateformat)
                    else:
                        y=ymin_date
                    y=self.munge_date(y, y_data_type, ymin_date)
                            

            
            if self.x_relative==False:                                                
                if x_log:
                    x=safelog10(x)                        
                if (x>=xmin and x<=xmax):
                    hx=int((x-xmin)/xfactor)
                    
                    if x_fuzz!=0:
                        hx+=int(random.random()*x_fuzz)
                        if hx>=xpixels:
                            hx=xpixels-1                
                else:
                    continue
                
            if self.x_relative==True:
                hx=bisect.bisect_left(xhistpos,x)
                try:
                    if (xhistpos_fuzz[hx]>1):
                        hx+=int(random.random()*xhistpos_fuzz[hx])
                        if hx>=xpixels:
                            hx=xpixels-1
                except:
                    print 'overflow, x:',  hx, len(xhistpos)

            
            if self.stats_enabled:
                x_hist=keys_x.get(hx,{})
                num=x_hist.get(y,0)                
                x_hist[y]=num+val
                keys_x[hx]=x_hist

            if self.y_relative==False:
                if y_log:
                    y=safelog10(y)
                if (y>=ymin and y<=ymax):
                    hy=int((y-ymin)/yfactor)
                    if y_fuzz!=0:
                        hy+=int(random.random()*y_fuzz)                
                        if hy>ypixels:
                            hy=ypixels-1
                else:
                    continue
                
            if self.y_relative==True:
                hy=bisect.bisect_left(yhistpos,y)
                
                if hy>=ypixels:
                    hy=ypixels-1
                try:
                    if (yhistpos_fuzz[hy]>1):                                    
                        hy+=int(random.random()*yhistpos_fuzz[hy])
                    if hy>=ypixels:
                        hy=ypixels-1  
                except:
                    print 'overflow-y:',  hy, len(yhistpos)                    
            total+=val  #

            
            if do_multimap:
                heatmapname=''
                for splitcol in multicols:                    
                    heatmapname+='_'+cols[splitcol]
                heatmap=heatmaps.get(heatmapname,None)
                if heatmap is None:
                    heatmap=[[0]*ypixels for i in range(xpixels)]
                    print 'define:', heatmapname
                heatmap[hx][hy]+=val
                heatmaps[heatmapname]=heatmap
                heatmap=self.heatmap
            
            try:
            	if no_fill:
                    heatmap[hx][hy]+=val
                else:                    
                    for dx in xrange(x_fill):
                        if y_fill==0:
                            heatmap[hx+dx][hy]+=val
                        else:                            
                            for dy in xrange(y_fill):
                                if (hy+dy<ypixels) and (hx+dx<xpixels):
                                    heatmap[hx+dx][hy+dy]+=val
                	    
            except IndexError:
                print 'IndexError (%d,%d), line nr %d:' % (hx,hy,linenr)
                print 'inputdata:',line
                sys.exit()

        

        #print heatmap
            
        if self.stats_enabled:  # calculate mean
            avg_x={}
            for xpixel in range(0,xpixels):
                x_hist=keys_x.get(xpixel,None)
                
                if x_hist is None:
                    avg_x[xpixel]=0
                    continue

                
                avg=sum([k*v for k,v in x_hist.items()])/sum(x_hist.values())            
                if avg<ymin:
                    avg=ymin
                if avg>ymax:
                    avg=ymax                         
                avg_in_pixels=int((avg-ymin)/yfactor)            
                #print xpixel, avg, avg_in_pixels
                avg_x[xpixel]=avg_in_pixels

        if self.stats_enabled:  # calculate median
            med_x={}
            for xpixel in range(0,xpixels):
                x_hist=keys_x.get(xpixel,None)                
                if x_hist is None:
                    med_x[xpixel]=0
                    continue
                medval=sum(x_hist.values())/2
                if medval<ymin:
                    medval=ymin
                if medval>ymax:
                    medval=ymax                         
                med_in_pixels=int((medval-ymin)/yfactor)
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
                if (x<xmin) or (x>xmax) or (y<xmin) or (y>ymax):
                    continue
                xpixel=int((x-xmin)/xfactor) 
                ypixel=int((y-ymin)/yfactor)                
            extradata.append([xpixel,ypixel])

        nonzerocount=0
        xsum=[0]*xpixels
        ysum=[0]*ypixels
        totalsum=0
        for x in range(0,xpixels):
            for y in range(0,ypixels):
                val=heatmap[x][y]
                nonzerocount+=(val!=0)
                xsum[x]+=val
                ysum[y]+=val
                totalsum+=val

                 
        print '%d records, %d bins filled, %d binvolume over img with %d pixels' % ( linenr, nonzerocount, total, xpixels*ypixels)
        print 'coverage: %.3f%% max, %.3f%% actual' % (100.0*linenr/(xpixels*ypixels*1.0), 100.0*nonzerocount/(1.0*xpixels*ypixels))

# multimaps aanmaken zo nodig

        if do_multimap:
            datakeys=sorted(heatmaps.keys())            
            multimap_vals=[[0]*ypixels for i in range(xpixels)]
            multimap_colors=[[0]*ypixels for i in range(xpixels)]
            for x in range(0,xpixels):
                for y in range(0,ypixels):
                    vals=[heatmaps[k][x][y] for k in datakeys]
                    maxval=max(vals)
                    multimap_vals[x][y]=maxval
                    multimap_colors[x][y]=vals.index(maxval)


# test autoscaling
        cutoff=1
        min_x=xsum[0]
        for x in range(0,xpixels):
            if xsum[x]>cutoff:
                min_x=x
                break
        max_x=xsum[0]            
        for x in range(xpixels-1,0,-1):
            if xsum[x]>cutoff:
                max_x=x
                break
        print 'suggested autoscale x:', min_x*xfactor+xmin,max_x*xfactor+xmin

        cutoff=1
        min_y=ysum[0]
        for y in range(0,ypixels):
            if ysum[y]>cutoff:
                min_y=y
                break
        max_y=ysum[0]
        for y in range(ypixels-1,0,-1):
            if ysum[y]>cutoff:
                max_y=y
                break
        print 'suggested autoscale y:', min_y*yfactor+ymin,max_y*yfactor+ymin
        


# dump data
        js=''
        if self.multi_nr==0 and do_multimap==False:
            js='var multimap=false;\nnr_heatmaps=1;\n\nvar data=[];\n'
    
        gradmin=self.heatmap[0][0]
        gradmax=gradmin

        if self.dump_csv:
            self.heatmap_to_csv (heatmap,self.outfile+'.csv')

        if do_multimap==True:
            datakeys=sorted(heatmaps.keys())
            js='var multimap=true;\n'
            js+='var nr_heatmaps=1;\n\n'
            js+='var data=[];\n'
            js+='var multimap_vals=[];\n'
            js+='var multimap_colors=[];\n'

            
            vals=self.heatmap_to_js(multimap_vals)
            js+=vals.replace('data','multimap_vals')
            colors=self.heatmap_to_js(multimap_colors)
            js+=colors.replace('data','multimap_colors')

            js+=self.heatmap_to_js (heatmaps[datakeys[0]])

            js+='var multimap_labels='+json.dumps(self.multimap_labels)+';\n';
            
            
           
             
           # for filename in datakeys:
           #     print filename
           #     heatmap=heatmaps[filename]
           #     js+=self.heatmap_to_js (heatmap)
           #     self.heatmap_to_csv (heatmap,self.outfile+filename+'.csv')
                
            js+='var datakeys='+str(datakeys)+';\n'
        if do_multimap==False:
            js+=self.heatmap_to_js (self.heatmap)

        self.datamin=gradmin
        self.datamax=gradmax
        
        if getattr(self,'gradmax') is None:
            self.gradmax=gradmax        

        if self.multi_nr==0:
                js+='var opties=[];\n'
        optiejs='opties.push({'
        for k in sorted(args.keys()):
            v=args[k]
            if v is None:
                optiejs+='"%s":null,\n' % (k)                
                continue
            t=type(v)
            if t==str:
                v=v.replace('\\','/')
                optiejs+='"%s":"%s",\n' % (k,v)
                continue
            if t==bool:
                if v:
                    optiejs+='"%s":true,\n' % (k)
                else:                    
                    optiejs+='"%s":false,\n' % (k)
                continue
            if isinstance(v, datetime.date):
                optiejs+='"%s":new Date("%s")\n,' % (k,v.isoformat())
                continue
            optiejs+='"%s":%s,\n' % (k,v)
        optiejs+='});\n\n'
        if do_multimap:
            for filename in datakeys:   # datakeys alleen gebruiken om te loopen over aantal opties
                js+=optiejs
        else:
            js+=optiejs

        if self.multi_nr==0:
            js+='var sum_x=[];\n';
        js+='sum_x.push(['
        txt=''
        nr=0
        for sumx in xsum:                
            if nr>9:
                txt+='\n'
                nr=0
            nr+=1
            txt+=str(sumx)+','
        js+=txt[:-1]+']);\n\n'
        
        if self.multi_nr==0:
            js+='var sum_y=[];\n';
        js+='sum_y.push(['
        txt=''
        nr=0
        for sumy in ysum:                
            if nr>9:
                txt+='\n'
                nr=0
            nr+=1
            txt+=str(sumy)+','
        js+=txt[:-1]+']);\n\n'

        if self.multi_nr==0:
            js+='var xmean=[];\n'
            js+='var ymean=[];\n'
        js+='var totalsum=%s;\n' % str(totalsum)
        js+='xmean.push(%s);\n' % str(float(sum(xsum))/len(xsum) )
        js+='ymean.push(%s);\n\n' % str(float(sum(xsum))/len(ysum) )
    

        if self.stats_enabled:   #mean
            if self.multi_nr==0:
                js+='var mean_x=[];\n'
            js+='mean_x.push(['
            txt=''
            nr=0
            for xpixel in sorted(avg_x.keys()):                
                if nr>9:
                    txt+='\n'
                    nr=0
                nr+=1
                txt+=str(avg_x[xpixel])+','
                
            js+=txt[:-1]+']);\n\n'

        if self.stats_enabled:  # median
            if self.multi_nr==0:
                js+='var median_x=[];\n'
            js+='median_x.push(['
            txt=''
            nr=0
            for xpixel in sorted(med_x.keys()):                
                if nr>9:
                    txt+='\n'
                    nr=0
                nr+=1
                txt+=str(med_x[xpixel])+','
                
            js+=txt[:-1]+']);\n\n'


        if self.info_datafile:
            if self.multi_nr==0:
                js+='var extradata=[];\n'
            js+='extradata.push(['
            txt=''
            nr=0
            for xpixel,ypixel in extradata:
                if nr>9:
                    txt+='\n'
                    nr=0
                nr+=1
                txt+='[%d,%d],' % (xpixel, ypixel)
                
            js+=txt[:-1]+']);\n'

        
                    

        self.js=js
        if self.dump_html==False:
            if self.multi_nr==0:
                f=open(self.module_dir+"/js/data.js","w")
            else:
                f=open(self.module_dir+"/js/data.js","a")
            f.write(js)
            f.close()

        


#    def write_html (self, args):
        
        if self.dump_html:
            html=open (self.module_dir+'/bitmap.html','r').read()
            
            g=open(self.outfile+'.html','w')
            cssfrags=html.split('<link href="')
            g.write(cssfrags[0])
           # cssfiles=[cssfrag.split('"')[0] for cssfrag in cssfrags[1:]]            

            for cssfrag in cssfrags[1:]:
                cssfile=cssfrag.split('"')
                if self.debuglevel==2:
                    print cssfile[0]
                g.write('\n<style>\n')
                css=open(self.module_dir+'/'+cssfile[0],"r").read()
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
                js=open(self.module_dir+'/'+jsfile[0],'r').read()    
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
                js_txt+=open(self.module_dir+'/'+jsfile[0],'r').read()    
                js_txt+='\n</script>\n'
              #  print js_txt
                body=jsfrags[0]+js_txt+jsfrags[1][len(js_end):]
                
            g.write(body)
            g.close()




