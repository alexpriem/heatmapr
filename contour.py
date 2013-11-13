import pyodbc
import argparse
from jinja2 import Environment, Template


class dbconnection:
    def __init__ (self,metadict):
        self.print_sql=True
        self.exec_sql=True
        self.open_server(metadict)

        
    def open_server (self, metadict):
        if metadict.get('username') is not None:
            s='Driver={%(driver)s};SERVER=%(server)s;DATABASE=%(database)s;uid=%(username)s;pwd=%(password)s' % metadict
        else:
            s='Driver={%(driver)s};SERVER=%(server)s;DATABASE=%(database)s' % metadict
        dbc = pyodbc.connect(s)     # open a database connection
        dbc.autocommit=True
        hnd=dbc.cursor()
        self.dbc=dbc
        self.hnd=hnd
        self.driver=metadict['driver']
        self.server=metadict['server']
        self.database=metadict['database']
        return dbc, hnd


    def run_sql (self, sql):        
        if self.print_sql:
            print sql
  
        if self.exec_sql:            
            self.hnd.execute(sql)
            self.dbc.commit()




class contour:
    def __init__(self):
        pass


    def setup_numbers (self):
        f=open("numbers.csv","w")
        for num in range(10000):
            f.write("%d\n" % num)
        f.close()
        
                    

    def run_contour (self, db_obj, args):
        tabel=args['tabel']
        x=args['x'].split(',')
        if len(x)!=4:
            raise RuntimeError ("-x: expected col, min,max, steps, got %x", str(x))
        y=args['y'].split(',')
        if len(x)!=4:
            raise RuntimeError ("-y: expected col, min,max, steps")
        xcol,xmin, xmax, xpixels=[xx.strip() for xx in x]
        ycol,ymin, ymax, ypixels=y=[yy.strip() for yy in y]


        debuglvl=args.get('debug','')
        db_obj.exec_sql=True
        db_obj.print_sql=True #False
        #print debuglvl
        if debuglvl=='1':
            db_obj.exec_sql=True
            db_obj.print_sql=True
        if debuglvl=='2':
            db_obj.exec_sql=False
            db_obj.print_sql=True

        
        
        selcol=args.get('sel','')
        #selcol=','+sel

        xmin=int(xmin)
        xmax=int(xmax)
        xpixels=int(xpixels)

        ymin=int(ymin)
        ymax=int(ymax)
        ypixels=int(ypixels)

        xfactor= (xmax-xmin)/ (1.0*xpixels)
        yfactor= (ymax-ymin)/ (1.0*ypixels)
        xfactorinv= (1.0*xpixels)/(xmax-xmin)
        yfactorinv= (1.0*ypixels)/(ymax-ymin)

        self.setup_numbers()
        
        if xcol=='leeftijd':
            s="01_template1_date"                     
        else:
            s="01_template1_int"
            
        sqltemplates=[
            "00_setup_numbers",
            s,
            "02_template2",
            "03_xas",
            "04_yas",
            "05_crossjoin",
            "06_prep_contourtab",
            "07_index"]
        if args['dbtype']=='mssql':
            postfix='_mssql.sql'
        if args['dbtype']=='psql':
            postfix='_psql.sql'
        self.postfix=postfix

        for t in sqltemplates:        
            s=open("templates/"+t+postfix).read()
            sql=Template(s).render(locals())            
            db_obj.run_sql (sql)        


    def dump_data  (self, db_obj, args):
        
        x=args['x'].split(',')
        if len(x)!=4:
            raise RuntimeError ("-x: expected col, min,max, steps, got %x", str(x))
        y=args['y'].split(',')
        if len(x)!=4:
            raise RuntimeError ("-y: expected col, min,max, steps")
        xcol,xmin, xmax, xpixels=[xx.strip() for xx in x]
        ycol,ymin, ymax, ypixels=y=[yy.strip() for yy in y]

        xmin=int(xmin)
        xmax=int(xmax)
        xpixels=int(xpixels)

        ymin=int(ymin)
        ymax=int(ymax)
        ypixels=int(ypixels)

        xfactor= (xmax-xmin)/ (1.0*xpixels)
        yfactor= (ymax-ymin)/ (1.0*ypixels)
        outfile=args['outfile']

        sql_tmpl=open("templates/10_dumpdata"+self.postfix).read()
        
        sql=Template(sql_tmpl).render(locals())
        db_obj.run_sql (sql)
        rows=db_obj.hnd.fetchall()

               
        js="var data=["

        gradmin=rows[0][0]
        gradmax=rows[0][0]
        prevx=None            
        #firstrow=True
        s=''
        for row in rows:
           # print row[0],row[1],row[2]
            x=row[1]        
            if prevx is not None and x>prevx:         
                js+=s+'\n'
                s=''
            s+="%d," % row[2]
            if row[2]<gradmin:
                gradmin=row[2]
            if row[2]>gradmax:
                gradmax=row[2]        
            prevx=x                    
        js+=s[:-1]+'];\n\n'
        
        if args['gradmax'] is None:
            args['gradmax']=gradmax
        if args['xlabel'] is None:
            args['xlabel']=xcol
        if args['ylabel'] is None:
            args['ylabel']=ycol            
        args['xmin']=xmin
        args['ymin']=ymin
        args['xmax']=xmax
        args['ymax']=ymax
        args['xpixels']=xpixels
        args['ypixels']=ypixels
        
        vlist=['gradmin','gradmax',
               'xmin','xmax',
               'ymin','ymax',
               'xpixels','ypixels',
               'imgwidth','imgheight',               
               'xlabel','ylabel','title']
        for k in vlist:
            v=args[k]
            try:
                v2=int(v)
            except:
                if v2 is None:
                    v=''                    
                js+='var %s="%s";\n' % (k,v)
            else:
                js+="var %s=%s;\n" % (k,v)
        
        return js


    def write_data (self, js,args):

        outfile=args['outfile']        
        if args['dump_js']:
            f=open(outfile+'.js','w')
            f.write(js)
            f.close()
        if args['dump_html']:
            html=open ("bitmap.html",'r').read()
            
            g=open(outfile+'.html','w')
            cssfrags=html.split('<link href="')
            g.write(cssfrags[0])
            for cssfrag in cssfrags[1:]:
                cssfile=cssfrag.split('"')
               # print cssfile[0]
                g.write('\n<style>\n')
                css=open(cssfile[0],"r").read()
                g.write(css)
                g.write('\n</style>\n')

            g.write('\n<script type="text/javascript">\n')            
            g.write(js)
            g.write('\n</script>\n')
            
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
parser.add_argument('-dbt','--dbtype', dest='dbtype',  help='set databasetype: psql/mssql', required=True)
parser.add_argument('-s','--server', dest='server', 
                    help='set server', required=True)
parser.add_argument('-db','--database', dest='database',  help='set database', required=True)
parser.add_argument('-u', dest='username',  help='set username', required=False)
parser.add_argument('-p', dest='password',  help='set password', required=False)
parser.add_argument('-t','--tabel', dest='tabel',  help='set tabel', required=True)

parser.add_argument('-x', dest='x',  help='define xaxis:columnname, min, max, steps', required=True)
parser.add_argument('-y', dest='y',  help='define yaxis:columnname, min, max, steps', required=True)
parser.add_argument('-gradmin', dest='gradmin',  help='define minimum gradient, default 0', required=False, default=0)
parser.add_argument('-gradmax', dest='gradmax',  help='define maximum gradient, default max value in heatmap', required=False)

parser.add_argument('-imgwidth', dest='imgwidth',  help='set img width (default 500)', required=False, default=500)
parser.add_argument('-imgheight', dest='imgheight',  help='set img height (default 500)', required=False, default=500)

parser.add_argument('-xlabel', dest='xlabel',  help='set xlabel; default x variable', required=False)
parser.add_argument('-ylabel', dest='ylabel',  help='set ylabel; default y variable', required=False)
parser.add_argument('-title', dest='title',  help='set title', required=False)

parser.add_argument('-o', dest='outfile',  help='set outfile', required=True)
parser.add_argument('-html', dest='dump_html',  help='html output', required=False, default=True, action='store_true')
parser.add_argument('-nohtml', dest='dump_html',  help='html output', required=False, action='store_false')
parser.add_argument('-js', dest='dump_js',  help='javascript ouput', required=False, default=False, action='store_true')
parser.add_argument('-nojs', dest='dump_js',  help='javascript output', required=False, action='store_false')
parser.add_argument('-sel', dest='sel',  help='set selection', required=False)
parser.add_argument('-debug', dest='debug',  help='1: print/execute; 2:print, do not execute sql', required=False)

args=vars(parser.parse_args())


args['driver']='PostgreSQL ODBC Driver(ANSI)'
db_obj=dbconnection(args)

c=contour()

c.run_contour(db_obj, args)
js=c.dump_data (db_obj, args)
c.write_data(js, args)

