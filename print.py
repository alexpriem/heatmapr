# taken from
# http://stackoverflow.com/questions/11060439/filling-out-a-form-using-pyqt-and-qwebview

import os,sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4 import QtCore
from time import sleep


f=open(sys.argv[1],'r')
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

def print_pdf():
    print 'print_pdf', filename
    printer = QPrinter(mode = QPrinter.ScreenResolution)
    printer.setPaperSize(QSizeF(640, 480), QPrinter.DevicePixel)
    printer.setOutputFormat(QPrinter.PdfFormat)
    printer.setPageMargins(0 , 0 , 0 , 0 , QPrinter.DevicePixel)
    printer.setFullPage(True)
    printer.setOutputFileName(filename)    
    web.print_(printer)
    #print_png()
    sys.exit(0)

def print_png():
    print 'print_png', filename
    xpage = web.page()
    print xpage.viewportSize()
    print xpage. currentFrame().contentsSize()
    #1.33*1600
    xpage.setViewportSize(xpage. currentFrame().contentsSize())    
    image = QImage(QSize(1706,1280),QImage.Format_ARGB32)
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
    painter.setRenderHint(QPainter.TextAntialiasing);
    painter.setRenderHint(QPainter.HighQualityAntialiasing); 
    xpage.mainFrame().render(painter)
    painter.end()
   # sleep(1)
    image.save(filename)    
    sys.exit(0) 

#web.show()
filename='out.png'
if len(sys.argv)==2:
	filename=sys.argv[1].replace('.html','.png')
	printtype='png'
if len(sys.argv)==3:    
    printtype=sys.argv[2]
    filename=sys.argv[1].replace('html',printtype)
if printtype=='pdf':
    print 'start_print_pdf'
    QObject.connect(web, SIGNAL("loadFinished(bool)"), print_pdf)    
    
else:
    print 'start_print_png'
    QObject.connect(web, SIGNAL("loadFinished(bool)"), print_png)

  
sys.exit(app.exec_())
