import os,sys
sys.path.insert(0,'h:\\src\\heatmapr')
import heatmapr


# voor het uitvoeren van dit voorbeeld eerst 'python multisplit.py' uitvoeren.



args=dict(infile='',
          sep=',',
          outfile='',
          
          x_var='x',
          x_min=0,
          x_max=50,
          x_steps=100,
          x_fuzz=10,

          y_var='y',
          y_min=1,
          y_max=5000,
          y_steps=100,                
                    
          gradmin=0,          
          gradmax='max',
          gradsteps=20,
          title="multimap 2",
          xlabel="xlabel",
          ylabel="ylabel",
          fontsize=16,
          numticks=6,
          
          colormap='blue',
          size='1',
          transform='linear',

          multi_cols=3,   # aantal heatmaps op een rij
          
          controltype='flat',
          dump_html=True,
          imgwidth=100,
          imgheight=100,   
          
          )

j=0
for f in os.listdir('data\\split'):
    print f
    args['infile']='data\\split\\'+f
    args['outfile']='html\\example_multimap'
    args['title']='colorcode:'+f
    args['multi_nr']=j
    j+=1
    if j==1:
        c=heatmapr.heatmap()
    c.make_heatmap(args)
