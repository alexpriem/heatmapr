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
            s="""
            IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'selectie') AND type in (N'U'))
            DROP TABLE selectie

            select  {{xcol}}=round(datediff(day,{{xcol}},'20120101')/365.0*{{xfactorinv}},0)/{{xfactorinv}}, 
                    {{ycol}}=round({{ycol}}/{{yfactor}},0)* {{yfactor}}
                    {% if selcol %}
                     , {{selcol}} 
                    {% endif %}    
                    into selectie
                    from {{tabel}}""" 
            
        else:
            s="""
            IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'selectie') AND type in (N'U'))
            DROP TABLE selectie

            select  {{xcol}}=round({{xcol}}/ {{xfactor}},0)* {{xfactor}}, 
                    {{ycol}}=round({{ycol}}/ {{yfactor}},0)* {{yfactor}}
                    {% if selcol %}
                     , {{selcol}} 
                    {% endif %}
                    into selectie
                    from {{tabel}}""" 

        sql=Template(s).render(locals())
        run_sql (dbc,hnd, sql, print_sql, exec_sql)

                
        s="""
        IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'selectie2') AND type in (N'U'))
        DROP TABLE selectie2

        select {{xcol}},
                {{ycol}},
                {% if selcol %}
                {{selcol}},
                {% endif %}
                num=count(*)
                into selectie2
                from selectie
                group by {{xcol}}, {{ycol}}
                {% if selcol %}
                , rollup({{selcol}})
                {% endif %}
        """ 

        sql=Template(s).render(locals())
        run_sql (dbc,hnd, sql, print_sql, exec_sql)


        s="""
        IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'xas') AND type in (N'U'))
        DROP TABLE xas

        select distinct {{xcol}}=number * {{xfactor}}
              into xas
              from numbers
            where number>({{xmin}} / {{xfactor}}) and number<=({{xmax}} / {{xfactor}})
        """  

        sql=Template(s).render(locals())
        run_sql (dbc,hnd, sql, print_sql, exec_sql)
        s="""
        IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'yas') AND type in (N'U'))
        DROP TABLE yas

        select distinct {{ycol}}=number* {{yfactor}}
                into yas
                from numbers
                where number>({{ymin}}  / {{yfactor}}) and number<=({{ymax}} / {{yfactor}})
        """
        sql=Template(s).render(locals())
        run_sql (dbc,hnd, sql, print_sql, exec_sql)

        if selcol!='':
            s="""
        IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'sel') AND type in (N'U'))
        DROP TABLE sel;

        select distinct {{selcol}} into sel from selectie2"""    
        sql=Template(s).render(locals())
        run_sql (dbc,hnd, sql, print_sql, exec_sql)    
        


        if selcol=='':
            s="""
        IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'xy') AND type in (N'U'))
        DROP TABLE xy

        select a.*, b.*
                into xy
                from xas a
                cross join yas b            
        """ 
        else:
            s="""
        IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'xy') AND type in (N'U'))
        DROP TABLE xy

        select a.*, b.*--, c.*
                into xy 
                from xas a
                cross join yas b            
             --   cross join sel c
        """     
        sql=Template(s).render(locals())
        run_sql (dbc,hnd, sql, print_sql, exec_sql)
      #  hnd.execute(s)


        s="""
        IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'contourtab') AND type in (N'U'))
        DROP TABLE contourtab

        select a.{{xcol}},
                a.{{ycol}},
                {% if selcol %}
                b.{{selcol}},
                {% endif %}
                num=isnull(b.num,0)
                into contourtab
                from xy a
                left join selectie2  b
                on a.{{xcol}}=b.{{xcol}} and a.{{ycol}}=b.{{ycol}}
                {% if selcol %}
                and a.{{selcol}}=b.{{selcol}}
                {% endif %}
        """     
        sql=Template(s).render(locals())
        run_sql (dbc,hnd, sql, print_sql, exec_sql)        

        s="""{% if selcol %} 
            create clustered index i1 on  contourtab( {{selcol}}, {{xcol}}, {{ycol}})    
            {% else %}
            create clustered index i1 on  contourtab( {{xcol}}, {{ycol}})    
            {% endif %}
        """
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

