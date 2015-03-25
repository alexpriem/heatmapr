import sys
sys.path.insert(0,'f:\\cbs\\heatmapr')
import heatmapr


args=dict(infile='data\\inkomen_vermogen.csv',
          sep=',',
          outfile='html\\dotplot_1',
          
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

          displaymode='dotplot',
          colormap='blue',
          size='1',
          transform='linear',          
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
args['outfile']='html\\dotplot_2'
c.make_heatmap(args)
args['dot_boxsize']=0.6
args['outfile']='html\\dotplot_3'
c.make_heatmap(args)
args['dot_use_gradient']=True
args['outfile']='html\\dotplot_4'
c.make_heatmap(args)
args['dot_show_background']=True
args['outfile']='html\\dotplot_5'
c.make_heatmap(args)
