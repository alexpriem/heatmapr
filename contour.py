import pyodbc
import argparse
from jinja2 import Environment, Template
from heatmapr.db import db





class contour:
    def __init__(self):
        pass




    def run_contour (dbc, hnd, args):
        server=args['server']
        database=args['database']
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
        exec_sql=True
        print_sql=False
        print debuglvl
        if debuglvl=='1':
            exec_sql=True
            print_sql=True
        if debuglvl=='2':
            exec_sql=False
            print_sql=True
        
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


        

        if xcol=='leeftijd':
            s="template_date_1"                     
        else:
            s="""template_int_1
            """ 

        sql=Template(s).render(locals())
        run_sql (dbc,hnd, sql, print_sql, exec_sql)

                
        s="template2"

        sql=Template(s).render(locals())
        run_sql (dbc,hnd, sql, print_sql, exec_sql)


        s="xas"

        sql=Template(s).render(locals())
        run_sql (dbc,hnd, sql, print_sql, exec_sql)
        s="yas"
        sql=Template(s).render(locals())
        run_sql (dbc,hnd, sql, print_sql, exec_sql)

        if selcol!='':
            s="sel"    
        sql=Template(s).render(locals())
        run_sql (dbc,hnd, sql, print_sql, exec_sql)    
        


        s="crossjoin"        
        sql=Template(s).render(locals())
        run_sql (dbc,hnd, sql, print_sql, exec_sql)
      #  hnd.execute(s)


        s="prep_contourtab"
        sql=Template(s).render(locals())
        run_sql (dbc,hnd, sql, print_sql, exec_sql)        

        s="index.sql" 
        sql=Template(s).render(locals())
        run_sql (dbc,hnd, sql, print_sql, exec_sql)





    def dump_data  (dbc, hnd, args):
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
        run_sql (dbc,hnd, sql, print_sql, exec_sql)
        rows=hnd.fetchall()

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

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-s','--server', dest='server', 
                    help='set server', required=True)
parser.add_argument('-db','--database', dest='database',  help='set database', required=True)
parser.add_argument('-t','--tabel', dest='tabel',  help='set tabel', required=True)
parser.add_argument('-x', dest='x',  help='set xaxis', required=True)
parser.add_argument('-y', dest='y',  help='set yaxis', required=True)
parser.add_argument('-o', dest='outfile',  help='set outfile', required=True)
parser.add_argument('-sel', dest='sel',  help='set selection', required=False)
parser.add_argument('-debug', dest='debug',  help='1: print/execute; 2:print, do not execute sql', required=False)

args=vars(parser.parse_args())
server=args['server']
database=args['database']

dbc, hnd=open_server(server, database)
run_contour(dbc, hnd, args)
dump_data (dbc, hnd, args)

