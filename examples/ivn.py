import heatmapr




args=dict(infile='data\\inkomen_vermogen_neg.csv',
          sep=',',
          outfile='ivn',
          
          x_var='inkomen',
          x_min=1,
          x_max=10,
          x_steps=10,

          y_var='vermogen',
          y_min=1,
          y_max=10,
          y_steps=10,
          
          weight_var='num',
                    
          gradmin=-10,
          gradcenter=0,
          gradmax='max',
          gradsteps=20,
          title="inkomen vs vermogen, boxplot",
          xlabel="Inkomen",
          ylabel="Vermogen",
          fontsize=16,
          numticks=6,
          
          colormap='blue',
          size='1',
          transform='linear',
          use_dots=True,
          dot_color='blue',
          dot_dotsize=5,
          dot_boxsize=0.5,
          dot_use_gradient=True,
          bimodal=True,
          gradient_invert=False,

          controltype='flat',
          dump_html=True,
          imgwidth=500,
          imgheight=500
          
          
          )


c=heatmapr.heatmap()
c.make_heatmap(args)
