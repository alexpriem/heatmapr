heatmapr
========

Parameters:

**infile**: csv-inputfile. Eerste regel van de csv-file moet de kolomnamen bevatten. 
**sep**:  scheidingsteken, default ';'
**convert_comma**: converteer komma's in getalvelden naar decimale punten (dit gebeurt normalerwijs automatisch, maar kan ook expliciet worden afgedwongen)

**x_var** : kolom in csv-file die variabele voor de x-as aangeeft.
**x_min** : minimumwaarde x-as
**x_max** : maximumwaarde x-as
**x_steps** : aantal stappen/klassen voor de x-as. 

**y_var** : kolom in csv-file die variabele voor de x-as aangeeft.
**y_min** : minimumwaarde y-as
**y_max** : maximumwaarde y-as
**y_steps** : aantal stappen/klassen voor de x-as. 

**weight_var**: optioneel: variabele die het gewicht van ieder record aangeeft. Normalerwijs telt ieder record als 1; met weight_var kunnen andere aantallen (ook negatieve aantallen) worden opgegeven.


**fuzzx**: 
**fuzzy**:
**logx**: logaritmische x-schaal
**logy**: logaritmische y-schaal
**gradmin**: minimumwaarde voor kleurgradient (default 0)
**gradmax**: maximumwaarde voor kleurgradient (default 100)
**gradsteps**: aantal stappen voor kleurgradient (default 40)
**colormap**: te gebruiken kleurmap voor kleurgradient. Default 'blue'. Beschikbare keuzes:'blue','blue2','green', 'red','gray','terrain', 'coolwarm', 'hot', 'hot2','hot3', 'ygb'
**transform** : kleurtransformatie: linear, sqrt, log(2) of log(10). Default linear.

**imgwidth**: breedte van heatmap in pixels
**imgheight**: hoogte van heatmap in pixels 500,False,
**size**: default aggegratiestap; default 1x1 (geen aggegratie)

**xlabel**: label voor x-as
**ylabel**: label voor y-as
**title**: titel boven heatmap

**outfile** : als html gegenereerd moet worden (zie **dump_html**): naam van outputfile
**dump_html** : genereer een opzichzelfstaand html-bestand.

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

**debuglevel**: default 0. 
