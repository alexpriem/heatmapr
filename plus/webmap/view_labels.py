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
    labels=sorted(labels.iteritems())
    template = loader.get_template('dataset_labels.html')


    context = RequestContext(request, {'labels':labels, 'dataset':dataset})
    return HttpResponse(template.render(context))




def view_var_key_labels (request, dataset, variable):

    datadir='e:/data'
    infodir=datadir+'/'+dataset+'_info'
    if not os.path.exists(infodir):
        os.makedirs(infodir)

    template = loader.get_template('var_labels.html')

    varlabels=read_csvfile (infodir+'/labels.csv')
    varlabel=varlabels[variable]

    labels=read_csvfile ('%s/labels/defaults.csv' % (infodir))
    print labels
    keylabels=read_csvfile ('%s/labels/%s.csv' % (infodir, variable))
    print keylabels
    if len(keylabels)==0:
        print 'ok'
        f=open('%s/hists/%s.csv' % (infodir, variable))
        f.readline()
        c=csv.reader(f,delimiter=',')
        for row in c:
            keylabels[row[0]]=''
        f.close()
    print keylabels
    labels.update(keylabels)
    labels=sorted(labels.iteritems())
    context = RequestContext(request, {'labels':labels,
                                       'dataset':dataset,
                                       'variable':variable,
                                       'varlabel':varlabel})
    return HttpResponse(template.render(context))

