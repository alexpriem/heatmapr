import sys, array


def parse_header (headerfile):
    f=open(headerfile,'r')
    filename=f.readline().split('=')[1].strip()
    sep=f.readline().split('=')[1].strip()
    cols=[]
    cols=[col.strip().lower() for col in f]
    f.close()
    return filename, sep, cols


def parse_header2 (header2file):
    f=open(header2file,'r')
    filename=f.readline().split('=')[1].strip()
    sep=f.readline().split('=')[1].strip()
    cols=[]
    types=[]
    subtypes=[]
    typecodes=[]
    minvals=[]
    maxvals=[]
   # c=[col.strip().split(',') for col in f]
   # print c
    lines=[col.strip().split(',') for col in f]
    for line in lines:
        cols.append(line[0].lower())
        types.append(line[1])
        subtypes.append(line[2])
        typecodes.append(line[3])
        minvals.append(line[4])
        maxvals.append(line[5])
    
    f.close()
    return filename, sep, cols, types, subtypes, typecodes, minvals, maxvals




headerfile=sys.argv[1]
#filename, sep, cols=parse_header(headerfile)
filename, sep, cols, types, subtypes, typecodes, minvals, maxvals=parse_header2(headerfile+'2')

s="""
var_x=sys.argv[2]
var_y=sys.argv[3]

min_x=float(sys.argv[4])
max_x=float(sys.argv[5])
min_y=float(sys.argv[6])
max_y=float(sys.argv[7])
"""

var_x='LFT'
var_y='BELIB1'
min_x=18
max_x=65
min_y=17600
max_y=19000

#min_y=53400
#max_y=55200

var_x=var_x.lower()
var_y=var_y.lower()

#print filename, sep, cols
xcolnr=cols.index(var_x)
ycolnr=cols.index(var_y)
print cols[xcolnr], typecodes[xcolnr]
print cols[ycolnr], typecodes[ycolnr]

xdata=array.array(typecodes[xcolnr])
ydata=array.array(typecodes[ycolnr])
f=open('splitbin\\%s.fullbin' % var_x, 'rb' )
g=open('splitbin\\%s.fullbin' % var_y ,'rb')
h=open('selectie_%s_%s.csv' % (var_x, var_y),'w')

xdata.fromstring(f.read())
ydata.fromstring(g.read())
xdata=xdata.tolist()
ydata=ydata.tolist()
j=0
print ydata[0:25]
print ydata[0:25]
print len(xdata), len(ydata)
for i,(x,y) in enumerate(zip(xdata,ydata)):
    #print x,y
    if (i % 100000)==0:
        print i,j, x,y
    if ((x>min_x) and (x<max_x)) and ((y>min_y) and (y<max_y)):
        
        h.write('%d\n' % i)
        j+=1

f.close()
g.close()
h.close()


        

