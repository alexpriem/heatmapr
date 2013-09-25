
f=open("colormaps.js","w")
f.write("var colormap=[")
for i in range(0,256):
    red=i
    green=i
    blue=i
    f.write("\n\t[%(red)s,%(green)s,%(blue)s]" % locals())
    if(i!=255):
        f.write(",")
f.write("];\n");
f.close()
            
            
