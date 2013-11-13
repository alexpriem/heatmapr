from pylab import *
from numpy import outer
import sys

def write_colormap (f, name, cmap):
    f.write("var %(name)s=[" % locals())
    colormap = cmap(np.arange(255))
    f.write('\n\t,'.join(['[%d,%d,%d]' % (col[0]*255,col[1]*255,col[2]*255) for col in colormap]))
    f.write("];\n\n");
    return {name:colormap}
 
    
def write_js_colormap ():
    colmaps=[m for m in cm.datad if not m.endswith("_r")]    
    maps={}
    f=open("colormaps.js","w")    
    maps.update(write_colormap(f,'terrain',get_cmap('terrain',255)))
    maps.update(write_colormap(f,'prism',get_cmap('prism',255)))

    # header uitschrijven
    s=["'%s':%s" % (mapname,mapname) for mapname in maps.keys()]
    s="\n\t,".join(s)
    f.write("var colormaps={\n\t"+s+"};")
    f.close()    

            
write_js_colormap ()
