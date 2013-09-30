import pyodbc
import argparse







def open_server (server, database):
    s='Driver={SQL Server}; SERVER=%s;DATABASE=%s' % (server, database)
    dbc = pyodbc.connect(s)     # open a database connection
    dbc.autocommit=True
    hnd=dbc.cursor()
    return dbc, hnd






def run_sql (args,hnd):
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

        select  %(xcol)s=round(datediff(day,%(xcol)s,'20120101')/365.0*%(xfactorinv)s,0)/%(xfactorinv)s, 
                %(ycol)s=round(%(ycol)s/%(yfactor)s,0)* %(yfactor)s,
                num
                into selectie
                from %(tabel)s""" % locals ()
    else:
        s="""
        IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'selectie') AND type in (N'U'))
        DROP TABLE selectie

        select  %(xcol)s=round(%(xcol)s/ %(xfactor)s,0)* %(xfactor)s, 
                %(ycol)s=round(%(ycol)s/ %(yfactor)s,0)* %(yfactor)s,
                num
                into selectie
                from %(tabel)s""" % locals ()

    print s
    hnd.execute(s)
    dbc.commit()

            
    s="""
    IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'selectie2') AND type in (N'U'))
    DROP TABLE selectie2

    select %(xcol)s, %(ycol)s, num=sum(num)
            into selectie2
            from selectie
            group by %(xcol)s, %(ycol)s	
    """ % locals()
    print s
    hnd.execute(s)


    s="""
    IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'xas') AND type in (N'U'))
    DROP TABLE xas

    select %(xcol)s=number* %(xfactor)s
          into xas
          from numbers
        where number>(%(xmin)s / %(xfactor)s) and number<=(%(xmax)s / %(xfactor)s)
    """  % locals()
    print s
    hnd.execute(s)

    s="""
    IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'yas') AND type in (N'U'))
    DROP TABLE yas

    select %(ycol)s=number* %(yfactor)s
            into yas
            from numbers
            where number>(%(ymin)s  / %(yfactor)s) and number<=(%(ymax)s / %(yfactor)s)
    """ % locals()
    print s
    hnd.execute(s)

    s="""
    IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'xy') AND type in (N'U'))
    DROP TABLE xy

    select a.*, b.*
            into xy
            from xas a
            cross join yas b
    """ % locals()
    print s
    hnd.execute(s)


    s="""
    IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'contourtab') AND type in (N'U'))
    DROP TABLE contourtab

    select a.%(xcol)s, a.%(ycol)s, num=isnull(b.num,0)
            into contourtab
            from xy a
            left join selectie2  b
            on a.%(xcol)s=b.%(xcol)s and a.%(ycol)s=b.%(ycol)s
    """ % locals()
    print s
    hnd.execute(s)

    s="""
    create clustered index i1 on  contourtab(%(xcol)s, %(ycol)s)
    """  % locals()
    print s
    hnd.execute(s)





def dump_data  (args, hnd):
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

    s="""select %(xcol)s, %(ycol)s, num
        from contourtab
        order by 1, 2""" % locals()

    hnd.execute(s)
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
    var width=%(width)s;
    var height=%(height)s;
    
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



args=vars(parser.parse_args())
server=args['server']
database=args['database']

dbc, hnd=open_server(server, database)
run_sql(args, hnd)
dump_data (args, hnd)

