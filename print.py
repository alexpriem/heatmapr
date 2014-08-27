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



def print_pdf():
    print 'print_pdf', filename
    printer = QPrinter(mode = QPrinter.ScreenResolution)
    printer.setPaperSize(QSizeF(1024, 768), QPrinter.DevicePixel)
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
    xpage.setViewportSize(xpage. currentFrame().contentsSize())
    image = QImage(xpage.viewportSize(),QImage.Format_ARGB32)
    image.setDotsPerMeterX(1000*1200)
    image.setDotsPerMeterY(1000*1200)

	#http://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/composer.html

	#painter = QPainter(image)
	#sourceArea = QRectF(0, 0, c.paperWidth(), c.paperHeight())
	#targetArea = QRectF(0, 0, width, height)
	#c.render(imagePainter, targetArea, sourceArea)
	#imagePainter.end()

    painter = QPainter(image)
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
    sys.exit()
else:
	print 'start_print_png'
	QObject.connect(web, SIGNAL("loadFinished(bool)"), print_png)

  
sys.exit(app.exec_())
