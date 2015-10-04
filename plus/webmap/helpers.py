import os, csv, datetime
import plus.settings as settings


# helperfunction to read simple csv-file to a dict



def get_infodir (dataset):

    infodir=settings.datadir+'/'+dataset+'_info'
    if not os.path.exists(infodir):
        os.makedirs(infodir)   # en dataset bekijken
        os.makedirs(infodir+'/labels')
        sep, cols=get_cols(datadir, dataset, infodir)  # aanmaken coltypes



    return infodir



def read_csvfile(filename, skipheader=False):
    f=None
    try:
        f=open(filename)
    except:
        pass
    labels={}
    if f is not None:
        if skipheader:
            f.readline()
        c=csv.reader(f,delimiter=',')
        for line in c:
            if len(line)==2:
                labels[line[0]]=line[1]
        f.close()
    return labels


# helperfunction to read simple csv-file to a list

def read_csv_list(filename, skipheader=False):   #  eerste waarde van csv-file inlezen
    f=None
    try:
        f=open(filename)
    except:
        pass
    labellist=[]
    if f is not None:
        if skipheader:
            f.readline()
        c=csv.reader(f,delimiter=',')
        for line in c:
            if len(line)>=1:
                labellist.append(line[0])
        f.close()
    return labellist






def get_cols (dataset, datadir, infodir):

    try:
        f=open(infodir+'/col_info.csv','r')
        sep=f.readline().strip()[4:]
        cols=[]
        for line in f:
            cols.append(line.strip())
    except:
        sep,cols=read_header(datadir+'/'+dataset+'.csv')
        f=open(infodir+'/col_info.csv','w')
        g=open(infodir+'/data_config.csv','w')
        f.write('sep=%s\n' % sep)
        for col in cols:
            f.write(col+'\n')
            g.write("1,%s,,''\n" % col)
        f.close()
        g.close()
    return sep, cols




def get_col_types(infodir):
    f=None
    col_info=[]
    coltypes_bycol={}
    try:
        f=open(infodir+'/col_types.csv')
    except:
        pass
    if f is not None:
        int_cols=['num_keys','missing','unique_index','num_valid','num_missing'
              'float_t','int_t','str_t','date_t','int_min','int_max']
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


def test_date (datestr, dateformat):

    if dateformat is not None:
        d=None
        try:
            d=datetime.datetime.strptime(datestr, dateformat)
        except:
            pass
        return d

    datestr=datestr.strip().replace(' ','-').replace(':','-')
    dateformats=['%Y-%m-%d','%Y-%m']
    for date_format in dateformats:
        d=None
        try:
            d=datetime.datetime.strptime(datestr, date_format )
        except:
            continue
        if d is not None:
            return d
    return None