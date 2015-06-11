import sys
sys.path.insert(0,'h:\\src\\heatmapr')
import heatmapr




args=dict(infile='data\\example_split1.csv',
          sep=',',
          outfile='html\\example_split2',
          
          x_var='x',
          x_min=0,
          x_max=50,
          x_steps=500,
          x_fuzz=10,

          y_var='y',
          y_min=0,
          y_max=5000,
          y_steps=500,

          multimap=['color1','color2'],

          multimap_labels={'color1':{'1':'label1','2':'label2','3':'label3','4':'label4','5':'label5','6':'label6'},
                               'color2':{'1':'a','2':'b'}},
          gradmin=0,
          gradmax='max',
          gradsteps=14,
          title="multimap2",
          y_label="ylabel",
          x_label="xlabel",
          colormap='qualitative14',
          missing_color=[0,0,0,0], #'min', #[128,128,128],
          size='1',
          transform='linear',
          dump_html=True,
          
          imgwidth=500,
          imgheight=500
          )


c=heatmapr.heatmap()
c.make_heatmap(args)
