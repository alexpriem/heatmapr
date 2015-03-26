from scipy import misc
import sys
import datetime
from collections import Counter

# tricolor.png is een 500x500 png

p = misc.imread('data\\tricolor.png')
s = misc.imread('data\\shapes.png')



def example_split1(f):
    f.write('x,y,color1,color2\n')
    cnt=Counter()
    for i in range(0,500):
        for j in range(0,500):
            c=p[i,j]
            val=(255-sum(c[0:3])/3)/20            
            if val<=1:
                continue
            red=c[0]
            grn=c[1]
            blu=c[2]
            
            if (red>grn) and (red>blu):                
                color=1
            if (grn>red) and (grn>blu):                
                color=2
            if (blu>red) and (blu>grn):                
                color=3                
            if val>9:
                color=5
            if blu==red and grn==blu:
                color=6
            if blu==red and grn==blu and blu==158:
                color=7                
            color2=0
            if color==1 or color==2 or color==3:
                color2=1          
            cnt[color]+=1
            for k in range(0,val):
                f.write('%.1f,%d,%d,%d\n' % (i/10.0,j*10,color,color2))

def example_split2(f):
    f.write('x,y\n')
    for i in range(0,500):
        for j in range(0,500):
            val=(255-sum(p[i,j][0:3])/3)/20
            if val<=1:
                continue            
            for k in range(0,val):
                f.write('%.1f,%d\n' % (i/10.0,j*10))




def example_fixed(f):
    f.write('   x    y\n')
    for i in range(0,500):
        for j in range(0,500):
            val=(255-sum(p[i,j][0:3])/3)/20
            if val<=1:
                continue            
            for k in range(0,val):
                f.write('%4.1f %4d\n' % (i/10.0,j*10))


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


funcs=[example_fixed,
        #example_split1,
    #example_xy_date_YMD,
      #  example_x_date_YMD,        
      #  example_x_date_year,
     #   example_simple,
    #    example_weight,        
        ]

for f in funcs:
    print f.__name__
    g=open('data\\%s.csv' % f.__name__,'w')
    f(g)
    g.close()

