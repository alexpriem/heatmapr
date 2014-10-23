import heatmapr




args=dict(infile='data\\tvc902v2.csv',
          sep=',',
          outfile='tvc902v',
          
          x_var='lft',
          x_min=0,
          x_max=100,
          x_steps=500,          

          y_var='Lnsv',
          y_min=0,
          y_max=5000,
          y_steps=500,

          weight_var='num',
                    
          gradmin=0,
          gradmax='max',
          title="Lnsv mannen, maandtijdvak februari 2009",
          ylabel="Loon",
          xlabel="Leeftijd",
          colormap='blue',
          missing_color='min', #[128,128,128],
          size='1',
          transform='linear',
          dump_html=False,
          imgwidth=500,
          imgheight=500
          )


c=heatmapr.heatmap()
c.make_heatmap(args)
