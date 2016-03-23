import random, os, inspect, json, bisect, csv, cjson, sys, ast, operator
from math import log10
import datetime #.datetime.strptime as strptime
import helpers


def safelog10 (x):
    if x==0:
        return 0
    if x>0:
        return log10(x)
    return -log10(-x)
        
        



class heatmap:
    def __init__(self):
        self.js=''
        self.defaults=[
            ['infodir','',True],
            ['sep',',',False],
            ['convert_comma',False,False],

            ['x_var','',True],
            ['x_label','',False],
            ['x_min','perc01',True],
            ['x_max','max',True],
            ['x_steps',0,False],
            ['x_fuzz',0,False],
            ['x_fill',0,False],
            ['x_log',False,False],
            ['x_data_type','nominal',False],
            ['x_dateformat','%Y%m%d',False],
            ['x_relative', False,False],
            ['x_relative_min', 0,False],
            ['x_relative_max', 100,False],

            ['y_var','',True],
            ['y_label','',False],
            ['y_min','perc01',True],
            ['y_max','max',True],
            ['y_steps',0,False],
            ['y_fuzz',0,False],
            ['y_fill',0,False],
            ['y_log',False,False],
            ['y_data_type','nominal',False],
            ['y_dateformat','%Y%m%d',False],
            ['y_relative', False,False],
            ['y_relative_min', 0,False],
            ['y_relative_max', 100,False],

            ['weight_var','',False],

            ['split1_var','',False],
            ['split2_var','',False],

            ['gradmin',0,False],
            ['gradmax','max',False],
            ['gradsteps',40,False],

            ['gradient_invert',False,False],
            ['gradcenter',50,False],
            ['gradient_bimodal',False,False],

            ['imgwidth',500,False],
            ['imgheight',500,False],
            ['outfile','',True],

            ['fontsize',16,False],
            ['numticks',0,False],



            ['title','',False],
            ['dump_csv',False,False],
            ['colormap','blue',False],
            ['missing_color','[192,192,192,255]',False],
            ['size','1',False],
            ['transform','linear',False],
            ['log_min',1,False],

            ['displaymode','heatmap',False],
            ['stats_enabled', True, False],
            ['plot_mean', False, False],
            ['plot_mean_pixelsize',2, False],
            ['plot_mean_color','[255,0,0,255]', False],

            ['plot_median', False, False],
            ['plot_median_pixelsize',2, False],
            ['plot_median_color','[0,0,255,255]', False],

            ['info_datafile','',False],
            ['info_pixelsize',2, False],
            ['info_color','[0,0,0,255]', False],

            ['dot_color','blue',False],
            ['dot_dotsize',5,False],
            ['dot_boxsize',0.6,False],
            ['dot_use_gradient',False,False],
            ['dot_show_background',True,False],

            ['text_show_background',True,False],

            ['weighx',False,False],
            ['weighy',False,False],

            ['multimap',False,False],
            ['multimap_labels',{},False],
            ['multimap_numcols',4,False],

            ['annotate',{},False],

            ['heatmap_indexnr',False,False],   # dummyvar
            ['add_new_heatmap',False,False],   # dummyvar
            ['expertmode',0, False],           # dummyvar
            ['controltype','notflat', False],   # dummyvar
            ['debuglevel',0, False],
        ]
        self.simple_vars=['x_var','x_label','x_min','x_max','x_steps',
                          'y_var','y_label','y_min','y_max','y_steps',
                          'colormap','grad_min','grad_max','grad_steps',
                          'weight_var', 'split1_var', 'split2_var',
                          'title']

        self.no_rebuild=['x_label','y_label','title','colormap','missing_color',
                         'fontsize','numticks',
                         'plot_mean','plot_mean_color','plot_mean_pixelsize',
                         'plot_median', 'plot_median_color','plot_median_pixelsize',
                         'dot_color','dot_dotsize','dot_boxsize']

        self.booleans=['x_log','x_relative',
                      'y_log','y_relative',
                      'gradient_invert','gradient_bimodal',
                      'weighx','weighy',
                      'text_show_background',
                      'plot_mean','plot_median']





    def check_args(self, args):    # alleen defaults zetten.

        defaults=self.defaults

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

        print 'XREL:', type(args['x_relative'])

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

                                        
        for key,value in args.items():
            try:
                value=ast.literal_eval(value)
            except:
                pass
            setattr(self,key,value)

        if self.x_steps is None:
            self.x_steps=self.imgwidth
        if self.y_steps is None:
            self.y_steps=self.imgheight

        if self.x_steps>self.imgwidth:
            s='\n\nx_steps > imgwidth: (%s>%s)' % (self.x_steps, self.imgwidth)
            raise RuntimeError (s)
        if self.y_steps>self.imgheight:
            s='\n\ny_steps > imgheight: (%s>%s)' % (self.y_steps, self.imgheight)
            raise RuntimeError (s)


        if int(self.x_steps)>2000:
            s='\n\nx_steps too large (>2000). (x_steps:%s)' % (self.x_steps)
            raise RuntimeError (s)
        if int(self.y_steps)>2000:
            s='\n\ny_steps too large (>2000). (y_steps:%s)' % (self.y_steps)
            raise RuntimeError (s)
        if int(self.imgwidth)>2000:
            s='\n\imgwidth too large (>2000). (imgwidth:%s)' % (self.imgwidth)
            raise RuntimeError (s)
        if int(self.imgheight)>2000:
            s='\n\imgheight too large (>2000). (imgheight:%s)' % (self.imgheight)
            raise RuntimeError (s)

        if (self.weight_var is not None) and self.weight_var.strip()=='':
            self.weight_var=None
        if (self.info_datafile is not None) and self.info_datafile.strip()=='':
            self.info_datafile=None



        


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
            s="x_data_type/y_datatype should be date_year, date_quarter, date_month, date_week or date_day, not '%s'" % datatype
            raise RuntimeError(s)
            


    def aggegrate_by_4 (self, heatmap):

        h=heatmap
        if self.x_steps>200 or self.y_steps>200:
            small_x_len=self.x_steps/4
            small_y_len=self.y_steps/4
        else:
            return h

        smallmap=[[0]*small_y_len for i in range(small_x_len)]
        for i in range(0,self.x_steps-1,4):
            for j in range(0,self.y_steps-1,4):
                u=i/4
                v=j/4
                val=h[i][j] + h[i][j+1] + h[i][j+2] + h[i][j+3] + \
                    h[i+1][j] + h[i+1][j+1] + h[i+1][j+2] + h[i+1][j+3] + \
                    h[i+2][j] + h[i+2][j+1] + h[i+2][j+2] + h[i+2][j+3] + \
                    h[i+3][j] + h[i+3][j+1] + h[i+3][j+2] + h[i+3][j+3]
                smallmap[u][v]=val
        return smallmap


    def heatmap_to_js (self, heatmap):        
        gradmin=self.gradmin
        gradmax=self.gradmax

        js='var d=[];\n'
        for row in heatmap:            
            js+='d.push('+','.join([str(col) for col in row])+');\n'
            minrow=min(row)
            maxrow=max(row)            
            if minrow<gradmin:
                gradmin=minrow
            if maxrow>gradmax:
                gradmax=maxrow   
        js+='data.push(d);\n'

        return js


    def save_options_to_csv (self, args, outfile):
        optiefile=open(self.infodir+"/heatmaps/%s_meta.csv" % outfile,'wb')
        c=csv.writer(optiefile,delimiter=',')
        for k in sorted(args.keys()):
            c.writerow([k,args[k]])
        optiefile.close()

    def load_options_from_csv (self, infile):

        optiefile=open(self.infodir+"/heatmaps/%s_meta.csv" % infile,'r')
        c=csv.reader(optiefile,delimiter=',')
        args={}
        for row in c:
            key,value=row[0],row[1]

            try:
                value=ast.literal_eval(value)
            except:
                pass
            if value=='':
                value=None
            args[key]=value
        return args

    def opties_to_js (self, args):   # poor mans json encoder with proper formatting

        print 'opties_to_js'
        optiejs='opties.push({\n'
        for k in sorted(args.keys()):
            v=getattr(self,k)
            if v is None:
                optiejs+='"%s":null,\n' % (str(k))
                continue
            t=type(v)

            if (t==str) or (t==unicode):
                v=v.replace('\\','/')
                optiejs+='"%s":"%s",\n' % (str(k),v)
                continue
            if t==bool:
                if v:
                    optiejs+='"%s":true,\n' % (str(k))
                else:
                    optiejs+='"%s":false,\n' % (str(k))
                continue
            if isinstance(v, datetime.date):
                optiejs+='"%s":new Date("%s")\n,' % (str(k),v.isoformat())
                continue
            if t==dict:
                print 'dict'
                new_v={}
                dictstr=''
                for d_k,d_v in sorted(v.items(), key=operator.itemgetter(0)):
                    if type(d_v)==dict:
                        s='"%s":{' % str(d_k)
                        for dd_k,dd_v in sorted(d_v.items(), key=operator.itemgetter(0)):
                            if type(dd_v)==str or type(dd_v)==unicode:
                                s+="'%s':'%s'," % (str(dd_k),str(dd_v))
                            else:
                                s+="'%s':%s," % (str(dd_k),dd_v)
                        s+='}'
                        dictstr+=s
                        continue
                optiejs+='"%s":{%s},\n' % (str(k),dictstr)
                continue
            if t==list:
                optiejs+='"%s":[' % (str(k))
                for nr,el in enumerate(v):
                    eltype=type(el)
                    if eltype==dict:
                        s='{'                        
                        for d_k,d_v in sorted(el.items(), key=operator.itemgetter(0)):                            
                            if type(d_v)==str or type(d_v)==unicode:
                                s+='"%s":"%s",' % (str(d_k),str(d_v))
                            else:
                                s+='"%s":"%s",' % (str(d_k),d_v)
                        s=s[:-1]
                        s+='}'
                        print s
                    else:
                        s=str(el)
                    if nr==len(v)-1:
                        optiejs+=s 
                    else:
                        if eltype==dict:                        
                            optiejs+=s+',\n'
                        else:
                            optiejs+=s+','
                
                optiejs+='],\n'
                continue
                        
            optiejs+='"%s":%s,\n' % (str(k),str(v))

        optiejs=optiejs[:-1]+'});\n\n'
        return optiejs


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



    def parse_minmax_range(self, value, data_type, dateformat, minmax, min_date=None):
        datevalue=None
        if data_type=='nominal':
            value=float(value)
        else:
            datevalue=datetime.datetime.strptime(value,dateformat)	    	                
            if minmax=='min':
                value=0
            if minmax=='max':
                value=self.munge_date(datevalue, data_type, min_date)
        return value, datevalue





    def make_heatmap (self, args, heatmapnr=0):

        print 'make_heatmap'

        self.check_args(args)
        sep=self.sep       
        
        xcol=self.x_var.lower()
        xmin=self.x_min
        xmax=self.x_max
        xpixels=int(self.x_steps)

        ycol=self.y_var.lower()
        ymin=self.y_min
        ymax=self.y_max
        ypixels=int(self.y_steps)

        weight_var=self.weight_var
        
        x_data_type=self.x_data_type
        y_data_type=self.y_data_type
        x_dateformat=self.x_dateformat
        y_dateformat=self.y_dateformat
        
        xmin, xmin_date=self.parse_minmax_range(xmin, x_data_type, x_dateformat, 'min')
        xmax, xmax_date=self.parse_minmax_range(xmax, x_data_type, x_dateformat, 'max', xmin_date)
        ymin, ymin_date=self.parse_minmax_range(ymin, y_data_type, y_dateformat, 'min')
        ymax, ymax_date=self.parse_minmax_range(ymax, y_data_type, y_dateformat, 'max', ymin_date)
        
        self.xmin_date=xmin_date
        self.xmax_date=xmax_date
        self.ymin_date=ymin_date
        self.ymax_date=ymax_date
        
        
       
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
        

        if self.x_label is None:
            self.x_label=xcol
        if self.y_label is None:
            self.y_label=ycol            


        split1_var=self.split1_var
        split2_var=self.split2_var

        multimap=False
        if split1_var!='' or split2_var!='':
            multimap=True
        args['multimap']=multimap
        self.multimap=multimap

        if multimap:
            if split1_var!='':
                split1_labels=helpers.read_csv_dict ('%s/labels/%s.csv' % (self.infodir, split1_var))
                #split1_labels=sorted(split1_labels.iteritems())
                print split1_labels
            if split2_var!='':
                split2_labels=helpers.read_csv_dict ('%s/labels/%s.csv' % (self.infodir, split2_var))
                #split2_labels=sorted(split2_labels.iteritems())





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

            fx=open(self.infodir+'/split/%s.csv' % xcol)
            fy=open(self.infodir+'/split/%s.csv' % ycol)
            fweight=None
            if (weight_var is not None):
                fweight=open(self.infodir+'/split/%s.csv' % weight_var)
            linenr=0
            for x_txt, y_txt in zip (fx, fy):
                linenr+=1
                if linenr % 10000==0:
                    print linenr
                
                if self.convert_comma:
                    x_txt=x_txt.replace(',','.')
                    y_txt=y_txt.replace(',','.')

                val=1
                if weight_var is not None:
                    val=fweight.readline()

                if x_data_type=='nominal':
                    try:
                        x=float(x_txt)
                    except:
                        pass
                else:
                    x=datetime.datetime.strptime(x_txt,x_dateformat)
                    x=self.munge_date(x, x_data_type, xmin_date)

                if y_data_type=='nominal':
                    try:
                        y=float(y_txt)
                    except:
                        pass
                else:
                    y=datetime.datetime.strptime(y_txt,y_dateformat)
                    y=self.munge_date(y, y_data_type, ymin_date)


                if self.x_relative==True:
                    x_fullhist[x]=x_fullhist.get(x,0)+val
                if self.y_relative==True:
                    y_fullhist[y]=y_fullhist.get(y,0)+val


            fx.close()
            fy.close()
            if fweight is not None:
                fweight.close()


            
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

        
            

        xfactor= (xmax-xmin)/ (1.0*(xpixels-1))
        yfactor= (ymax-ymin)/ (1.0*(ypixels-1))


        linenr=0
        keys_x={}
        keys_y={}
        total=0
        xnullhist={}
        ynullhist={}

        fx=open('%s/split/%s.csv' % (self.infodir,xcol))
        fy=open('%s/split/%s.csv' % (self.infodir,ycol))
        fx.readline()
        fy.readline()
        fweight=None
        if (weight_var is not None):
            fweight=open('%s/split/%s.csv' % (self.infodir, weight_var))
            fweight.readline()
        split1file=None
        split2file=None
        if multimap:
            split1file=open('%s/split/%s.csv' % (self.infodir, split1_var))
            split1file.readline()
            if split2_var!='':
                split2file=open('%s/split/%s.csv' % (self.infodir, split2_var))
                split2file.readline()


        for x_txt, y_txt in zip (fx, fy):

            x_txt=x_txt.strip()
            y_txt=y_txt.strip()
            if self.convert_comma:
                x_txt=x_txt.replace(',','.')
                y_txt=y_txt.replace(',','.')
            linenr+=1
            if linenr % 10000==0:
                print linenr
            val=1
            if weight_var is not None:
                val=float(fweight.readline().strip())
            if split1file is not None:
                split1_data=split1file.readline().strip()
            if split2file is not None:
                split2_data=split2file.readline().strip()

                
            if x_data_type=='nominal':
                try:
                    x=float(x_txt)
                except:
                    xnull=xnullhist.get(x_txt,{})                    
                    xnull[y_txt]=xnull.get(y_txt,0)+val
                    xnullhist[x_txt]=xnull
                    x=None
            else:
                if x_txt!='':
                    x=datetime.datetime.strptime(x_txt,x_dateformat)
                else:
                    x=xmin_date
               # print x
                x=self.munge_date(x, x_data_type, xmin_date)
                #print x

            if y_data_type=='nominal':
                try:
                    y=float(y_txt)
                except:
                    ynull=ynullhist.get(y_txt,{})
                    ynull[x_txt]=ynull.get(x_txt,0)+val
                    ynullhist[x_txt]=ynull
                    y=None
            else:
                if y_txt!='':
                    y=datetime.datetime.strptime(y_txt,y_dateformat)
                else:
                    y=ymin_date
                y=self.munge_date(y, y_data_type, ymin_date)

            if x is None or y is None:
                continue
            
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

            
            if multimap:
                heatmapname=''
                if split2_var!='':
                    heatmapname=split1_data +'_'+ split2_data
                else:
                    heatmapname=split1_data
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
                continue
        

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

                 
        #print '%d records, %d bins filled, %d binvolume over img with %d pixels' % ( linenr, nonzerocount, total, xpixels*ypixels)
        #print 'coverage: %.3f%% max, %.3f%% actual' % (100.0*linenr/(xpixels*ypixels*1.0), 100.0*nonzerocount/(1.0*xpixels*ypixels))



# dump data
        js=''
        if multimap==False:
            js='var multimap=false;\nvar nr_heatmaps=1;\n\nvar data=[];\n'
    
        gradmin=self.heatmap[0][0]
        gradmax=gradmin

        if self.dump_csv:
            self.heatmap_to_csv (heatmap,self.outfile+'.csv')

        if multimap==True:
            datakeys=sorted(heatmaps.keys())
            js='var multimap=true;\n'
            js+='var data=[];\n'

            for datakey in datakeys:
                js+=self.heatmap_to_js (heatmaps[datakey])
            js+='var smalldata=[];\n'
            for datakey in datakeys:
                smallmap=self.aggegrate_by_4 (heatmaps[datakey])
                js_txt=self.heatmap_to_js (smallmap)
                js+=js_txt.replace('data','smalldata')


            js+='var multimap_labels='+json.dumps(self.multimap_labels)+';\n';
            

           # for filename in datakeys:
           #     print filename
           #     heatmap=heatmaps[filename]
           #     js+=self.heatmap_to_js (heatmap)
           #     self.heatmap_to_csv (heatmap,self.outfile+filename+'.csv')
                
            js+='var datakeys='+str(datakeys)+';\n'
        if multimap==False:
            js+=self.heatmap_to_js (self.heatmap)

        js+='var nr_heatmaps=data.length;\n\n'
        self.datamin=gradmin
        self.datamax=gradmax
        
        if getattr(self,'gradmax') is None:
            self.gradmax=gradmax        



        if heatmapnr==0:
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

        if heatmapnr==0:
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

        if heatmapnr==0:
            js+='var xmean=[];\n'
            js+='var ymean=[];\n'
        js+='var totalsum=%s;\n' % str(totalsum)
        js+='xmean.push(%s);\n' % str(float(sum(xsum))/len(xsum) )
        js+='ymean.push(%s);\n\n' % str(float(sum(xsum))/len(ysum) )
    

        if self.stats_enabled:   #mean
            if heatmapnr==0:
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
            if heatmapnr==0:
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
            if heatmapnr==0:
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


        self.js=self.js+js



        self.save_options_to_csv (args, self.outfile)



        optiejs=''
        if heatmapnr==0:
                optiejs='var opties=[];\n'

        if multimap:
            legend_labels={}
            for key in datakeys:
                args['multimap_title']=key
                self.multimap_title=key
                legend_labels[key]=key+':'+split1_labels.get(key,key)
                optiejs+=self.opties_to_js(args)
            legend_labels=sorted(legend_labels.iteritems())
            js+='var legend_labels='+cjson.encode(legend_labels)+';'
        else:
            optiejs+=self.opties_to_js(args)



        optiefile=open(self.infodir+"/heatmaps/%s_meta.js" % self.outfile,'w')
        optiefile.write(optiejs)
        optiefile.close()


        
        if heatmapnr==0:
            f=open(self.infodir+"/heatmaps/%s.js" % self.outfile,"w")
        else:
            f=open(self.infodir+"/heatmaps/%s.js"% self.outfile ,"a")
        f.write(js)
        f.close()
            
