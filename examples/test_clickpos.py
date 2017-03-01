import sys
sys.path.insert(0,'h:\\src\\heatmapr-master')
import heatmapr




args=dict(infile='data\\test_clickpos.csv',
          sep=',',
          outfile='html\\test_clickpos',
          
          x_var='x',                    
          x_min=0,
          x_max=500,
          x_steps=500,        

          y_var='y',
          y_min=0,
          y_max=500,
          y_steps=500,
                    
          gradmin=0,
          gradmax=100,
          gradsteps=20,
          
          title="test_clickpos",
          y_label="ylabel",
          x_label="xlabel",
          colormap='hot2',          
          size='1',
          transform='linear',

          #dump_html=False,
          dump_html=False,
          imgwidth=500,
          imgheight=500
          )


c=heatmapr.heatmap()
c.make_heatmap(args)
