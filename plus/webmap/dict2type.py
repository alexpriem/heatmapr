import os,sys,math
import array




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
            key,val=line[:-1].split(':')
            sumval+=int(val)
        self.num_records=sumval
        
    #
    #
    #
    def get_type (self, variable):

        if variable=='dummy':
            f={}
            f['datatype']=0
            f['float_t']=0
            f['int_t']=0
            f['str_t']=0
            f['float_min']=0
            f['float_max']=0
            f['int_min']=0
            f['int_max']=0
            f['empty']=0
            f['num_keys']=0
            f['min_val']=0
            f['max_val']=0
            return f
        
        self.empty=False
        f=open(self.infodir+'/hist/%s.csv' % variable)
        f.readline()
        
        lines=0        
        float_t=0
        int_t=0
        str_t=0
        empty=0
        int_min=None
        int_max=None
        float_min=None
        float_max=None
        
        for line in f:            
            lines+=1
            key,val=line.strip().split(':')            
            if key=='':
                empty=1
                continue            
            try:
                v=float(key)
            except:                
                str_t+=1
                continue
            
            if len(key)>=2:
                if key[0]=='0' and key[1].isdigit():    # voorloopnul -> string ipv int/float                
                    str_t+=1
                    continue
                
            if math.isinf(v):
                str_t+=1
                continue
            
            if v.is_integer():
                int_t+=1
                i=int(v)
                if int_min is None or i<int_min:
                    int_min=i
                if int_max is None or i>int_max:
                    int_max=i                
            else:
                float_t+=1                
                if float_min is None or v<float_min:
                    float_min=v
                if float_max is None or v>float_max:
                    float_max=v
                            
        print variable, int_t, float_t, str_t


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
                    

        num_keys=lines
        datatype='complex'
        if (float_t!=0) and (str_t==0):
            datatype='float'
        if (float_t==0) and  (int_t!=0) and (str_t==0):
            datatype='int'
        if (float_t==0) and  (int_t==0) and (str_t!=0):
            datatype='char'
        if (str_t==1) or (int_t==1) or (float_t==1):
            if (num_keys==1) or ((num_keys==2) and (empty==1)):
                datatype='single_'+datatype
        if (empty==1) and (num_keys==1):
            datatype='empty'
        

        f={}
        f['datatype']=datatype
        f['float_t']=float_t
        f['int_t']=int_t
        f['str_t']=str_t
        f['float_min']=float_min
        f['float_max']=float_max
        f['int_min']=int_min
        f['int_max']=int_max
        f['empty']=empty
        f['num_keys']=num_keys
        f['min_val']=min_val
        f['max_val']=max_val    
        return f



    def get_range (self, variable,t, min_perc, max_perc):

        if not os.path.exists(self.infodir+'/hists'):
            os.makedirs(self.infodir+'/hists')

        

        if self.empty:
            return 'char'
        
        f=open(self.infodir+'/hist/%s.csv' % variable)
        f.readline()
        maxlen=None
        min_val=None
        max_val=None
        min_records=min_perc*self.num_records
        max_records=max_perc*self.num_records
        min_range=None
        max_range=None
        sumval=0
        hist={}        
        for line in f:            
            key,val=line[:-1].split(':')
            if key=='':
                sumval+=int(val)
                hist['']=val
                continue
            if t=='int':
                d=int(key)
                if min_val is None or d<min_val:
                    min_val=d
                if max_val is None or d>max_val:
                    max_val=d
                    
            if t=='float':
                d=float(key)    
                if min_val is None or d<min_val:
                    min_val=d
                if max_val is None or d>max_val:
                    max_val=d

            if t=='int' or t=='float':
                sumval+=int(val)           
               # print t,key,d
                if min_range is None and sumval>min_records:
                    min_range=d
                if max_range is None and sumval>max_records:
                    max_range=d

            if t=='char':
                d=key
                if maxlen is None or len(key)>maxlen:
                    maxlen=len(key)
                    
            hist[d]=val
        #print sorted(hist.keys())
        f.close()

        
        self.num_keys=len(hist.keys())        
        self.hist=hist
        # rewrite histogram keys in sorted order according to type
        if ((t=='int') or (t=='float')):
            f=open(self.infodir+'/hists/%s.csv' % variable,'w') 
            f.write('%s:nums\n' % variable)
            for k in sorted(hist.keys()):
                val=hist[k]
                f.write('%s:%s\n' % (str(k),str(val)))
            f.close()

        self.min_range2=min_range
        self.min_range=min_range
        self.max_range=max_range
        if max_range is not None:            
            if min_range>0 and min_range<max_range*0.1:
                self.min_range2=0        
                

            
        print variable, ' range' , min_val, max_val
        self.min_val=min_val
        self.max_val=max_val
        self.max_len=maxlen
        
        if t=='int':
            if ((min_val>=0) and (max_val<255)):
                return 'unsigned char' # 0..255

            if ((min_val>-126) and (max_val<127)):
                return 'signed char'   # -126..127

            if ((min_val>=0) and (max_val<65535)):
                return 'unsigned short'  # 0..65535

            if ((min_val>-32767) and (max_val<32767)):
                return 'signed short'  # -32767..32767

            if ((min_val>=0) and (max_val<4294967296L)):
                return 'unsigned long'  # 0..4294967296L

            if ((min_val>-2147483648L) and (max_val<2147483648L)):
                return 'signed long'   # -2147483648L..2147483648L
            return 'unsigned long'

        if t=='float':
            if ((min_val>-1e+30) and (max_val<1e+30)):
                return 'float'
            return 'double'
        
        
        if t=='char':
            self.max_val=maxlen    
            return 'char'

#        print variabele, min_range, max_range







    def  write_binfile (self, variable,datatype, subtype, minrange, maxrange):
        
        if not os.path.exists(self.infodir+'/splitbin'):
            os.makedirs(self.infodir+'/splitbin')

        
        print variable, subtype, minrange, maxrange, self.num_keys
        typecode=self.subtype2typecode[subtype] 
        if self.empty:
            print 'skipping, empty file'
            return 

#        if (datatype=='int' or datatype=='float') and (maxrange is None or minrange is None):
#            return

#        if (maxrange==minrange) :
#            print 'skipping, minrange=maxrange'
#            return
        num_keys=self.num_keys
        if num_keys<8192:
            return
        
        #print self.hist
        hist_keys=sorted(self.hist.keys())
        hist_index={}
        for i,k in enumerate(hist_keys):
            hist_index[k]=i
       # print hist_keys

        if num_keys>65535:
            print 'skipping, too much keys'
            return
        if num_keys==1:
            print 'skipping, no data'
            return
        if datatype=='char':
            typecode='H'
        data=[]
        data2=[]

        #print hist_keys
        f=open(self.infodir+'/split/%s.csv' % variable)
        nr=0
        for line in f:
            nr+=1
            
            s=line.strip()
            if datatype=='int':
                try:
                    d=int(float(s))
                except:
                    if s=='' or s=='-':
                        d=0
                    else:
                        print line
                        raise RuntimeError
                if d<-2147483648L:
                    d=-2147483648L
                if d>2147483648L:
                    d=2147483648L
            

                    
            if datatype=='float':
                try:
                    d=float(s)
                except:
                    s=s.strip()
                    if s=='' or s=='-':
                        d=0.0
            if datatype=='char':                
                d=hist_index[s]
                data2.append(d)
                continue

            val=hist_index[d]
            data.append(val)
            data2.append(d)

        
        f.close()

        f=open(self.infodir+'/splitbin/%s.info' % variable,'wb')
        f.write('min:%s\n' % minrange)
        f.write('max:%s\n' % maxrange)
        if num_keys>=1000:
            f.write('num_keys:1000\n' )
        else:
            f.write('num_keys:%s\n' % num_keys)
        f.close()
        
        
        f=open(self.infodir+'/splitbin/%s.bin' % variable,'wb')
        if num_keys>255:
            data_array=array.array('H',data)
        else:
            data_array=array.array('B',data)
        data_array.tofile(f)
        f.close()

       # print datatype, self.subtype2typecode[subtype]
        f=open(self.infodir+'/splitbin/%s.fullbin' % variable,'wb')
       # print self.subtype2typecode[subtype],data2[:25]
       
        data_array=array.array(typecode,data2)
        data_array.tofile(f)
        f.close()


    def analyse(self):
        g=open(self.infodir+'/col_types.csv','w')
        g.write('filename=%s\n' % self.filename)
        g.write('sep=%s\n' % self.sep)
        for col in self.cols:
            if col=='.':
                break
            f=self.get_type(col)
            f['col']=col
            self.data_info=f
           # self.datatype=f['datatype']
           # try:
           #     self.subtype=self.get_range(col,self.datatype, 0.01, 0.99)
           #     self.typecode=self.subtype2typecode[self.subtype]
           # except:
           #     self.subtype=''
           #     self.typecode=''

            
            #s='%s,%s,%s,%s,' % (col,self.datatype,self.subtype,self.typecode)
            #s+=' '*(40-len(s))
            s='%(col)s,%(datatype)s, \t%(num_keys)d,%(empty)d' %f 
            s+=',%(float_t)d,%(int_t)d,%(str_t)d' % f            
            s+=',\t%(int_min)s,%(int_max)s' % f
            s+=',\t%(float_min)s,%(float_max)s' % f
            s+=',\t%(min_val)s,%(max_val)s' % f
            s+='\n'
                      
            g.write(s)

    def writebin(self):
        return
        for col in self.cols:
            if col=='.':
                break
            self.datatype=self.get_type(col)    
            self.subtype=self.get_range(col,self.datatype, 0.01, 0.99)
            self.typecode=self.subtype2typecode[self.subtype]        
            self.write_binfile (col,self.datatype,self.subtype, self.min_range, self.max_range)
        

    


    
    


