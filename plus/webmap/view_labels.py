import os, csv
from django.http import HttpResponse
from django.template import RequestContext, loader
import helpers, cjson
from operator import itemgetter
import plus.settings as settings

def view_dataset_var_labels (request, dataset):

    infodir=helpers.get_infodir(dataset)

    labels=helpers.read_csvfile (infodir+'/labels.csv')
    labels=sorted(labels.iteritems())
    template = loader.get_template('dataset_labels.html')
    labeljson=cjson.encode(labels)

    context = RequestContext(request, {'defaults':labeljson, 'dataset':dataset})
    return HttpResponse(template.render(context))




def view_var_key_labels (request, dataset, variable):

    infodir=settings.datadir+'/'+dataset+'_info'
    if not os.path.exists(infodir):
        os.makedirs(infodir)

    template = loader.get_template('var_labels.html')

    varlabels=helpers.read_csvfile (infodir+'/labels.csv')
    varlabel=varlabels[variable]

    global_labels=helpers.read_csvfile ('%s/labels/defaults.csv' % (infodir))
    global_labels=sorted(global_labels.iteritems())
    key_labels=helpers.read_csvfile ('%s/labels/%s.csv' % (infodir, variable))
    if len(key_labels)==0:
        key_labels={}
        f=open('%s/hists/%s.csv' % (infodir, variable))
        f.readline()
        c=csv.reader(f,delimiter=',')
        for row in c:
            key_labels[row[0]]=''
        f.close()
    #key_labels=sorted(key_labels, key=itemgetter(1))
    key_labels=sorted(key_labels.iteritems())
    has_labels= len(key_labels)!=0
    has_global= len(global_labels)!=0
    #print has_labels, has_global
    #print key_labels
    context = RequestContext(request, {'labels':key_labels,
                                       'global_labels':global_labels,
                                       'has_global':has_labels,
                                       'has_labels':has_labels,
                                       'dataset':dataset,
                                       'variable':variable,
                                       'varlabel':varlabel})
    return HttpResponse(template.render(context))

