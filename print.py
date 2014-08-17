# taken from
# http://stackoverflow.com/questions/11060439/filling-out-a-form-using-pyqt-and-qwebview

import os,sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4 import QtCore

app = QApplication(sys.argv)
web = QWebView()
web.load(QUrl("./bitmap.html"))



def print_pdf():
    print 'print_pdf', filename
    printer = QPrinter(mode = QPrinter.ScreenResolution)
    printer.setPaperSize(QSizeF(1024, 768), QPrinter.DevicePixel)
    printer.setOutputFormat(QPrinter.PdfFormat)
    printer.setPageMargins(0 , 0 , 0 , 0 , QPrinter.DevicePixel)
    printer.setFullPage(True)
    printer.setOutputFileName(filename)    
    web.print_(printer)
    print_png()
    sys.exit(0)

def print_png():
    print 'print_png', filename
    xpage = web.page()
    xpage.setViewportSize(xpage. currentFrame().contentsSize())
    image = QImage(xpage.viewportSize(),QImage.Format_ARGB32)
    painter = QPainter(image)
    xpage.mainFrame().render(painter)
    painter.end()
    image.save(filename)    
    sys.exit(0) 

#web.show()
filename='out.png'
if len(sys.argv)==2:
    filename=sys.argv[1]
print filename, filename[-4:]
if filename[-4:]=='.png':
    print 'start_print_png'
    QObject.connect(web, SIGNAL("loadFinished(bool)"), print_png)
if filename[-4:]=='.pdf':
    QObject.connect(web, SIGNAL("loadFinished(bool)"), print_pdf)
    
sys.exit(app.exec_())
