import sys
sys.path.insert(0,'e:\\src\\heatmapr')
import heatmapr




args=dict(infile='data\\example_simple.csv',
          sep=',',
          outfile='html\\example_verysimple',
          
          x_var='x',                    
          x_min=0,
          x_max=50,

          y_var='y',
          y_min=0,
          y_max=5000
            )


c=heatmapr.heatmap()
c.make_heatmap(args)
