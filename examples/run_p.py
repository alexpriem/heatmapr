import sys
sys.path.insert(0,'f:\\cbs\\heatmapr')
import heatmapr




args=dict(infile='f:\\cbs\\heatmapr\\data\\tvc902v2.csv',
          sep=',',
          outfile='tvc902v',
          
          x_var='lft',
          x_min=0,
          x_max=100,
          x_steps=100,          

          y_var='Lnsv',
          y_min=0,
          y_max=5000,
          y_steps=100,

          weight_var='num',
                    
          gradmin=0,
          gradmax='max',
          title="Lnsv vrouwen, maandtijdvak februari 2009",
          ylabel="Loon",
          xlabel="Leeftijd",
          colormap='blue',
          missing_color=[0,0,0,0], #'min', #[128,128,128],
          size='1',
          transform='linear',
          dump_html=False,
          imgwidth=100,
          imgheight=100
          )


c=heatmapr.heatmap()
c.make_heatmap(args)
