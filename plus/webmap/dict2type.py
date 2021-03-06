import os, math, csv
import array, datetime, dateutil.parser
import helpers



class typechecker ():

    def __init__(self):
        self.subtype2typecode={'char':'c',
                             'signed char':'b',
                             'unsigned char':'B',
                             'signed short':'h',
                             'unsigned short':'H',
                             'signed int':'i',
                             'unsigned int': 'I',
                             'signed long':'l',
                             'unsigned long':'L',
                             'float':'f',
                             'double':'d'}


    def update_num_records (self, variable):
        f=open(self.infodir+'/hist/%s.csv' % variable)
        f.readline()        
        sumval=0
        for line in f:
            key,val=line[:-1].split(',')
            sumval+=int(val)
        self.num_records=sumval
        
    #
    #
    #
    def get_type (self, variable):

        info={}
        info['col']=variable
        if variable=='dummy':
            d={}
            info['datatype']=0
            info['float_t']=0
            info['int_t']=0
            info['str_t']=0
            info['date_t']=0
            info['float_min']=0
            info['float_max']=0
            info['int_min']=0
            info['int_max']=0
            info['missing']=0
            info['num_keys']=0
            info['num_valid']=0
            info['num_missing']=0
            info['min_val']=0
            info['max_val']=0
            return info

        dateconfig=helpers.read_csv_dict(self.infodir+'/dateformat.csv')
        dateformat=dateconfig.get(variable)


        self.empty=False
        f=open(self.infodir+'/hist/%s.csv' % variable)
        f.readline()
        c=csv.reader (f, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        lines=0        
        float_t=0
        int_t=0
        str_t=0
        date_t=0
        date_fails=0
        has_missing=False
        int_min=None
        int_max=None
        float_min=None
        float_max=None
        sumval=0
        avgsum=0
        num_valid=0


        hist={}
        hist_string={}
        self.hist=hist
        self.hist_string=hist_string
        for line in c:            
            lines+=1
            key,val=line[0],int(line[1])                        
            hist_string[key]=val            
            try:
                v=float(key)
            except:
                hist[key]=val
                if (date_fails<20):
                    #print 'df', date_fails, date_t
                    d=helpers.test_date(key, dateformat)
                    #print 'date:',d, type(d)
                    if type(d)==datetime.datetime:
                        date_t+=1
                        continue
                    else:
                        str_t+=1
                        date_fails+=1
                        continue
                str_t+=1
                date_fails+=1
                hist[key]=val
                continue
            
            if len(key)>=2:
                if key[0]=='0' and key[1].isdigit():    # voorloopnul -> string ipv int/float                
                    str_t+=1
                    hist_string[key]=val                    
                    continue
                
            if math.isinf(v):
                str_t+=1
                hist[key]=val
                continue                

            num_valid+=val
            avgsum+=v*val            
            if v.is_integer():                
                int_t+=1
                i=int(v)
                if int_min is None or i<int_min:
                    int_min=i
                if int_max is None or i>int_max:
                    int_max=i
                hist[i]=val                
            else:                
                float_t+=1                
                if float_min is None or v<float_min:
                    float_min=v
                if float_max is None or v>float_max:
                    float_max=v
                hist[v]=val
            
        print variable, int_t, float_t, str_t, date_t

        num_keys=lines
        num_missing=0

        missing=helpers.read_csv_list(self.infodir+'/missing/default.csv')
        missing2=helpers.read_csv_list(self.infodir+'/missing/%s.csv' % variable)
        if missing is None:
            missing=['','NA','NULL']    # tzt naar externe file

        if ['0'] in hist_string.items() and missing2 is None:
            if (num_keys>20) and (hist_string['0']>0.1*self.num_records):
                missing.append('0')
        if missing2 is not None:
            missing=missing+missing2

        for k,v in hist_string.items():
            if k in missing:
                num_missing+=v


        min_val=None
        if int_min is not None:
            min_val=int_min;
        if float_min is not None:
            min_val=float_min;
            if int_min is not None:
                if int_min<float_min:
                    min_val=int_min

        max_val=None
        if int_max is not None:
            max_val=int_max;
        if float_max is not None:
            max_val=float_max;
            if int_max is not None:
                if int_max>float_max:
                    max_val=int_max
                            
            

        datatype='char'
        realstr=str_t - num_missing
        if (num_keys>=14):
            if (float_t!=0) and (realstr<=4):
                datatype='float'
            if (float_t==0) and  (int_t!=0) and (realstr<=4):
                datatype='int'
            if (float_t==0) and  (int_t==0) and (realstr>=0):
                datatype='char'
            if (num_keys>100) and (str_t>50):     # voor het geval van een kleine fractie ints/floats
                datatype='char'
            if (date_t>0) and (date_fails<10):
                datatype='date'
        if (num_keys<14):
            if (float_t!=0) and (realstr<=1):
                datatype='float'
            if (float_t==0) and  (int_t!=0) and (realstr<=1):
                datatype='int'
            if (float_t==0) and  (int_t==0) and (realstr>=0):
                datatype='char'
            if (date_t>0) and (realstr<=1):
                datatype='date'

        if (has_missing) and (num_keys==1):
            datatype='missing'


        single_value=(num_keys==1)
        bi_value=(num_keys==2)
        string_garbage=False
        #print (float_t+int_t)>str_t, (str_t-empty), ((str_t-empty)>0 and (str_t-empty<10))
        if ((float_t+int_t)>str_t) and ((realstr)>0 and (realstr<10)):
            string_garbage=True



        info['datatype']=datatype
        info['float_t']=float_t
        info['string_garbage']=string_garbage
        info['single_value']=single_value
        info['bi_value']=bi_value
        info['int_t']=int_t
        info['str_t']=str_t
        info['date_t']=date_t
        info['float_min']=float_min
        info['float_max']=float_max
        info['int_min']=int_min
        info['int_max']=int_max

        info['missing']=has_missing
        info['num_keys']=num_keys
        info['num_valid']=num_valid
        info['num_missing']=num_missing
        info['num_records']=self.num_records
        info['min_val']=min_val
        info['max_val']=max_val
        info['avg']=avgsum/self.num_records
        self.num_keys=lines
        unique_index=0
        if len(hist)==self.num_records:
            unique_index=1
        info['unique_index']=unique_index
        
        return info






    def sort_histogram (self, variable, minbound, maxbound):     

        numeric=((self.data_info['int_t']!=0) or (self.data_info['float_t']!=0))
        range01=None
        range50=None
        range99=None
        num_valid=self.data_info['num_valid']
        if (numeric):
            perc01=minbound*num_valid # 0.01 percentiel      # percentielen alleen over gevulde data bepalen
            perc50=0.5*num_valid # 0.99 percentiel
            perc99=maxbound*num_valid # 0.99 percentiel
            sumval=0

        datatype=self.data_info['datatype']
        empty=self.data_info['missing']

        
        f=open(self.infodir+'/hist/%s.csv' % variable)
        header=f.readline()

        histdir=self.infodir+'/hists'
        if not os.path.exists(histdir):
            os.makedirs(histdir)        
        outfile=histdir+'/%s.csv' % variable
    
        f=open (outfile,'wb')
        f.write(header)
        c=csv.writer(f, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)        

        hist=self.hist
        self.sorted_keys=sorted(hist.keys())
        for k in self.sorted_keys:
            if  numeric:
                sumval+=int(hist[k])
                if range01 is None and sumval>perc01:
                    range01=k
                if range50 is None and sumval>perc50:
                    range50=k
                if range99 is None and sumval>perc99:
                    range99=k
            c.writerow([str(k),hist[k]])   
        self.data_info['perc01']=range01
        self.data_info['perc50']=range50
        self.data_info['perc99']=range99
        f.close()

        



        # todo: histogram uitschrijven zonder grenzen
        # indikken van aantal keys in histogram tot max 100.

    def write_histogram_alphanumeric (self, variable):


        return
        
        
    def write_histogram_100 (self, variable): 

        if not os.path.exists(self.infodir+'/hista'):
            os.makedirs(self.infodir+'/hista')

        data_info=self.data_info
        data_info['maxy2']=None
        data_info['maxy3']=None        
        data_info['sparse1']=False
        data_info['sparse2']=False

        
        num_keys=self.num_keys
        if num_keys==1:
            return
        
        numeric=((data_info['int_t']!=0) and (data_info['float_t']!=0))
        if not(numeric):    # numeriek en alles met <14 keys:  behandelen als classificatie
            self.write_histogram_alphanumeric (variable)
            return
        if num_keys<14:
            self.write_histogram_alphanumeric(variable)
            return

        bins=100
        if num_keys<100:
            bins=num_keys

        
        minx=data_info['perc01']   
        maxx=data_info['perc99']
        if data_info['min_val']<=0 and minx>0:
            minx=0
        if maxx=='':
            maxx=data_info['max_val']
        if (maxx-minx)==0:
            return


        dx=(maxx-minx)/(1.0*bins)       # swap van relatieve space naar absolute space, kan fout gaan ;-)

        j=0
        histogram=[0]*(bins+1)
        hist=self.hist
        sorted_keys=self.sorted_keys

        
        for key in sorted_keys:
            if ((key<minx) or (key>maxx)):
                continue
            binnr=int((key-minx)/dx)
            try:            
                histogram[binnr]+=int(hist[key])
            except:
                print data_info
                print bins, binnr, minx, maxx, dx, key
                raise RuntimeError

        f=open(self.infodir+'/hista/%s.csv' % variable,'wb')        
        f.write('bin_min,val\n')

        h=sorted(histogram)
        maxy=h[-1]
        maxy2=h[-2]
        maxy3=h[-3]

        data_info['maxy2']=maxy2
        data_info['maxy3']=maxy3
        if maxy>10*maxy2:
            data_info['sparse1']=True
            if maxy2>10*maxy3:
                data_info['sparse2']=True

        
    
        miny=h[0]
        c=csv.writer(f, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        c.writerow([minx,miny])
        c.writerow([maxx,maxy])
        c.writerow([maxy2,maxy3])
        for i,y in enumerate(histogram):
            c.writerow([minx+i*dx,y])
        f.close()

        self.data_info=data_info
        

            
                
            
            
            


# missings doen!

    def  write_binfile (self, variable):
        
        if not os.path.exists(self.infodir+'/splitbin'):
            os.makedirs(self.infodir+'/splitbin')

        self.data_info['bin_typecode']=''
        self.data_info['bin_indirect']=False
        num_keys=self.num_keys            
        if num_keys>4294967295:
         #   print 'write_binfile:skipping, too many keys'
            return
        if num_keys==1:
        #    print 'write_binfile:skipping, no data'
            return
        data_info=self.data_info


       # print hist_keys




        data=[]
        bin_indirect=True
        if (data_info['datatype']=='int'):
            code=None
            if data_info['int_min']>=0 and data_info['int_max']<=255:
                code='B'
            if (code is None) and (data_info['int_min']>-127) and (data_info['int_max']<=127):
                code='b'
            if data_info['int_min']>=0 and data_info['int_max']<=65536:
                code='H'
            if (code is None) and (data_info['int_min']>-32767) and (data_info['int_max']<=32767):
                code='b'
            if data_info['int_min']>=0 and data_info['int_max']<=4294967295:
                code='L'
            if data_info['int_min']>=-2147483647 and data_info['int_max']<=2147483647:
                code='l'
            if code is not None:
                data_array=array.array(code,data)
                bin_indirect=False
                f=open(self.infodir+'/split/%s.csv' % variable)
                for line in f:
                    try:
                        i=int(line)
                    except:
                        i=255  # of max
                    data.append(i)




        if bin_indirect:
            f=open(self.infodir+'/split/%s.csv' % variable)
            hist_keys=sorted(self.hist_string)
            hist_index={}
            for i,k in enumerate(hist_keys):
                hist_index[k]=i

            if num_keys<256:
                code='B'
            if num_keys>=256 and num_keys<65536:
                code='H'
            if num_keys>=65536 and num_keys<4294967295:
                code='L'

            for line in f:
                s=line[:-1]
                try:
                    d=hist_index[s]
                    data.append(d)
                except:
                    ef=open(self.infodir+'/error.log','a')
                    s='Key [%s] not found when dictifying variable %s, %d\n' % (s,variable, len(s))
                    ef.write(s)
                    ef.close()

        data_array=array.array(code,data)

        f=open(self.infodir+'/splitbin/%s.bin' % variable,'wb')
        data_array.tofile(f)
        f.close()

        self.data_info['bin_typecode']=code
        self.data_info['bin_indirect']=bin_indirect



     

    def analyse(self, cols):
        g=open(self.infodir+'/col_types.csv','w')
        s="colname,datatype,num_keys,num_valid,num_missing,num_records,"
        s+="missing,unique_index,string_garbage,single_value,bi_value,"
        s+="float_t,int_t,str_t,date_t,int_min,int_max,"
        s+="float_min,float_max,min,max,avg,perc01,perc50,perc99,maxy2,maxy3,"
        s+="sparse1,sparse2,bin_typecode,bin_indirect\n"
        g.write(s);
        skip=True
        for col in cols:
            if col=='.':
                break
            f=self.data_info=self.get_type (col)
            self.sort_histogram (col, 0.01, 0.99)
            self.write_histogram_100 (col)
            self.write_binfile (col)

            s='%(col)s,%(datatype)s,%(num_keys)d,%(num_valid)d,%(num_missing)d,%(num_records)d,%(missing)d,%(unique_index)d' % f
            s+=',%(string_garbage)s,%(single_value)s,%(bi_value)s' % f
            s+=',%(float_t)d,%(int_t)d,%(str_t)d,%(date_t)d' % f
            s+=',%(int_min)s,%(int_max)s' % f
            s+=',%(float_min)s,%(float_max)s' % f
            s+=',%(min_val)s,%(max_val)s' % f
            s+=',%(avg)s,%(perc01)s,%(perc50)s,%(perc99)s' % f
            s+=',%(maxy2)s,%(maxy3)s' % f
            s+=',%(sparse1)s,%(sparse2)s, %(bin_typecode)s,%(bin_indirect)s' % f
            s+='\n'
            g.write(s)
