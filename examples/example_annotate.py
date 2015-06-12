import sys
sys.path.insert(0,'e:\\src\\heatmapr')
import heatmapr




args=dict(infile='data\\example_simple.csv',
          sep=',',
          outfile='html\\example_annotate',
          
          x_var='x',                    
          x_min=0,
          x_max=50,

          y_var='y',
          y_min=0,
          y_max=5000,
          annotate={'annotatie1':{'rect':[[0,0],[50,100]],
                                'text':'dit is de tekst van annotatie1'},
                     'annotatie2':{'line':[[0,0],[50,100]],
                                'text':'dit is de tekst van annotatie2'},
                     'annotatie3':{'area':[[0,0],[50,100]],
                                'text':'dit is de tekst van annotatie3'},
                     'annotatie4':{'area_up':[[0,0],[50,100]],
                                'text':'dit is de tekst van  annotatie4'},
                     'annotatie5':{'area_down':[[0,0],[50,100]],
                                'text':'dit is de tekst van annotatie5'},
                     'annotatie6':{'area_left':[[0,0],[50,100]],
                                'text':'dit is de tekst van annotatie6'},
                     'annotatie7':{'area_left':[[0,0],[50,100]],
                                 'text':'dit is de tekst van annotatie7'},
                     'annotatie8':{'polygon':[[0,0],[50,100],[25,250]],
                                 'text':'dit is de tekst van annotatie8'}
                     },
              dump_html=False
# extra opties:
# lijnkleur, lijndikte, fill, fillkleur, fillalpha, textfile
# visibility: none / click / hover / always
          
          
            )


c=heatmapr.heatmap()
c.make_heatmap(args)
