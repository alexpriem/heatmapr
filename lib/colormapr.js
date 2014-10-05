

var colormap_gray=function colormap_gray (N) {	
	var step=256/N;
	var cmap=[];
	var col=0;
	for (var i=0; i<N; i++){
		col+=step;
		intcol=parseInt(col);
		cmap.push([255-intcol,255-intcol,255-intcol]);
	}
  return cmap;
}

var colormap_blue2=function colormap_blue2 (N) {
	var step=256/N;
	var cmap=[];
	var col=256;
	for (var i=0; i<N; i++){
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



var colormap_terrain=function colormap_terrain (N) {
	
	scale = chroma.scale(['#333399','#0098fe','#00ca69','#ffff99','#805d54','#ffffff']);
	cmap=[];
	frac=1.0/N;
	for (i=0; i<N; i++){
		rgb=scale(i*frac).rgb();
		cmap.push([parseInt(rgb[0]),parseInt(rgb[1]),parseInt(rgb[2])]);
	}
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

var colormap_hot3=function colormap_hot3(N){
    
scale=chroma.scale(['white', '#ffce00', '#ffae00', 'black']).correctLightness(true);
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


var colormap_blue=function colormap_blue(N){

scale=chroma.scale(['white', '#d2ecf7','#9cd7ef','#00a1cd','#008dd1','#004b9a', '#002c61']);

// dump for debug-purposes
cmap=[];
frac=1.0/N;
for (i=0; i<N; i++){
	rgb=scale(i*frac).rgb();
	cmap.push([parseInt(rgb[0]),parseInt(rgb[1]),parseInt(rgb[2])]);
//	console.log('%d:%d,%d,%d',i,rgb[0],rgb[1],rgb[2]);
}


scale=chroma.scale(['white', '#d2ecf7','#9cd7ef','#00a1cd','#008dd1','#004b9a', '#002c61']).correctLightness(true);
cmap=[];
frac=1.0/N;
for (i=0; i<N; i++){
	rgb=scale(i*frac).rgb();
	cmap.push([parseInt(rgb[0]),parseInt(rgb[1]),parseInt(rgb[2])]);
//	console.log('%d:%d,%d,%d',i,rgb[0],rgb[1],rgb[2]);
}
return cmap;
}

var colormap_red=function colormap_red(N){
    
scale=chroma.scale(['white', '#fee4c7','#fccb8d','#f39200','#ea5906','#e4002c', '#af081f']).correctLightness(true);
cmap=[];
frac=1.0/N;
for (i=0; i<N; i++){
	rgb=scale(i*frac).rgb();
	cmap.push([parseInt(rgb[0]),parseInt(rgb[1]),parseInt(rgb[2])]);
}
return cmap;
}

var colormap_green=function colormap_green(N){
    
scale=chroma.scale(['white', '#ecf2d0','#dae49b','#afcb05','#85bc22','#00a139', '#007f2c']).correctLightness(true);
cmap=[];
frac=1.0/N;
for (i=0; i<N; i++){
	rgb=scale(i*frac).rgb();
	cmap.push([parseInt(rgb[0]),parseInt(rgb[1]),parseInt(rgb[2])]);
}
return cmap;
}










var enter_selectie=function enter_selectie (evt) {
	$(this).addClass('hover_selectie');
}
var leave_selectie=function enter_selectie (evt) {
	$(this).removeClass('hover_selectie');
}


var click_size=function click_size (evt) {
	size=parseInt($(this).attr('data-size'));
	$('.sizename ').removeClass('active_selectie');
	$(this).addClass('active_selectie');	

	draw_heatmap();
	return false;
}


function init_sizes(widget_id) {
	   
	console.log('init_sizes:', widget_id)
   $('.sizename_'+widget_id).slice(0,1).addClass('active_selectie');	
   $('.sizename_'+widget_id).on('click',click_size);
   $('.sizename_'+widget_id).on('mouseenter ',enter_selectie);
   $('.sizename_'+widget_id).on('mouseout ',leave_selectie);
 }



var click_transform=function click_transform (evt) {

	transform=$(this).attr('data-transform');
	widget_id=$(this).attr('data-widget');
	
	topnode=document.getElementById(widget_id);
	gradient=topnode.getAttribute('data-gradient');
	gradient_node=document.getElementById(gradient);	
	gradient_node.setAttribute('transform',transform);	
	console.log('click_transform:', widget_id, gradient_node.id);
	draw_colormap (gradient_node);		
	$('.transformname_'+widget_id).removeClass('active_selectie');
	$(this).addClass('active_selectie');

	return false;
}



function init_gradient_transforms(widget_id, transform) {

 	$('.transformname_'+widget_id).on('click',click_transform);
 	$('.transformname_'+widget_id).on('mouseenter ',enter_selectie);
  	$('.transformname_'+widget_id).on('mouseout ',leave_selectie);
  	$('#trans_'+transform+'_'+widget_id).addClass('active_selectie');	  	
}



function click_data_transform () {

	var id=$(this).attr('id');
	var topnode=document.getElementById(widget_id);
	var gradient=topnode.getAttribute('data-gradient');
	var gradient_node=document.getElementById(gradient);
	

	if (id=='inv_grad') {		
		var gradient_invert=topnode.getAttribute('gradient_invert');
		gradient_invert=1-gradient_invert;
		gradient_node.setAttribute('gradient_invert',gradient_invert);	
		var state=gradient_invert;
	}

	if (state) {
		$(this).addClass('active_selectie');
	} else {
		$(this).removeClass('active_selectie');
	}

	widget_id=$(this).attr('data-widget');	
	draw_colormap (gradient_node);
	return false;
}





var click_colormap=function click_colormap (evt) {

	colormapname=$(this).attr('data-colormap');			
	widget_id=$(this).attr('data-widget');
	console.log('click_colormap',colormapname);
	$('.colormapname_'+widget_id).removeClass('active_selectie');
	$(this).addClass('active_selectie');
	
	topnode=document.getElementById(widget_id);
	gradient=topnode.getAttribute('data-gradient');
	gradient_node=document.getElementById(gradient);
	gradient_node.setAttribute('colormapname',colormapname);
	var gradsteps=gradient_node.getAttribute('gradient_steps')
	gradient_node.colormap=gradient_node.colormaps[colormapname](gradsteps);

	
	draw_colormap (gradient_node);

	return false;
}




function init_colormaps(widget_id, colormapname)
{
console.log('init_colormap:',colormapname,'#colormap_'+colormapname+'_'+widget_id);

$('.colormapname_'+widget_id).on('click',click_colormap);
$('.colormapname_'+widget_id).on('mouseenter ',enter_selectie);
$('.colormapname_'+widget_id).on('mouseout ',leave_selectie);

$('#colormap_'+colormapname+'_'+widget_id).addClass('active_selectie');
 
 //colormap=colormaps[colormapname](gradsteps); 
 
}




function update_gradient (e) {

	
	console.log('update_gradient:');
	if (e.keyCode == '13') {
		widget_id=$(this).attr('data-widget');
		gradmax=$('#max_'+widget_id).val();
		gradsteps=$('#steps_'+widget_id).val();
		gradmin=$('#min_'+widget_id).val();
		console.log('update_gradient:',widget_id, gradmin, gradmax, gradsteps);


		topnode=document.getElementById(widget_id);
		gradient=topnode.getAttribute('data-gradient');
		gradient_node=document.getElementById(gradient);	
		var colormapname=gradient_node.getAttribute('colormapname');		
		console.log('map/#',topnode, gradient, gradient_node);
		console.log(gradient_node.colormaps)
		console.log ('map:',colormapname, gradsteps);
		console.log('grad:',gradient_node.colormaps[colormapname]);

		gradient_node.colormap=gradient_node.colormaps[colormapname](gradsteps);
		gradient_node.setAttribute('gradient_min', gradmin);
		gradient_node.setAttribute('gradient_max',gradmax);
		gradient_node.setAttribute('gradient_steps',gradsteps);
		draw_colormap (gradient_node);

	}
}


function init_colormap_inputs(widget_id) {

	console.log('init_inputs');
	$("#min_"+widget_id).on('keydown',update_gradient);
	$("#max_"+widget_id).on('keydown',update_gradient);
	$("#steps_"+widget_id).on('keydown',update_gradient);	
}




function init_controls (node, gradientnode) {

    console.log('created:', node.id);

    colormaps=[];
    var colormapnames=gradientnode.colormapnames;
    for (i=0; i<colormapnames.length; i++){
        colormaps.push({name:colormapnames[i], widget_id:node.id});
    }

	xpixels=gradientnode.getAttribute('xpixels');
	ypixels=gradientnode.getAttribute('ypixels');
	show_size=gradientnode.getAttribute('show_size');
	sizes=[];
	if (show_size=='true') {
		show_size=true;
	} else {
		show_size=false;
	}

	if (show_size) {
		sizetable=[2,5,10,20,50,100,200,500,1000,2000,5000];
		j=0;
		size=sizetable[0];		
		while ((xpixels/size>9) && (ypixels/size)>9) {		
			el={};
			el.size_x_size=Math.floor(xpixels/size)+"x"+Math.floor(ypixels/size);
			el.size=size;
			el.sizenr=j;
			el.widget_id=node.id;
			j++;
			size=sizetable[j];		
			sizes.push(el);
		}
	}

    var source   = $("#entry-template").html();        
    var template = Handlebars.compile(source); 
    var data = {
         widget_id : node.id,
         min: gradientnode.getAttribute('gradient_min'),
         max: gradientnode.getAttribute('gradient_max'),
         steps: gradientnode.getAttribute('gradient_steps'),
         transform: gradientnode.getAttribute('transform'),
         colormaps: colormaps, 
         show_size: show_size,
         sizes: sizes         
       };
    node.innerHTML =template(data);

    console.log('gradient:', node.getAttribute('data-gradient'));
    init_gradient_transforms(node.id, gradientnode.getAttribute('transform'));                            
    init_colormaps(node.id, gradientnode.getAttribute('colormapname'));
    init_colormap_inputs(node.id);
    init_sizes(node.id);
}





// gradient 



function draw_colormap (topnode) {

if (!('id' in topnode)) {
  console.error('draw_colormap:gradient element needs id');
}
 if (typeof(topnode.preAttributeChangedCallback)=='function') {
    topnode.preAttributeChangedCallback();
}


child=topnode.childNodes[0];
topnode.removeChild(child);
var svg=d3.select('#'+topnode.id).append('svg')


var width=topnode.getAttribute('width');
var height=topnode.getAttribute('height');

svg.attr('width',150);
svg.attr('height',300);
var chart=svg.append('svg:g');

console.log('id:',chart );

svg.attr("id",'g_'+topnode.id);
chart.attr("id",'g_'+topnode.id);


if (topnode.hasAttribute('gradient_min_data')){
  var gradmin=topnode.getAttribute('gradient_min_data');  
}
else {
  var gradmin=topnode.getAttribute('gradient_min');
}
if (topnode.hasAttribute('gradient_max_data')){  
  var gradmax=topnode.getAttribute('gradient_max_data');
} else {
  var gradmax=topnode.getAttribute('gradient_max');
}
var gradsteps=topnode.getAttribute('gradient_steps');
var transform=topnode.getAttribute('transform');
var colormap=topnode.colormap;


//chart = d3.select("#svg_"+topnode);
// $('.colormap').remove(); oude element verwijderen.
var barlength=200;
var barstep=(barlength/gradsteps);
console.log(barlength, barstep);
chart.append("rect")  
	.attr("class","colormap")
	.attr("x",75)
	.attr("y",25+10)
	.attr("width",20)
	.attr("height",barlength)
	.style("fill","none")
	.style("stroke","black")
	.style("stroke-width","1px");

//console.log('chartexit:', chart[0][0].innerHTML);

 for (i=1; i<=gradsteps; i++) {
 	color=colormap[i-1];
	chart.append("svg:rect")
		.attr("class","colormap")
		.attr("x",76)
		.attr("y",25+10+barlength-barstep*i-1)
		.attr("width",20)
		.attr("height",barstep)
		.style("fill","rgb("+color[0]+","+color[1]+","+color[2]+")")
		.style("stroke","rgb("+color[0]+","+color[1]+","+color[2]+")")
		.style("stroke-width","1px");

 }



  
  if (transform=='linear') {
	var colorScale=d3.scale.linear();
  }  
  if (transform=='log10') {  	
  	var colorScale=d3.scale.log();
    if (gradmin==0)  {      //bandaid
        gradmin=1;
      }
  }
  if (transform=='log2') {
  	var colorScale=d3.scale.log().base(2);
    if (gradmin==0)  {
        gradmin=1;
      }

  }
  if (transform=='sqrt') {
  	var colorScale=d3.scale.pow().exponent(0.5);
  }

//  console.log('Colorscale, datadomain',datamin, datamax);
  //console.log('Colorscale, domain',tgradmin, tgradmax);
  colorScale.domain([gradmax, gradmin]);
  colorScale.range([0,barlength]); 
  colorScale.ticks(8);

  var colorAxis=d3.svg.axis();  
  colorAxis.scale(colorScale)       
       .orient("right");

  scalepos=95;
  chart.append("g")
        .attr("class","yaxis colormap")
        .attr("transform","translate("+scalepos+",35)")
        .call(colorAxis);        
 
  
 // console.log('chartexit:',chart);
 // console.log('chartexit:',chart[0][0].innerHTML);
 // console.log(topnode.id);
 // topnode.innerHTML =chart[0][0].innerHTML;
    if (typeof(topnode.postAttributeChangedCallback)=='function') {
      topnode.postAttributeChangedCallback();
  }

}



var init_colormap=function init_colormap (i, topnode) {


  console.log('init_colormap'); 
  var default_colormaps={              
            'blue':colormap_blue,
            'blue2':colormap_blue2,
            'green':colormap_green,
            'red':colormap_red, 
            'gray':colormap_gray,
            'terrain':colormap_terrain,
            'coolwarm':colormap_coolwarm,
            'hot':colormap_hot, 
            'hot2':colormap_hot2,   
            'hot3':colormap_hot3,
            'ygb':colormap_ygb,
              };

  var defaults={ width: 150,
              height: 300,
              xpixels: 500,
              ypixels: 500,
              show_size: 'true',
              gradient_min: 0,
              gradient_max: 100,
              gradient_steps: 20,
              transform: 'linear',
              colormaps: default_colormaps ,
              gradient_invert:'false'        
            };

  console.log('init_colormap');
  if (!('id' in topnode)){
    console.error('No id for gradient element');
  }
  
  if (!topnode.hasAttribute('data-controls')) {
    console.error('No controls for gradient element #',topnode.id);
  }
  controlnode=document.getElementById(topnode.getAttribute('data-controls'));


  for (var keyword in defaults) {
      if (defaults.hasOwnProperty(keyword)) {
          if (!topnode.hasAttribute(keyword)){
              //console.log(keyword, defaults[keyword]);
              if (keyword!='colormaps') {
                topnode.setAttribute(keyword, defaults[keyword]);
              }
          }
      }
  }
  

  if (!('postAttributeChangedCallback' in topnode)) {
    topnode.postAttributeChangedCallback=null;
  }
  if (!('preAttributeChangedCallback' in topnode)) {
    topnode.preattributeChangedCallback=null;
  }

  var colormaps=defaults.colormaps;
  colormapnames=[];
  for (var colormapname in colormaps) {
      if (colormaps.hasOwnProperty(colormapname)) {
          colormapnames.push(colormapname);
      }
  }  
  if (!('colormaps' in topnode)) {    
      topnode.colormaps=colormaps;
  }  

  topnode.colormapnames=colormapnames;
  if (!topnode.hasAttribute('colormapname')) {
      topnode.setAttribute('colormapname',colormapnames[0]);
  }
  
  var gradsteps=topnode.getAttribute('gradient_steps');
  var colormapname=topnode.getAttribute('colormapname');
  
  var colormap=colormaps[colormapname](gradsteps);
  topnode.colormap=colormap;

  //console.log('calc_colormap:',colormap);

  init_controls(controlnode, topnode);
  draw_colormap(topnode);
}


var init_gradients=function init__gradients () {
    
  
      $('.colormap-gradient').each(init_colormap); 
      console.log('init done');
  };
