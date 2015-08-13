import os,sys, cjson, shutil, csv
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt


from csv_split import csv_select
from dictify import dictify_all_the_things
from dict2type import typechecker
from makehist import make_hist3, get_data, check_binsize
from helpers import get_col_types, read_csvfile


def view_dataset_var_labels (request, dataset):

    datadir='e:/data'
    infodir=datadir+'/'+dataset+'_info'
    if not os.path.exists(infodir):
        os.makedirs(infodir)

    labels=read_csvfile (infodir+'/labels.csv')
    template = loader.get_template('dataset_labels.html')
    print 'labels:',labels

    context = RequestContext(request, {'labels':labels, 'dataset':dataset})
    return HttpResponse(template.render(context))




def view_var_key_labels (request, dataset, var):

    datadir='e:/data'
    infodir=datadir+'/'+dataset+'_info'
    if not os.path.exists(infodir):
        os.makedirs(infodir)

    template = loader.get_template('var_labels.html')

    labels=read_csvfile (infodir+'/labels.csv')
    context = RequestContext(request, {'labels':labels})
    return HttpResponse(template.render(context))

