import sys
sys.path.insert(0,'h:\\src\\heatmapr')
import heatmapr




args=dict(infile='data\\example_x_date_year.csv',
          sep=',',
          outfile='html\\example_date_year_no_fuzz',
          
          x_var='x',
          x_data_type='date_year',
          x_dateformat='%Y',
          x_min='1900',
          x_max='2000',
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
          y_label="label voor y as",
          x_label="label voor x as",
          colormap='hot2',
          dump_html=True,
          imgwidth=500,
          imgheight=500
          )


c=heatmapr.heatmap()
c.make_heatmap(args)
args['x_fuzz']=5
args['outfile']='html\\example_date_year_fuzz'
c.make_heatmap(args)     
