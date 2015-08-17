import os,sys, cjson, shutil, csv
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt


from csv_split import csv_select
from dictify import dictify_all_the_things
from dict2type import typechecker
from makehist import make_hist3, get_data, check_binsize
import heatmap




# helperfunction to read simple csv-file to a dict

def read_csvfile (filename):
    f=None
    try:
        f=open(filename)
    except:
        pass
    labels={}
    if f is not None:
        c=csv.reader(f,delimiter=',')
        for line in c:
            if len(line)==2:
                labels[line[0]]=line[1]
        f.close()
    return labels




def get_col_types(infodir):
    f=None
    col_info=[]
    coltypes_bycol={}
    try:
        f=open(infodir+'/col_types.csv')
    except:
        pass
    if f is not None:
        f.readline()
        f.readline()
        int_cols=['num_keys','empty','unique_index',
              'float_t','int_t','str_t','int_min','int_max']
        float_cols=['float_min','float_max','min','max','perc01','perc50','perc99','maxy2','maxy3', 'avg']
        bool_cols=['sparse1','sparse2','string_garbage','single_value','bi_value']
        c=csv.DictReader(f,delimiter=',')
        linenr=0
        for row in c:
          #  print line
            for c in int_cols:
                try:
                    row[c]=int(float(row[c]))
                except:
                    row[c]=''
            for c in float_cols:
                try:
                    v=float(row[c])
                    if v.is_integer():
                        v=int(v)
                    row[c]=v
                except:
                    row[c]=''


            for c in bool_cols:
                if row[c]=='True':
                    row[c]=True
                if row[c]=='False':
                    row[c]=False
            row['colnr']=linenr
            col_info.append(row)
            colname=row['colname']
            coltypes_bycol[colname]=row
            linenr+=1
        f.close()


    return col_info,coltypes_bycol

