import sys
sys.path.insert(0,'f:\\heatmapr')

import heatmapr


args=dict(infile='f:\\examples\\inkomen_vermogen.csv',
          sep=',',
          outfile='simple',
          
          x_var='inkomen',
          x_min=1,
          x_max=10,
          x_steps=10,

          y_var='vermogen',
          y_min=1,
          y_max=10,
          y_steps=10,
          
          weight_var='num',
          )


c=heatmapr.heatmap()
c.make_heatmap(args)
