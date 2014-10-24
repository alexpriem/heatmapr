heatmapr
========

Uitvoeren: maak een python-file aan met de volgende inhoud (of kopieer 'simple.py' uit de examples-directory)
```
import sys
sys.path.insert(0,'f:\\heatmapr')   # of waar de heatmap-software staat.

import heatmapr

args=dict(infile='f:\\examples\\simple_data.csv',		
          sep=',',
          outfile='simple',
          
          x_var='inkomen',
          x_min=1,
          x_max=10,
          x_steps=10,

          y_var='vermogen',
          y_min=1,
          y_max=10,
          y_steps=10,
          
          weight_var='num'
          )


c=heatmapr.heatmap()
c.make_heatmap(args)

```

Parameters:

**infile**: csv-inputfile. Eerste regel van de csv-file moet de kolomnamen bevatten. 
**sep**:  scheidingsteken, default ';'
**convert_comma**: converteer komma's in getalvelden naar decimale punten (dit gebeurt normalerwijs automatisch, maar kan ook expliciet worden afgedwongen)

**x_var** : kolom in csv-file die variabele voor de x-as aangeeft.
**x_min** : minimumwaarde x-as
**x_max** : maximumwaarde x-as
**x_steps** : aantal stappen/klassen voor de x-as. Aantal stappen in x-richting moet voor nu nog gelijk zijn aan aantal stappen in y-richting; ongelijke
stapgroottes leveren nu een niet-passende y- of x-schaal op, omdat het aantal stappen wordt gematched met het aantal 'pixels' in de breedte/hoogte (zie **imgwidth** / **imgheight**).
**x_fuzz**: 

**y_var** : kolom in csv-file die variabele voor de x-as aangeeft.
**y_min** : minimumwaarde y-as
**y_max** : maximumwaarde y-as
**y_steps** : aantal stappen/klassen voor de x-as. 
**y_fuzz**:

**weight_var**: optioneel: variabele die het gewicht van ieder record aangeeft. Normalerwijs telt ieder record als 1; met weight_var kunnen andere aantallen (ook negatieve aantallen) worden opgegeven.


**logx**: logaritmische x-schaal
**logy**: logaritmische y-schaal
**gradmin**: minimumwaarde voor kleurgradient (default 0)
**gradmax**: maximumwaarde voor kleurgradient (default 100)
**gradsteps**: aantal stappen voor kleurgradient (default 40)
**colormap**: te gebruiken kleurmap voor kleurgradient. Default 'blue'. Beschikbare keuzes:'blue','blue2','green', 'red','gray','terrain', 'coolwarm', 'hot', 'hot2','hot3', 'ygb'
**transform** : kleurtransformatie: linear, sqrt, log(2) of log(10). Default linear.
**size**: default aggegratiestap: 1=maximale resolutie, 2=2x2 bins, 3=3x3 bins, etc. (voorzover mogelijk binnen combinatie van imgwidth/x_steps en imhgheigt/y_steps).
**missing_color**: kleur die gebruikt wordt voor 'missings' (bins waar geen punten in vallen, met waarde 0), op te geven als [Red, Green, Blue, Alpha]; rgba-waardes gaan van 0-255; alpha=0 is doorschijnend, alpha=255 is volledig niet doorschijnend. Default 'min', voor de laagste waarde uit de gradient (zie **colormap**).
**gradient_invert**: keer volgorde van gradient om (van wit naar blauw ipv van blauw naar wit).
**gradient_bimodal**: bimodale gradient met centerwaarde; splits gradient op in 2 delen, bedoeld voor positief/negatieve waardes.
**gradcenter**:  center van bimodale gradient, default 0.



**imgwidth**: breedte van heatmap in pixels
**imgheight**: hoogte van heatmap in pixels 500,False,
**size**: default aggegratiestap; default 1x1 (geen aggegratie)

**xlabel**: label voor x-as
**ylabel**: label voor y-as
**title**: titel boven heatmap
**fontsize**:  grootte van font voor xlabel, ylabel en title.
**numticks**: aantal ticks voor x-as/y-as. None: laat bepaling van aantal ticks over aan d3.

**outfile** : als html gegenereerd moet worden (zie **dump_html**): naam van outputfile
**dump_html** : genereer een opzichzelfstaand html-bestand.

**stats_enabled**: bij maken van heatmap, gemiddelde en mediaan voor iedere x-waarde berekenen. Default True.
**plot_mean**: Waardes 'True' of 'False', default 'False'. Gemiddelde x-waardes plotten in heatmap. Gemiddelde wordt berekend over alle waardes in inputbestand, 
ook over de waardes die buiten min/max van huidige as liggen.
**plot_mean_pixelsize**: Lijndikte/Puntdikte
**plot_mean_color**:  Kleur: lijst met [R,G,B]-waardes. R/G/B waardes lopen van 0 tot 255. Default [0,0,0]: zwart

**plot_median** Waardes 'True' of 'False', default 'False'. Mediaan van x-waardes plotten in heatmap.  Mediaan wordt berekend over alle waardes in inputbestand, 
ook over de waardes die buiten min/max van huidige as liggen.
**plot_median_pixelsize** 2, False,
**plot_median_color** Kleur: lijst met [R,G,B]-waardes; R/G/B waardes lopen van 0 tot 255. Default [0,0,255]: blauw

**info_datafile** bestandsnaam met aparte x-y waardes die in heatmap geplot worden (bv. statlinedata). Ongetest, bevat mogelijk bugs.
**info_pixelsize**: Lijndikte/Puntdikte
**info_color**:Kleur: lijst met [R,G,B]-waardes; R/G/B waardes lopen van 0 tot 255. Default [0,0,255]: blauw



**use_dots**: True/False; True: plot 'dots' die aantal representeren. Te gebruiken tot aantallen van ~25 (wordt nu nog niet getest/afgebroken op grotere aantallen, browser loopt ws. vast); maximale resolutie waar dit voor te gebruiken is is ws 25x25. Zie iv.py/ivn.py
**dot_color**: kleur van dots. Default 'blue'. 
**dot_dotsize**: grootte van dots in pixels, default 5.
**dot_boxsize**: ruimte om serie dots heen; 1=geen ruimte, 0.0=dots zitten op center van box. Default 0.6.
**dot_use_gradient**: True/False: gebruik ipv 'dot_color' als kleur, de kleurenmap van 'colormap' als kleuring.
**dot_show_background**: True/False: gebruik een heatmap met inverse gradient tov de dotplot als achtergrond.

**multi_nr**: default 0; bij waardes boven 0 worden meerdere heatmaps aangemaakt binnen 1 html-file, en weergegeven in 1 html-file. Experimenteel. 
Imgwidth/imgheight wordt op 100 gezet. Zie multimap.py/multisplit.py
**multi_cols**: heatmaps worden gegroepeerd in een rijen met 'multi_cols'-kolommen; default 5.

**debuglevel**: default 0. 
