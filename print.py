# taken from
# http://stackoverflow.com/questions/11060439/filling-out-a-form-using-pyqt-and-qwebview


import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4 import QtCore

app = QApplication(sys.argv)
web = QWebView()
web.load(QUrl("./bitmap.html"))



def print_pdf():
    
    printer = QPrinter(mode = QPrinter.ScreenResolution)
    printer.setPaperSize(QSizeF(1024, 768), QPrinter.DevicePixel)
    printer.setOutputFormat(QPrinter.PdfFormat)
    printer.setPageMargins(0 , 0 , 0 , 0 , QPrinter.DevicePixel)
    printer.setFullPage(True)
    printer.setOutputFileName('out.pdf')    
    web.print_(printer)
    print_png()

def print_png():
    xpage = web.page()
    xpage.setViewportSize(xpage. currentFrame().contentsSize())
    image = QImage(xpage.viewportSize(),QImage.Format_ARGB32)
    painter = QPainter(image)
    xpage.mainFrame().render(painter)
    painter.end()
    image.save("out3.png")    
    sys.exit(0) 

#web.show()
QObject.connect(web, SIGNAL("loadFinished(bool)"), print_png)
#QtCore.QObject.connect(web, QtCore.SIGNAL("loadFinished"), print_it)


sys.exit(app.exec_())
