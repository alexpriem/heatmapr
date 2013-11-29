


var colormap_gray=function colormap_gray (N) {	
	var step=256/N;
	var cmap=[];
	var col=0;
	for (var i=0; i<N; i++,c+=step){
		col+=step;
		intcol=parseInt(col);
		cmap.push([intcol,intcol,intcol]);
	}
  return cmap;
}

var colormap_blue=function colormap_blue (N) {
	var step=256/N;
	var cmap=[];
	var col=256;
	for (var i=0; i<N; i++,c+=step){
		col-=step;
		intcol=parseInt(col);
		cmap.push([intcol,intcol,255]);
	}
  return cmap;
}


var colormap_contour5=function colormap_contour5 (N) {

	var step=256/5;
	var cmap=[];
	var col=0;
	for (var i=0; i<N; i++) {
		col+=step;
		if (col>256) col=0;
		cmap.push([col,col,col]);
	}
	return cmap;
}

var colormap_contour10=function colormap_contour10 (N) {

	var step=256/10;
	var cmap=[];
	var col=0;
	for (var i=0; i<N; i++) {
		col+=step;
		if (col>256) col=0;
		cmap.push([col,col,col]);
	}
	return cmap;
}


function build_colormap (N, colorvals){

	var step=parseInt(N/5);	
	var steps=[step,step,step,step,step];
	for (var i=0; i<N-step*5;i++) {
		steps[i]=steps[i]+1;
	}
	var cmap=[];
	var r,g,b, rangesteps;
	
	console.log(steps);
	for (var range=0; range<5; range++) {
		rangesteps=steps[range];
		deltar=(colorvals[range+1][0]-colorvals[range][0])/rangesteps;
		deltag=(colorvals[range+1][1]-colorvals[range][1])/rangesteps;
		deltab=(colorvals[range+1][2]-colorvals[range][2])/rangesteps;
//		console.log("DELTA:",deltar, deltag, deltab);		
		r=colorvals[range][0];
		g=colorvals[range][1];
		b=colorvals[range][2];
		for (var i=0; i<rangesteps; i++) {								
//			console.log(r,g,b);
			cmap.push([parseInt(r),parseInt(g),parseInt(b)]);
			r+=deltar;
			g+=deltag;
			b+=deltab;
		}
	}
	console.log("terrain");
	return cmap;
}

var colormap_terrain=function colormap_terrain (N) {
	
	var colorvals=[
		[51,51,153],
		[0,152,254],
		[0,202,105],
		[255,255,153],
		[128,93,84],
		[255,255,255]];
	var cmap=build_colormap(N, colorvals);	
	console.log(cmap.length);
	return cmap;
}

var colormap_coolwarm=function colormap_coolwarm(N){
    
scale = chroma.scale(['#3A4CC0','white','#B30326']);
cmap=[];
frac=1.0/N;
for (i=0; i<N; i++){
	rgb=scale(i*frac).rgb();
	cmap.push([parseInt(rgb[0]),parseInt(rgb[1]),parseInt(rgb[2])]);
}
return cmap;
}

var colormap_hot=function colormap_hot(N){
    
scale=chroma.scale(['white', 'yellow', 'red', 'black']).correctLightness(true);
cmap=[];
frac=1.0/N;
for (i=0; i<N; i++){
	rgb=scale(i*frac).rgb();
	cmap.push([parseInt(rgb[0]),parseInt(rgb[1]),parseInt(rgb[2])]);
}
return cmap;
}

var colormap_hot2=function colormap_hot2(N){
    
scale=chroma.interpolate.bezier(['white', 'yellow', 'red', 'black']);
cmap=[];
frac=1.0/N;
for (i=0; i<N; i++){
	rgb=scale(i*frac).rgb();
	cmap.push([parseInt(rgb[0]),parseInt(rgb[1]),parseInt(rgb[2])]);
}
return cmap;
}

var colormap_ygb=function colormap_ygb(N){
    
scale=chroma.scale(['yellow', 'green', 'blue']);
cmap=[];
frac=1.0/N;
for (i=0; i<N; i++){
	rgb=scale(i*frac).rgb();
	cmap.push([parseInt(rgb[0]),parseInt(rgb[1]),parseInt(rgb[2])]);
}
return cmap;
}




var colormaps={
	'blue':colormap_blue,
	'gray':colormap_gray,
	'contour5':colormap_contour5,
    'contour10':colormap_contour10,
	'terrain':colormap_terrain,
	'coolwarm':colormap_coolwarm,
	'hot':colormap_hot,	
	'hot2':colormap_hot2,		
	'ygb':colormap_ygb,
        };
