import sys
sys.path.insert(0,'h:\\src\\heatmapr')
import heatmapr



# dit werkt nog niet: verandert alleen aslabels, niet daadwerkelijke selectie


args=dict(infile='data\\example_simple.csv',  
          sep=',',
          outfile='html\\example_perc2',
          
          x_var='x',
          x_relative=True,
          x_relative_min=40,
          x_relative_max=60,
          x_min=0,
          x_max=50,          
          x_steps=500,          

          y_var='y',
          y_relative=True,
          y_min=0,
          y_max=5000,          
          y_steps=500,
          
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

