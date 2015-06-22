import sys
from time import time
#from django.conf import settings
import settings
from django.views.debug import technical_500_response
from django.template import RequestContext
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseServerError

class Http403(Exception):
    pass  

def render_to_403(*args, **kwargs):
    """
        Returns a HttpResponseForbidden whose content is filled with the result of calling
        django.template.loader.render_to_string() with the passed arguments.
    """
    if not isinstance(args,list):
        args = []
        args.append('403.html')              

    httpresponse_kwargs = {'mimetype': kwargs.pop('mimetype', None)}
    response = HttpResponseForbidden(loader.render_to_string(*args, **kwargs), **httpresponse_kwargs)              
    return response  


class Http403Middleware(object):
    def process_exception(self,request,exception):
        if isinstance(exception,Http403):
            if settings.DEBUG:
                raise PermissionDenied
            return render_to_403(context_instance=RequestContext(request))


class UserBasedExceptionMiddleWare(object):
    def process_exception(self, request, exception):
        import sys        
        if request.is_ajax():
            import sys, traceback
            (exc_type, exc_info, tb) = sys.exc_info()
            errortxt = "%s\n" % exc_type.__name__
            errortxt += "%s\n\n" % exc_info
            errortxt += "TRACEBACK:\n"    
            for tb in traceback.format_tb(tb):
                errortxt += "%s\n" % tb
            if request.META.get('REMOTE_ADDR')=='127.0.0.1':
                print errortxt #ook naar console loggen bij ontwikkelserver
            return HttpResponseServerError(errortxt, mimetype='text/html')
        
        if isinstance(exception, Http403):
            if settings.DEBUG:
                raise PermissionDenied
            return render_to_403(context_instance=RequestContext(request))
        return technical_500_response(request, *sys.exc_info())
    
        

    def process_request(self, request):
        request.META['reqid']=hex(int(1000*time()))      # fungeert als unieke identifier.


