from scipy import misc
import sys
import datetime

# tricolor.png is een 500x500 png
p = misc.imread('data\\tricolor.png')
s = misc.imread('data\\shapes.png')

def example_simple(f):
    f.write('x,y\n')
    for i in range(0,500):
        for j in range(0,500):
            val=(255-sum(p[i,j][0:3])/3)/20
            if val<=1:
                continue            
            for k in range(0,val):
                f.write('%.1f,%d\n' % (i/10.0,j*10))

def example_weight(f):
    f.write('x,y,num\n')
    for i in range(0,500):
        for j in range(0,500):
            val=255-sum(p[i,j][0:3])/3
            if val<=20:
                continue
            val=val/20
            f.write('%.1f,%d,%d\n' % (i/10.0,j*10,val))


def example_x_date_year(f):
    f.write('x,y,num\n')
    for i in range(0,500):
        for j in range(0,500):
            val=255-sum(p[i,j][0:3])/3
            if val<=20:
                continue
            val=val/20
            d=datetime.datetime(1900+i/5,1,1)
            f.write('%d,%d,%d\n' % (d.year,j*10,val))


def example_x_date_YMD(f):
    f.write('x,y,num\n')
    for i in range(0,500):
        for j in range(0,500):
            val=255-sum(p[i,j][0:3])/3
            if val<=20:
                continue
            val=val/20
            d=datetime.date(2010,1,1)+datetime.timedelta(days=i)            
            s=datetime.date.strftime(d,'%Y-%m-%d')
            f.write('%s,%d,%d\n' % (s,j*10,val))


def example_xy_date_YMD(f):
    f.write('x,y,num\n')
    for i in range(0,500):
        for j in range(0,500):
            val=255-sum(p[i,j][0:3])/3
            if val<=20:
                continue
            val=val/20
            d=datetime.date(2010,1,1)+datetime.timedelta(days=i)
            s=datetime.date.strftime(d,'%Y-%m-%d')
            d=datetime.date(2010,1,1)+datetime.timedelta(days=j)
            s2=datetime.date.strftime(d,'%Y-%m-%d')
            f.write('%s,%s,%d\n' % (s,s2,val))


funcs=[example_xy_date_YMD,
        example_x_date_YMD,        
      #  example_x_date_year,
     #   example_simple,
    #    example_weight,        
        ]

for f in funcs:
    print f.__name__
    g=open('data\\%s.csv' % f.__name__,'w')
    f(g)
    g.close()

