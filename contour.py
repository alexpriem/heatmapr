import pyodbc
import argparse
from jinja2 import Environment, Template
import db





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

        s=open("templates/10_dumpdata"+self.postfix).read()
        
        sql=Template(s).render(locals())
        db_obj.run_sql (sql)
        rows=db_obj.hnd.fetchall()
      
        f=open("js/data.js","w")        
        f.write("var data=[")

        gradmin=rows[0][0]
        gradmax=rows[0][0]
        prevx=None            
        #firstrow=True
        s=''
        for row in rows:
           # print row[0],row[1],row[2]
            x=row[1]        
            if prevx is not None and x>prevx:         
                f.write(s+'\n')
                s=''
            s+="%d," % row[2]
            if row[2]<gradmin:
                gradmin=row[2]
            if row[2]>gradmax:
                gradmax=row[2]        
            prevx=x                    
        f.write(s[:-1]+'];\n\n')
        
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
                f.write('var %s="%s";\n' % (k,v))
            else:
                f.write("var %s=%s;\n" % (k,v))
        
        f.close();

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
parser.add_argument('-sel', dest='sel',  help='set selection', required=False)
parser.add_argument('-debug', dest='debug',  help='1: print/execute; 2:print, do not execute sql', required=False)

args=vars(parser.parse_args())


args['driver']='PostgreSQL ODBC Driver(ANSI)'
db_obj=db.dbconnection(args)

c=contour()

c.run_contour(db_obj, args)
c.dump_data (db_obj, args)

