import glob, datetime,sys, gzip, os


selectie='pops'
datadir='.'
infile='p.csv'
indir=datadir+'/'+selectie+'/'+infile
outdir=datadir+'/'+selectie+'/split'
idcols='seccoal1'
sep=','
output=['lft','brutink']
verbose=2



def csv_select (infile, idcol, output, meetfiles):
    
    if infile[-3:]=='.gz':
        f=gzip.open (infile,'r')
    else:
        f=open (infile,'r')
    
    keys=f.readline().strip().split(sep)
    idcolnr=keys.index(idcol)
    outputcols=[]
    for o in output:
        outputcols.append(keys.index(o))

    nr=0
    for line in f:
        nr+=1
        if verbose==2 and nr % 100000==0:
            print infile, nr
        vals=line.strip().split(sep)
        meetpunt=vals[idcolnr].replace('/','_')

        subset=[vals[o] for o in outputcols]        
        meetpuntdata=meetfiles.get(meetpunt,[])
        meetpuntdata.append(sep.join(subset)+'\n')
        meetfiles[meetpunt]=meetpuntdata
            
    return meetfiles


def csv_write (output, meetfiles):

    for filename,meetdata in meetfiles.items():
   #     print filename
        outfilename=outdir+'/'+filename+'.csv'
        writeheader=False
        if not(os.path.isfile(outfilename)):
            writeheader=True        
        f=open(outfilename,'a')
        if writeheader:
            f.write(sep.join(output)+'\n')
        for line in meetdata:
            f.write(line)
        f.close()



if not(os.path.isdir(outdir)):
    os.mkdir(outdir)        
meetfiles={}
meetfiles=csv_select(infile, idcol, output, meetfiles)
csv_write(output,meetfiles)


    

