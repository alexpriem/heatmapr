import sys
sys.path.insert(0,'f:\\cbs\\heatmapr')

import heatmapr


args=dict(infile='f:\\cbs\\heatmapr\\data\\inkomen_vermogen.csv',
          sep=',',
          outfile='iv_a',
          
          x_var='inkomen',
          x_min=1,
          x_max=10,
          x_steps=10,

          y_var='vermogen',
          y_min=1,
          y_max=10,
          y_steps=10,
          
          weight_var='num',
                    
          gradmin=0,
          gradmax='max',
          gradsteps=20,
          title="inkomen vs vermogen, boxplot",
          xlabel="Inkomen",
          ylabel="Vermogen",
          
          colormap='blue',
          size='1',
          transform='linear',
          use_dots=True,
          dot_color='blue',
          dot_dotsize=5,
          dot_boxsize=0.0,
          dot_use_gradient=False,
          dot_show_background=False,

          dump_html=True,
          imgwidth=500,
          imgheight=500
          )


c=heatmapr.heatmap()
c.make_heatmap(args)

args['dot_boxsize']=1.0
args['outfile']='iv_b'
c.make_heatmap(args)
args['dot_boxsize']=0.6
args['outfile']='iv_c'
c.make_heatmap(args)
args['dot_use_gradient']=True
args['outfile']='iv_d'
c.make_heatmap(args)
args['dot_show_background']=True
args['outfile']='iv_e'
c.make_heatmap(args)
