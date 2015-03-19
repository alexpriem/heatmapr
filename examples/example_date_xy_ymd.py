import sys
sys.path.insert(0,'h:\\src\\heatmapr')
import heatmapr




args=dict(infile='data\\example_xy_date_YMD.csv',
          sep=',',
          outfile='html\\example_date_xy_ymd',
          
          x_var='x',
          x_data_type='date_day',
          x_dateformat='%Y-%m-%d',
          x_min='2010-01-02',
          x_max='2011-05-15',
          x_steps=500,          

          y_var='y',
          y_data_type='date_day',
          y_dateformat='%Y-%m-%d',
          y_min='2010-01-02',
          y_max='2011-05-15',
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

