import random, os, sys, inspect
sys.path.insert(0,'f:\\cbs\\heatmapr')
import man2csv


class man2csv:
    def __init__(self):    
        pass



    def read(self): 
        
        f=open(self.infile)        
        g=open(self.outfile,'a')
       
        out=[variable['varname'] for variable in self.variables]
       	g.write(self.sep.join(out)+'\n') 
        for line in f:
        	out=[line[variable['pos_start']:variable['pos_end']] for variable in self.variables]
        	g.write(self.sep.join(out)+'\n') 



    def check_args(self, args):    # alleen defaults zetten.

        defaults=[
            ['infile',';',True,''],
            ['outfile',';',False,''],
            ['sep',';',False,''],
            ['variables',[],'False,''],                       
        ]
       

        self.module_dir=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
      
        
        defaultvars=[]
        for varinfo in defaults:
            varname=varinfo[0]
            defaultvars.append(varname)
            defaultval=varinfo[1]
            required=varinfo[2]
            helptxt=varinfo[3]
            
            if not (varname in args):
                if required:
                    raise RuntimeError('Missing required variable %s' % varname)
                args[varname]=defaultval

        for varname in args.keys():
            if varname not in defaultvars:
                raise RuntimeError('Unknown variable: %s' % varname)
                                        
        for k,v in args.items():
            setattr(self,k,v)




