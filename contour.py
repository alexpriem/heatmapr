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

        for t in sqltemplates:        
            s=open("templates/"+t+postfix).read()
            sql=Template(s).render(locals())
            print sql
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


        debuglvl=args.get('debug','')
        exec_sql=True
        print_sql=False
        if debuglvl=='1':
            exec_sql=True
            print_sql=True
        if debuglvl=='2':
            exec_sql=False
            print_sql=True

        s="""select {{xcol}}, 
                    {{ycol}}, 
                    {% if selcol %}
                    {{selcol}},
                    {% endif %}
                    num
            from contourtab
            order by 3, 1, 2"""

        sql=Template(s).render(locals())
        db_obj.run_sql (sql)
        rows=db_obj.hnd.fetchall()

      #  rows=rows[10]
        prevx=None
        prevy=None
        s=''
    #    f=open(outfile,'w')
        width=xpixels;
        height=ypixels;
        
        f=open("js/data.js","w")
        f.write("""
        var width={{width}};
        var height={{height}};
        
        var data=[""" % locals())
        

        minval=rows[0][0]
        maxval=rows[0][0]

        firstrow=True
        for row in rows:        
            y=row[0]        
            if prevy is not None and y>prevy:
                if firstrow==True:
                    f.write(s[1:]+'\n')
                    firstrow=False
                f.write(s+'\n')
                s=''
            s+=",%d" % row[2]
            if row[2]<minval:
                minval=row[2]
            if row[2]>maxval:
                maxval=row[2]        
            prevy=y                    
        f.write(s+'];\n')

        f.write("var minval=%(minval)s;\n" % locals())
        f.write("var maxval=%(maxval)s;\n" % locals())

        f.close();

parser = argparse.ArgumentParser(description='generate javascript contourdata from db.')
parser.add_argument('-dbt','--dbtype', dest='dbtype',  help='set databasetype: psql/mssql', required=True)
parser.add_argument('-s','--server', dest='server', 
                    help='set server', required=True)
parser.add_argument('-db','--database', dest='database',  help='set database', required=True)
parser.add_argument('-t','--tabel', dest='tabel',  help='set tabel', required=True)
parser.add_argument('-x', dest='x',  help='set xaxis', required=True)
parser.add_argument('-y', dest='y',  help='set yaxis', required=True)
parser.add_argument('-o', dest='outfile',  help='set outfile', required=True)
parser.add_argument('-u', dest='username',  help='set username', required=False)
parser.add_argument('-p', dest='password',  help='set password', required=False)
parser.add_argument('-sel', dest='sel',  help='set selection', required=False)
parser.add_argument('-debug', dest='debug',  help='1: print/execute; 2:print, do not execute sql', required=False)

args=vars(parser.parse_args())


args['driver']='PostgreSQL ODBC Driver(ANSI)'
db_obj=db.dbconnection(args)

c=contour()

c.run_contour(db_obj, args)
c.dump_data (db_obj, args)

