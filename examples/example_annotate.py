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
          annotate=[{'annotatie1':{'rect':[(0,0),(50,100)],
                                'text':'annotatie1'},
                     'annotatie2':{'line':[(0,0),(50,100)],
                                'text':'annotatie2'},
                     'annotatie3':{'area':[(0,0),(50,100)],
                                'text':'annotatie3'},
                     'annotatie4':{'area_up':[(0,0),(50,100)],
                                'text':'annotatie4'},
                     'annotatie5':{'area_down':[(0,0),(50,100)],
                                'text':'annotatie5'},
                     'annotatie6':{'area_left':[(0,0),(50,100)],
                                'text':'annotatie6'},
                     'annotatie7':{'area_left':[(0,0),(50,100)],
                                 'text':'annotatie7'},
                     'annotatie8':{'polygon':[(0,0),(50,100),(25,250)],
                                 'text':'annotatie8'}
                     }],
              dump_html=False
        
            )


c=heatmapr.heatmap()
c.make_heatmap(args)
