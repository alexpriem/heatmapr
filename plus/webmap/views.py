from django.http import HttpResponse
from django.template import RequestContext, loader



def top (request):

    template = loader.get_template('top.html')

    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


