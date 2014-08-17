import sys, threading, webbrowser, BaseHTTPServer

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4 import QtCore


FILE = 'bitmap.html'
PORT = 8080

FILE=sys.argv[1]

app = QApplication(sys.argv)
web = QWebView()
web.load(QUrl("./"+FILE))
web.show()

def print_png_Qt():

        print 'print_png_Qt:'
        xpage = self.web.page()
        xpage.setViewportSize(xpage.currentFrame().contentsSize())
        image = QImage(xpage.viewportSize(),QImage.Format_ARGB32)
        painter = QPainter(image)
        xpage.mainFrame().render(painter)
        painter.end()
        image.save('out.png')




class TestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """The test example handler."""

    def do_GET(self):        
        is_ajax=self.headers.get('X-Requested-With')=='XMLHttpRequest'            
        if self.path== "favico.ico":
            return                
        if self.path.endswith(".html"):
            f=open (self.path[1:])
            result=f.read()
            f.close()
                
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()          
            self.wfile.write(result)
        if self.path.endswith(".css"):
            f=open (self.path[1:])
            result=f.read()
            f.close()
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()          
            self.wfile.write(result)
        if self.path.endswith(".js"):
            f=open (self.path[1:])
            result=f.read()
            f.close()
            self.send_response(200)
            self.send_header('Content-type', 'text/javascript')
            self.end_headers()          
            self.wfile.write(result)

        if is_ajax:
            print 'is_ajax'
            path=self.path.split('?')
            result='{"msg":"error"}'        
            if path[0]=='/png':
                filename='out.png'
                self.print_png(filename)
                result='{"msg":"OK"}'
            if path[0]=='/pdf':
                filename='out.pdf'
                self.print_pdf(filename)
                result='{"msg":"OK"}'
            self.send_response(200)            
            self.send_header('Content-length', len(result))
            self.send_header('Content-type', 'application/json')
            self.end_headers()          
            self.wfile.write(result)                        
            
            

            
    def do_POST(self):
        """Handle a post request by returning the square of the number."""        
        is_ajax=self.headers.get('X-Requested-With')=='XMLHttpRequest'
        
        print 'POST', self.path, is_ajax    
        result={'result':'ok'}
        self.send_response(200)
        self.send_header('Content-type', 'text/javascript')
        self.end_headers()          
        self.wfile.write(result)


    
    def print_png(self,filename):

        print 'print_png:',filename
        self.filename=filename        
     
        QObject.connect(web, SIGNAL("loadFinished(bool)"), print_png_Qt)
        
        


def open_browser():
    """Start a browser after waiting for half a second."""
    def _open_browser():
        webbrowser.open('http://localhost:%s/%s' % (PORT, FILE))
    thread = threading.Timer(0.5, _open_browser)
    thread.start()

def start_server():
    """Start the server."""
    server_address = ("", PORT)
    server = BaseHTTPServer.HTTPServer(server_address, TestHandler)
    server.serve_forever()

if __name__ == "__main__":
    open_browser()
    start_server()
