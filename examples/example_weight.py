import sys
sys.path.insert(0,'h:\\src\\heatmapr')
import heatmapr




args=dict(infile='data\\example_weight.csv',
          sep=',',
          outfile='html\\example_weight',
          
          x_var='x',                    
          x_min=0,
          x_max=50,
          x_steps=500,          

          y_var='y',
          y_min=0,
          y_max=5000,
          y_steps=500,

          weight_var='num',
                    
          gradmin=0,
          gradmax=20,
          gradsteps=20,
          title="knoop",
          ylabel="label voor y as",
          xlabel="label voor x as",
          colormap='hot2',
          dump_html=True,
          imgwidth=500,
          imgheight=500
          )


c=heatmapr.heatmap()
c.make_heatmap(args)
# tweede heatmap
args['gradmax']='max'  # autoschalen op maximum van alle bins in heatmap
args['gradsteps']=10
args['outfile']='html\\example_weight2'
args['colormap']='ygb'
c.make_heatmap(args)
