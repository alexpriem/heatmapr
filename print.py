# taken from
# http://stackoverflow.com/questions/11060439/filling-out-a-form-using-pyqt-and-qwebview

import os,sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4 import QtCore
from time import sleep

infile=sys.argv[1]
f=open(infile,'r')
txt=f.read()
f.close()
txt=txt.replace('printinfo hier','printinfo hier\nvar print=true;\n')
g=open('./tmp.html','w')
g.write(txt)
g.close()

app = QApplication(sys.argv)
web = QWebView()
web.load(QUrl("./tmp.html"))

# alternatief: met gs conversie doen
#gs -sDEVICE=pngalpha -sOutputFile=infile.png -r1200 infile.pdf -dBATCH

def get_imgsize(filename):

    f=open(filename)
    imgwidth=500
    imgheight=500
    for line in f.readlines():
      #  print line[:11]
        if line[:11]=='"imgwidth":':
            imgwidth=int(line[11:-2])
        if line[:12]=='"imgheight":':
            imgheight=int(line[12:-2])    
    f.close()
    return imgwidth, imgheight
    
        


def print_pdf():
    print 'print_pdf', outfile
    width,height=get_imgsize(infile)
    printer = QPrinter(mode = QPrinter.ScreenResolution)
    printer.setPaperSize(QSizeF(640, 480), QPrinter.DevicePixel)
    printer.setOutputFormat(QPrinter.PdfFormat)
    printer.setPageMargins(0 , 0 , 0 , 0 , QPrinter.DevicePixel)
    printer.setFullPage(True)
    printer.setOutputFileName(outfile)    
    web.print_(printer)
    #print_png()
    sys.exit(0)


def print_png():
    print 'print_png, output:', outfile
    xpage = web.page()        
    xpage.setViewportSize(xpage. currentFrame().contentsSize())
    width,height=get_imgsize(infile)
    print width, height
    image = QImage(QSize(width+200,height+150),QImage.Format_ARGB32)
    image.setDotsPerMeterX(1000*1200)
    image.setDotsPerMeterY(1000*1200)

	#http://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/composer.html

	#painter = QPainter(image)
	#sourceArea = QRectF(0, 0, c.paperWidth(), c.paperHeight())
	#targetArea = QRectF(0, 0, width, height)
	#c.render(imagePainter, targetArea, sourceArea)
	#imagePainter.end()

    painter = QPainter(image)
    painter.setRenderHint(QPainter.SmoothPixmapTransform);
    painter.setRenderHint(QPainter.Antialiasing);
    #painter.setRenderHint(QPainter.TextAntialiasing);
    #painter.setRenderHint(QPainter.HighQualityAntialiasing); 
    xpage.mainFrame().render(painter)
    
    painter.end()
    image.save(outfile)    
    sys.exit(0)   

#web.show()
outfile='out.png'



if len(sys.argv)==2:        
	outfile=infile.replace('.html','.png')
	printtype='png'
if len(sys.argv)==3:    
    printtype=sys.argv[2]    
    outfile=infile.replace('html',printtype)
if printtype=='pdf':
    print 'start_print_pdf'    
    QObject.connect(web, SIGNAL("loadFinished(bool)"), print_pdf)    
    
else:
    print 'start_print_png'    
    QObject.connect(web, SIGNAL("loadFinished(bool)"), print_png)

  
sys.exit(app.exec_())
