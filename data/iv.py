f=open ('iv_raw.csv')
g=open('iv.csv','w')
g.write('inkomen,vermogen,num\n')
j=1
for line in f:
    line=line.replace('  ',' ').replace('  ',' ').replace('  ',' ')
    cols=line.strip().split(' ')
    i=1
    for c in cols:
       g.write ('%d,%d,%s\n'  % (i,j,c))
       i+=1
    #g.write('\n')
    j+=1
g.close()
f.close()
       
