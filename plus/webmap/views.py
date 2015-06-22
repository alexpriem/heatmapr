import os,sys, cjson
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader




# Create your views here.


def top (request):

    template = loader.get_template('top.html')

    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

    

def heatmap (request):

    print request.path
    print request #.META
    
    #print dataset
    template = loader.get_template('bitmap.html')

    context = RequestContext(request, {})
    return HttpResponse(template.render(context))




def dataset (request, dataset):

    #print request.GET['dataset']
    datadir=request.GET['datadir']
    
    
    sep=';'
    data={'dataset':dataset, 'sep':sep}
    return HttpResponse(cjson.encode(data))

