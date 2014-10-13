import contour




args=dict(infile='data\\inkomen_vermogen.csv',
          sep=',',
          outfile='iv',
          
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
          
          colormap='blue',
          size='1',
          transform='linear',
          use_dots=True,
          dot_color='blue',
          dot_size=5,

          dump_html=False,
          imgwidth=500,
          imgheight=500
          )


c=contour.contour()
c.run_contour(args)
