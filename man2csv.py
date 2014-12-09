import random, os, sys, inspect


class man2csv:
    def __init__(self):    
        pass



    def read(self): 
        
        f=open(self.infile)        
        if self.append:
            g=open(self.outfile,'a')
        else:
            g=open(self.outfile,'w')
            out=[variable['varname'] for variable in self.variables]
            g.write(self.sep.join(out)+'\n') 
        matches=self.matches

       
        for line in f:
            out=[line[variable['pos_start']-1:variable['pos_end']] for variable in self.variables]
            write=True
            if len(matches)>0:
                write=False
                outdict={variable['varname']:line[variable['pos_start']-1:variable['pos_end']] for variable in self.variables}
                for match in matches:
                    dataval=outdict[match['varname']]
                    matchval=match['value']
                    if match['check']=='>=':
                        #print dataval, matchval, dataval>matchval, dataval>=matchval
                        if dataval>=matchval:
                            write=True
            if write:
                g.write(self.sep.join(out)+'\n') 



    def check_args(self, args):    # alleen defaults zetten.

        defaults=[
            ['infile',';',True,''],
            ['outfile',';',False,''],
            ['sep',';',False,''],
            ['append',False,False,''],
            ['variables',[],False,''],
            ['matches',[],False,'']            
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




