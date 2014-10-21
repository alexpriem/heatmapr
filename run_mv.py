import make_heatmap




args=dict(infile='data\ib_mv_2010_v.csv',
          sep=';',
          outfile='v',
          
          x_var='LFT_V',
          x_min=0,
          x_max=100,
          x_steps=500,
          x_fuzz=10,

          y_var='BELIB1_V',
          y_min=0,
          y_max=100000,
          y_steps=500,          
                    
          gradmin=0,
          gradmax='max',
          title="Vrouwen met hoger inkomen dan man",
          ylabel="Inkomen box 1",
          xlabel="Leeftijd",
          colormap='blue',
          size='1',
          transform='log10',
          dump_html=False,
          imgwidth=500,
          imgheight=500
          )


c=heatmapr.heatmap()
c.make_heatmap(args)
