# taken from
# http://stackoverflow.com/questions/11060439/filling-out-a-form-using-pyqt-and-qwebview



def do_print  (self, url, outfile, printtype):

    # django-template maken
    s="""
var page = require('webpage').create();
page.open('http://localhost:8000/print/%(url)s', function() {
  page.render('%(outfile)s.png');
  phantom.exit();
});""" % locals()

    if printtype=='pdf':
        print 'start_print_pdf'
        os.system(settings.base_dir+'/bin/phantomjs.exe print.js'

    if printtype=='png':
        print 'start_print_png'
        os.system(settings.base_dir+'/bin/phantomjs.exe print.js'
