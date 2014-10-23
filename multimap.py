import heatmapr,os




args=dict(infile='data\\inkomen_vermogen_neg.csv',
          sep=',',
          outfile='pops\\html\\ivn',
          
          x_var='lft',
          x_min=1,
          x_max=100,
          x_steps=100,
          x_fuzz=10,

          y_var='brutink',
          y_min=1,
          y_max=100000,
          y_steps=100,                
                    
          gradmin=0,          
          gradmax='max',
          gradsteps=20,
          title="inkomen vs vermogen, boxplot",
          xlabel="Leeftijd",
          ylabel="Bruto inkomen",
          fontsize=16,
          numticks=6,
          
          colormap='blue',
          size='1',
          transform='linear',

          controltype='flat',
          dump_html=False,
          imgwidth=100,
          imgheight=100
          
          
          )

j=0
for f in os.listdir('pops\\split'):
    print f
    args['infile']='pops\\split\\'+f
    args['outfile']='pops\\html\\'+f.replace('.csv','')
    args['title']='brutink vs lft:'+f
    args['multi_nr']=j
    j+=1
    c=heatmapr.heatmap()
    c.make_heatmap(args)
