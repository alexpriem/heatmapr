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



def read_csv_dict(filename, skipheader=False):
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


def read_csv_file(filename):   #  eerste waarde van csv-file inlezen
    f=None
    try:
        f=open(filename)
    except:
        pass
    labellist=[]
    if f is not None:
        c = csv.DictReader(f)
        for row in c:
            labellist.append(row)
        f.close()
    return labellist




def read_header (filename,sep=None):

    f=open(filename,'r')
    headerline=f.readline()
    if sep is None:
        sep=','
        if len(headerline.split(sep))==1:
            sep=';'
            if len(headerline.split(';'))==1:
                raise RuntimeError ('unknown separator')

    cols=[col.replace('"','').strip() for col in headerline.split(sep)]
    return sep, cols






def read_configfile (infodir):

    f=None
    try:
        f=open(infodir+'/data_config.csv')
    except:
        pass
    config=[]
    if f is not None:
        c=csv.DictReader(f,delimiter=',')
        for line in c:
            config.append(line)
    return config


def read_filterfile (infodir):

    f=None
    try:
        f=open(infodir+'/filters.csv')
    except:
        pass
    matches=[]
    if f is not None:
        c=csv.DictReader(f,delimiter=',')
        for line in c:
            matches.append(line)
        f.close()
    return matches


def read_recodefile (infodir):

    f=None
    try:
        f=open(infodir+'/recodes.csv')
        f.readline()
    except:
        pass

    labelset=[]
    labeldict={}
    if f is not None:
        c=csv.reader(f,delimiter=',')
        for line in c:
            if len(line)==2:
                labelset.append({'value':line[0],'replacement':line[1]})
                labeldict[line[0]]=line[1]
        f.close()
    return labeldict,labelset





def get_cols (datadir, dataset, infodir):

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
        csv.write(g,delimiter=',',quotechar='"')
        f.write('sep=%s\n' % sep)
        g.write('enabled,colname,typehint,format\n')
        for col in cols:
            f.write(col+'\n')
            g.writerow([1,col,'',""])
        f.close()
        g.close()
    return sep, cols




def get_enabled_cols (infodir):

    config=read_configfile(infodir)
    enabled_keys=[]
    for row in config:
        if int(row['enabled'])==1:
            enabled_keys.append(row['colname'])
    return enabled_keys




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