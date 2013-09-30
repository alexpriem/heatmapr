import math


width=250
height=250
minval=0;
maxval=int(math.sqrt(height*height/4+width*width/4)+5);


xmin=10
xmax=20

ymin=20
ymax=50

f=open("js/data.js","w")
f.write("""
var width=%(width)s;
var height=%(height)s;

var minval=%(minval)s;
var maxval=%(maxval)s;

var xmin=%(xmin)s;
var xmax=%(xmax)s;

var ymin=%(ymin)s;
var ymax=%(ymax)s;

var data=[
""" % locals())



for i in range(1,height+1):
    a=[]
    for j in range(1,width+1):
        if ((i==1) | (i==height) | (j==1) | (j==width)) :
            val=str(maxval);
        else:
            ii=i-height/2;
            jj=j-width/2;
            offs=math.sqrt(height*height/4+width*width/4);
            val=int(offs-math.sqrt(ii*ii*0.2+jj*jj*0.5))
            val=str(val)
        a.append(val)
    s=','.join(a)
    if i!=height:
        s+=','
    s='\t'+s+'\n'
    f.write(s)
f.write("];\n");

f.close()
    
    
            
        

