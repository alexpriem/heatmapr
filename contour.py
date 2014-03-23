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

    def run_contour (self, args):
        infile=args['infile']
        x=args['x'].split(',')
        if len(x)!=4:
            raise RuntimeError ("-x: expected col, min,max, steps, got %x", str(x))
        y=args['y'].split(',')
        if len(x)!=4:
            raise RuntimeError ("-y: expected col, min,max, steps")
        xcol,xmin, xmax, xpixels=[xx.strip() for xx in x]
        ycol,ymin, ymax, ypixels=y=[yy.strip() for yy in y]

        logx=args['logx']
        logy=args['logy']

        xmin=int(xmin)
        xmax=int(xmax)
        xpixels=int(xpixels)
        if logx:            
            xmin=safelog10(xmin)
            xmax=safelog10(xmax)

        ymin=int(ymin)
        ymax=int(ymax)
        ypixels=int(ypixels)
        if logy:            
            ymin=safelog10(ymin)
            ymax=safelog10(ymax)

        xfactor= (xmax-xmin)/ (1.0*xpixels)
        yfactor= (ymax-ymin)/ (1.0*ypixels)
        xfactorinv= (1.0*xpixels)/(xmax-xmin)
        yfactorinv= (1.0*ypixels)/(ymax-ymin)

        args['xmin']=xmin
        args['ymin']=ymin
        args['xmax']=xmax
        args['ymax']=ymax
        args['xpixels']=xpixels
        args['ypixels']=ypixels

        if args['xlabel'] is None:
            args['xlabel']=xcol
        if args['ylabel'] is None:
            args['ylabel']=ycol            

        heatmap=[[0]*xpixels for i in range(ypixels)]

        sep=args['sep']

        fuzzx=float(args['fuzzx'])
        fuzzy=float(args['fuzzy'])


        linenr=0
        f=open(infile)
        line=f.readline()
        cols=line.split(sep)
        numcols=len(cols)
        #f.seek(0)
        
        for line in f:
            linenr+=1
            if linenr % 10000==0:
                print linenr
            
            cols=line.split(sep)
            x=float(cols[0])
            y=float(cols[1])
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
            if (y>ymin and y<ymax):
                hy=int((y-ymin)/yfactor)
                if fuzzy!=0:
                    hy+=int(random.random()*fuzzy)
            else:
                continue
           # print x,y,hx,hy
            heatmap[hx][hy]+=val

        self.heatmap=heatmap
            

    def dump_data  (self, args):
        
        outfile=args['outfile']
               
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


        args['datamin']=gradmin
        args['datamax']=gradmax
        
        if args['gradmax'] is None:
            args['gradmax']=gradmax
        
        
        vlist=['gradmin','gradmax','gradsteps',
               'datamin','datamax',
               'xmin','xmax','logx',
               'ymin','ymax','logy',
               'xpixels','ypixels',
               'imgwidth','imgheight',               
               'xlabel','ylabel','title']
        for k in vlist:
            v=args[k]
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

        if args['dump_js']:
            f=open(outfile+'.js','w')
            f.write(js)
            f.close()        

#        self.js=js
        f=open("js/data.js","w")
        f.write(js)
        f.close()
        


    def write_html (self, args):

        outfile=args['outfile']        
        if args['dump_html']:
            html=open ("bitmap.html",'r').read()
            
            g=open(outfile+'.html','w')
            cssfrags=html.split('<link href="')
            g.write(cssfrags[0])
            cssfiles=[cssfrag.split('"')[0] for cssfrag in cssfrags[1:]]            

            for cssfrag in cssfrags[1:]:
                cssfile=cssfrag.split('"')
                
               # print cssfile[0]
                g.write('\n<style>\n')
                css=open(cssfile[0],"r").read()
                g.write(css)
                g.write('\n</style>\n')

#            g.write('\n<script type="text/javascript">\n')            
#            g.write(self.js)
#            g.write('\n</script>\n')
            
            jsfrags=html.split('script src="')            
            for jsfrag in jsfrags[1:]:
                jsfile=jsfrag.split('"')
              #  print jsfile[0]
                g.write('\n<script type="text/javascript">\n')
                js=open(jsfile[0],'r').read()    
                g.write(js)
                g.write('\n</script>\n')

            body=html.split("<body>")

            g.write("</head>\n")
            g.write("<body>\n")
            g.write(body[1])
            g.close()



parser = argparse.ArgumentParser(description='generate javascript contourdata from db.')

parser.add_argument('-f','--file', dest='infile',  help='inputfile (csv)', required=True)
parser.add_argument('-sep', dest='sep',  help='seperator (default ;)', required=False, default=';')

parser.add_argument('-x', dest='x',  help='define xaxis:columnname, min, max, steps', required=True)
parser.add_argument('-y', dest='y',  help='define yaxis:columnname, min, max, steps', required=True)

parser.add_argument('-fuzzx', dest='fuzzx',  help='x-pixel fuzz (default 0)', required=False, default=0)
parser.add_argument('-fuzzy', dest='fuzzy',  help='y-pixel fuzz (default 0)', required=False,default=0)
parser.add_argument('-logx', dest='logx',  help='log x axis', required=False, default=False, action='store_true')
parser.add_argument('-logy', dest='logy',  help='log y axis', required=False, default=False, action='store_true')

parser.add_argument('-gradmin', dest='gradmin',  help='define minimum gradient, default 0', required=False, default=0)
parser.add_argument('-gradmax', dest='gradmax',  help='define maximum gradient, default max value in heatmap', required=False)
parser.add_argument('-gradsteps', dest='gradsteps',  help='define nr of steps in gradient, default 255', required=False, default=255)

parser.add_argument('-imgwidth', dest='imgwidth',  help='set img width (default 500)', required=False, default=500)
parser.add_argument('-imgheight', dest='imgheight',  help='set img height (default 500)', required=False, default=500)

parser.add_argument('-xlabel', dest='xlabel',  help='set xlabel; default x variable', required=False)
parser.add_argument('-ylabel', dest='ylabel',  help='set ylabel; default y variable', required=False)
parser.add_argument('-title', dest='title',  help='set title', required=False)

parser.add_argument('-o', dest='outfile',  help='set outfile', required=True)
parser.add_argument('-html', dest='dump_html',  help='html output', required=False, default=True, action='store_true')
parser.add_argument('-nohtml', dest='dump_html',  help='html output', required=False, action='store_false')
parser.add_argument('-js', dest='dump_js',  help='javascript output', required=False, default=False, action='store_true')
parser.add_argument('-nojs', dest='dump_js',  help='javascript output', required=False, action='store_false')
parser.add_argument('-sel', dest='sel',  help='set selection', required=False)

parser.add_argument('-debug', dest='debug',  help='1: print/execute; 2:print, do not execute sql', required=False)

args=vars(parser.parse_args())

c=contour()

c.run_contour(args)
c.dump_data (args)
c.write_html(args)

