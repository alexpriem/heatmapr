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




def read_header (filename,sep=None):


    f=open(filename,'r')
    headerline=f.readline()
    if sep is None:
        sep=','
        if len(headerline.split(sep))==1:
            sep=';'
            if len(headerline.split(';'))==1:
                raise RuntimeError ('unknown separator')
            
    cols=[col.strip() for col in headerline.split(sep)]

    return sep, cols


def dataset (request, dataset):

    #print request.GET['dataset']
    datadir=request.GET['datadir']


    sep,cols=read_header(datadir+'/'+dataset+'.csv')
        
    data={'dataset':dataset, 'sep':sep, 'cols':cols}
    return HttpResponse(cjson.encode(data))

