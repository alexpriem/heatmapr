import sys
sys.path.insert(0,'h:\\src\\heatmapr')
import heatmapr


args=dict(infile='data\\inkomen_vermogen.csv',
          sep=',',
          outfile='html\\textplot_a',
          
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

          displaymode='text',
          colormap='blue',
          size='1',
          transform='linear',          
          text_show_background=False,

          dump_html=True,
          imgwidth=500,
          imgheight=500
          )


c=heatmapr.heatmap()
c.make_heatmap(args)
args['text_show_background']=True
args['outfile']='html\\textplot_b'
c.make_heatmap(args)
