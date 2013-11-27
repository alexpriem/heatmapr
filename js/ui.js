/* settings */	
var colormapname='terrain';
var size=1;
var transform='linear';
var crashnr=0;
var skipzero=true;

var histmax=0;

var inv_x=0;
var inv_y=1;
var inv_xy=1;
var inv_grad=0;

/* storage */

var colormap=[];
var val=0;
var chart;
var backbuffer, transposebuf;
var imgData, mapdata;


var xpix2img=parseInt(imgwidth/xpixels);
var ypix2img=parseInt(imgheight/ypixels);
if ((xpixels>0) && (ypixels>0)) {
	var realimgwidth=xpixels*xpix2img;
	var realimgheight=ypixels*ypix2img;
} else {
//upscale
}

// sanity checks
if (gradmin<1) {gradmin=1;}


function init_databuffers () {

chart = d3.select("#heatmap_svg");

// first, create a new ImageData to contain our pixels
imgData = ctx.createImageData(imgwidth, imgheight); // width x height
try {
    transposebuffer= new Float32Array  (xpixels*ypixels);
    } catch(x){
    transposebuffer= new Array  (xpixels*ypixels);
}

try {
    backbuffer= new Uint32Array  (imgwidth*imgheight);
    } catch(x){
    backbuffer= new Array  (imgwidth*imgheight);
}
mapdata = imgData.data;
}






var click_colormap=function click_colormap (evt) {
	colormapname=$(this).attr('data-colormap');
	
	console.log('click_colormap',colormapname);
	colormap=colormaps[colormapname](gradsteps);
	colormaplength=colormap.length-1;
	console.log('click_colormap',colormapname,  colormaplength);
	$('.colormapname ').removeClass('active_selectie');
	$(this).addClass('active_selectie');
	
	draw_heatmap();
	return false;
}



function init_colormaps()
{

var html='<li class="sel_heading"> Colormaps: </li>';
var selclas='';
for (var key in colormaps) {
  if (colormaps.hasOwnProperty(key)) {
  	if (key==colormapname) 
  		selclass='active_selectie';
  	else
  		selclass='';
    html+='<li class="colormapname '+selclass+'" id="colormap_'+key+'" data-colormap="'+key+'">'+key+'</li>';
  }
}

$('#sel_colormap').html(html);
$('.colormapname').on('click',click_colormap);
$('.colormapname').on('mouseenter ',enter_selectie);
$('.colormapname').on('mouseout ',leave_selectie);

$('#colormapname_'+colormapname).addClass('active_selectie');
 //for (colormapname in colormaps)  break;
 colormap=colormaps[colormapname](gradsteps);
 colormaplength=colormap.length-1;
 console.log('init_colormap:',colormapname,colormaplength,gradsteps);
 //console.log('init_colormap:',colormap);
}


function update_gradient () {

	console.log('update_gradient:');
	gradmax=$('#edit_gradmax').val();
	gradsteps=$('#edit_gradsteps').val();
	gradmin=$('#edit_gradmin').val();
	console.log('update_gradient:',gradmin, gradmax, gradsteps);
	colormap=colormaps[colormapname](gradsteps);	
	draw_heatmap();
}


function init_colormap_inputs() {

chart.append("foreignObject")
	.attr("width", 150)
	.attr("height", 50)
	.attr("x",imgwidth+150)
	.attr("y",35)
	.append("xhtml:body")
	.style("font", "14px Helvetica")
	.html("<input type='text' id='edit_gradmax'name='gradmax' value='"+gradmax+"' size=4/>");

chart.append("foreignObject")
	.attr("width", 150)
	.attr("height", 50)
	.attr("x",imgwidth+150)
	.attr("y",105)
	.append("xhtml:body")
	.style("font", "14px Helvetica")
	.html("<input type='text' id='edit_gradsteps'  name='gradsteps' value='"+gradsteps+"' size=4/>");

chart.append("foreignObject")
	.attr("width", 150)
	.attr("height", 50)
	.attr("x",imgwidth+150)
	.attr("y",185)
	.append("xhtml:body")
	.style("font", "14px Helvetica")
	.html("<input type='text' id='edit_gradmin'  name='gradmin' value='"+gradmin+"' size=4/>");

$("#edit_gradmax").on('change',update_gradient);
$("#edit_gradsteps").on('change',update_gradient);
$("#edit_gradmin").on('change',update_gradient);

}



function calc_heatmap () {

	console.log("calc_heatmap: invx, invy, invxy, inv_grad:",inv_x, inv_y, inv_xy, inv_grad);
	
	hist=new Array(gradsteps);
	for (i=0; i<gradsteps; i++) {
		hist[i]=0;
	}

	console.log('calc_heatmap',size);
	var ptr2=0;
	maxval=0;
	for (var i=0; i<ypixels; i+=size) {
		for (var j=0; j<xpixels;  j+=size) {		
			val=0;
			if (inv_xy) 
				ptr=j*ypixels+i;
			else
				ptr=i*xpixels+j;
			if (size==1) val=data[ptr];
			if (size>1) {
				for (cx=0; cx<size; cx++) {
					for (cy=0; cy<size; cy++) {
						val+=data[ptr+cx+cy*xpixels];
						}
					}				//cy
			}  // size >1
			

	    	if (transform=='sqrt') {
				val=Math.sqrt(val);
	    	}
			if (transform=='log2') {
				if (val>0) {
					val=Math.log(val);
				} else { 
					val=0;
				}
	    	}
			if (transform=='log10') {
				if (val>0) {
					val=Math.log(val)/Math.LN10;
				} else { 
					val=0;
				}
	    	}
	    			
			ptr2++;			
			transposebuffer[ptr2]=val;			
			if (val>maxval) maxval=val;	    			

		} //j
//		console.log("i:",i);
	}	//i



	if (gradmax=='max') {
		tgradmax=maxval;
	} else {
		tgradmax=gradmax;
	}
	tgradmin=gradmin;
	tdelta=tgradmax-tgradmin;

	var line=0;
	for (i=0; i<imgwidth*imgheight; i++) {
		backbuffer[i]=0;
	}
	xstep=xpix2img*size;
	ystep=ypix2img*size;
	ptr=-xstep; // whut?
	u=0;
	v=0;

	for (i=0; i<ptr2; i++)	{	
		val=transposebuffer[i];

		indexval=~~((val-tgradmin)/(tdelta)*gradsteps);  					
		if (indexval<0) indexval=0;
		if (indexval>=gradsteps) indexval=gradsteps-1;

		indexval=parseInt(indexval);
		hist[indexval]++;
		if ((inv_grad)  && (indexval!=0)) {			
				indexval=colormaplength-indexval;
		}

		if (inv_y) {
			ptr=(imgheight-v*ystep)*imgwidth; 
		} else {
			ptr=v*ystep*imgwidth;
		}

		if (inv_x) {
			ptr+=imgwidth-u*xstep;
		} else {
			ptr+=u*xstep;
		}

		//if (line==0) { console.log("val=",val);}
		//ptr=u*xstep+v*ystep*imgwidth;
		for (cy=0; cy<ystep; cy++) {
			for (cx=0; cx<xstep; cx++) {			
				backbuffer[ptr+cy*imgwidth+cx]=indexval;
				}
			}
		u++;
		line+=xstep;		
		if (line>=imgwidth) {			
			u=0;
			v++;			
			line=0;
		}
	}			//cy

histmax=0;
for (i=1; i<gradsteps; i++) 
	if (hist[i]>histmax) histmax=hist[i];
	
 
//console.log('hist:',hist);
//console.log('hist2:',backbuffer);

console.log("calc_heatmap, maxval:",maxval);
console.log("calc_heatmap, len:",backbuffer.length);
}



/* draw_heatmap:
	- heatmap uitrekenen
	- minima/maxima bepalen
   - colormap tekenen; 
   - heatmap tekenen.

*/

function draw_heatmap() {

	console.log("draw_heatmap:",size, colormapname,transform);
	calc_heatmap();
	draw_colormap();

	draw_histogram();	

	/* eigenlijke heatmap plotten */

	var indexval=0;
	var color=[];

	console.log("draw_heatmap:",backbuffer.length);
	for (i=0,j=0; i<backbuffer.length; i++,j+=4) {
			indexval=backbuffer[i];
			if ((indexval!=0) || (!skipzero)) {	  // waardes die 0 zijn niet plotten
				color=colormap[indexval];
	    		mapdata[j] =  color[0];  
	    		mapdata[j+1] = color[1];  
	    		mapdata[j+2] = color[2];  
	    		mapdata[j+3] = 0xff; 
			} else {
				mapdata[j] =  0xff;  
	    		mapdata[j+1] = 0xff; 
	    		mapdata[j+2] = 0xff; 
	    		mapdata[j+3] = 0xff; 
	    	}

		}	
	console.log('putdata');
	ctx.putImageData(imgData, 0, 0);		 

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

function init_sizes() {

	var html='<li class="sel_heading"> Sizes:</li>';
		

	html+='<li class="sizename" data-size="1">'+xpixels+"x"+ypixels+'</li>';
	sizetable=[2,5,10,20,50,100,200,500,1000,2000,5000];
	j=0;
	size=sizetable[0];
	while ((xpixels/size>9) && (ypixels/size)>9) {		
		html+='<li class="sizename" data-size="'+size+'">'+Math.floor(xpixels/size)+"x"+Math.floor(ypixels/size)+'</li>';
		j++;
		size=sizetable[j];		
	}
	size=1;
	$('#sel_size').html(html);

   $('.sizename').slice(0,1).addClass('active_selectie');	
   $('.sizename').on('click',click_size);
   $('.sizename').on('mouseenter ',enter_selectie);
   $('.sizename').on('mouseout ',leave_selectie);
 // console.log("initsize");
}



var click_transform=function click_size (evt) {

	transform=$(this).attr('data-transform');
	$('.transformname ').removeClass('active_selectie');
	$(this).addClass('active_selectie');

/*	tgradmax=gradmax;
	tgradmin=gradmin;
*/	
	console.log("click_transform:", transform,tgradmin, tgradmax);				
	draw_heatmap();
	return false;
}



function init_gradient_transforms() {
 	$('.transformname').on('click',click_transform);
 	$('.transformname').on('mouseenter ',enter_selectie);
  	$('.transformname').on('mouseout ',leave_selectie);
  	$('#trans_'+transform).addClass('active_selectie');	  	
  	tgradmax=gradmax;
  	tgradmin=gradmin;
}



function click_data_transform () {

	var id=$(this).attr('id');
	if (id=='inv_x') {inv_x=1-inv_x; var state=inv_x;}
	if (id=='inv_y') {inv_y=1-inv_y; var state=inv_y;}
	if (id=='inv_xy') {inv_xy=1-inv_xy; var state=inv_xy;}
	if (id=='inv_grad') {inv_grad=1-inv_grad;	var state=inv_grad;}

	if (state) {
		$(this).addClass('active_selectie');
	} else {
		$(this).removeClass('active_selectie');
	}
	draw_heatmap();
}


function init_data_transforms() {
 	$('.swapname').on('click',click_data_transform);
 	$('.swapname').on('mouseenter ',enter_selectie);
  	$('.swapname').on('mouseout ',leave_selectie);  	
}


  function draw_axes () {


  var xScale=d3.scale.linear();
  var yScale=d3.scale.linear();
  xScale.range([0,imgwidth]); 
  xScale.domain([xmin,xmax]);
  yScale.domain([ymax,ymin]);
  yScale.range([0,imgheight]); 

  var xAxis=d3.svg.axis();
  var yAxis=d3.svg.axis();  
  xAxis.scale(xScale)       
       .orient("bottom");
  yAxis.scale(yScale)       
       .orient("left");

  //console.log(chart);
  chart.append("g")
        .attr("class","xaxis")
        .attr("transform","translate(50,"+(imgheight+25)+")")
        .call(xAxis);
  chart.append("g")
        .attr("class","yaxis")
        .attr("transform","translate(50,25)")
        .call(yAxis);        

  chart.append("text")      // text label for the x axis
  		.attr("class","xaxis")
        .attr("x", imgwidth/2 )
        .attr("y",  imgheight+70 )
        .style("text-anchor", "middle")
        .attr("font-family", "sans-serif")
  		.attr("font-size", "16px")
  		.attr("font-weight", "bold")
        .text(xlabel);
  chart.append("text")      // text label for the x axis
    	.attr("class","yaxis")
        .attr("x", 0 )
        .attr("y", 0)
        .attr("font-family", "sans-serif")
  		.attr("font-size", "16px")
  		.attr("font-weight", "bold")        
        .attr("transform","translate(10,"+(imgheight/2)+")rotate(270)")
        .style("text-anchor", "middle")
        .text(ylabel);
  chart.append("text")      // text label for the x axis
    	.attr("class","yaxis")
        .attr("x", imgwidth/2+50 )
        .attr("y", 15)
        .attr("font-family", "sans-serif")
  		.attr("font-size", "16px")
  		.attr("font-weight", "bold")         
        .style("text-anchor", "middle")
        .text(title);

}



function draw_colormap () {

console.log("draw_colormap", colormaplength);


$('.colormap').remove();
var barlength=imgheight/3;
var barstep=(barlength/gradsteps);
console.log(barlength, barstep);
chart.append("rect")
	.attr("class","colormap")
	.attr("x",imgwidth+75)
	.attr("y",25+10)
	.attr("width",20)
	.attr("height",barlength)
	.style("fill","none")
	.style("stroke","black")
	.style("stroke-width","1px");
  
 for (i=0; i<gradsteps; i++) {
 	color=colormap[i];
	chart.append("rect")
		.attr("class","colormap")
		.attr("x",imgwidth+75)
		.attr("y",25+10+barlength-barstep*i)
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
  }
  if (transform=='log2') {
  	var colorScale=d3.scale.log().base(2);
  }
  if (transform=='sqrt') {
  	var colorScale=d3.scale.pow().exponent(0.5);
  }

  console.log('Colorscale, datadomain',datamin, datamax);
  console.log('Colorscale, domain',tgradmin, tgradmax);
  colorScale.domain([tgradmax, tgradmin]);
  colorScale.range([0,barlength]); 
  colorScale.ticks(8);

  var colorAxis=d3.svg.axis();  
  colorAxis.scale(colorScale)       
       .orient("right");

  scalepos=imgwidth+95;
  chart.append("g")
        .attr("class","yaxis colormap")
        .attr("transform","translate("+scalepos+",35)")
        .call(colorAxis);        
 
}



function draw_histogram () {

console.log("draw_histogram:", histmax, colormaplength);
//console.log(colormap);

histwidth=500;
barwidth=500/gradsteps;

$('.hist_2d').remove();
$('.hist_x').remove();
$('.hist_y').remove();
for (i=1; i<gradsteps; i++) {
 	color=colormap[i];
 	//console.log(hist[i],histmax,imgheight-(hist[i]/histmax)*0.4*imgheight); 	
 	chart.append("rect")
		.attr("class","hist_2d")
		.attr("x",imgwidth+75+i*barwidth)
		.attr("y",imgheight-(hist[i]/histmax)*0.4*imgheight)
		.attr("width",barwidth)
		.attr("height",(hist[i]/histmax)*0.4*imgheight)
		.style("fill","rgb("+color[0]+","+color[1]+","+color[2]+")")
		.style("stroke","rgb("+color[0]+","+color[1]+","+color[2]+")")
		.style("stroke-width","1px");		
 }

  
  console.log('hist:',transform);
  var heatmap_hist_xScale=d3.scale.linear();
  
  heatmap_hist_xScale.range([0,gradsteps*barwidth]);
  heatmap_hist_xScale.domain([tgradmin,tgradmax]);

  var heatmap_hist_yScale=d3.scale.linear();
  heatmap_hist_yScale.range([0,0.4*imgheight]);
  heatmap_hist_yScale.domain([histmax,0]);

  
  var heatmap_hist_xAxis=d3.svg.axis(); 
  var heatmap_hist_yAxis=d3.svg.axis();   
  heatmap_hist_xAxis.scale(heatmap_hist_xScale)   
  		.ticks(5)    
       .orient("bottom");
  heatmap_hist_yAxis.scale(heatmap_hist_yScale)   
  		.ticks(5)    
       .orient("left");

  //console.log(chart);
  offsetx=imgwidth+75;
  offsety=imgheight;

  chart.append("g")
        .attr("class","xaxis hist_2d")
        .attr("transform","translate("+offsetx+","+offsety+")")
        .call(heatmap_hist_xAxis); 
  offsety=0.6*imgheight;
  chart.append("g")
        .attr("class","yaxis hist_2d")
        .attr("transform","translate("+offsetx+","+offsety+")")
        .call(heatmap_hist_yAxis); 

        /*
        .attr("class","yaxis hist_2d")
        .attr("transform","translate("+offsetx+","+offsety+")")
        .call(heatmap_hist_yAxis);*/

}



function init_manipulation () {

	$('#sharpen').on('click',sharpen);
	$('#denoise').on('click',denoise);
	$('#pointilize').on('click',pointilize);	
	$('#edge').on('click',edge);
	$('#blur').on('click',blurfast);
	$('#lighten').on('click',lighten);
	
	$('.man').on('mouseenter ',enter_selectie);
  	$('.man').on('mouseout ',leave_selectie);
}

function denoise () {
	console.log("denoise");
	var img= document.getElementById("heatmap_canvas");
	var newimg=Pixastic.process(img,"removenoise",{});
	console.log('newimg', newimg);
}


function sharpen () {
	console.log("sharpen");
	var img= document.getElementById("heatmap_canvas");
	var newimg=Pixastic.process(img,"sharpen",{amount:0.5});
}



function pointilize () {
	console.log("pointilize");
	var img= document.getElementById("heatmap_canvas");
	var newimg=Pixastic.process(img, "pointillize", {radius:5, density:1.5, noise:1.0, transparent:false});
}

function edge () {
	console.log("edge");
	var img= document.getElementById("heatmap_canvas");
	var newimg=Pixastic.process(img, "edges", {mono:true,invert:true});
}

function blurfast () {
	console.log("blurfast");
	var img= document.getElementById("heatmap_canvas");
	var newimg=Pixastic.process(img, "blurfast", {amount:0.5});
}


function lighten () {
	console.log("lighten");
	var img= document.getElementById("heatmap_canvas");
	var newimg=Pixastic.process(img, "lighten", {amount:0.5});
}



function update_hist_x_y (evt) {

	console.log("update_hist_x_y");	
	x=parseInt(evt.pageX-$(this).position().left-50);
	y=parseInt(evt.pageY-$(this).position().top-25);
	console.log(x, y);

	if ((x<0) || (y<0) || (x>imgwidth) || (y>imgheight)) {
		if ((x>imgwidth) && (x<imgwidth+100) && (y<150)) {
			//toggle_gradcontrols();					
		}
	}return;
	
	$('.hist_2d').remove();
	$('.hist_x').remove();
	$('.hist_y').remove();

	max=0;
	for (i=0; i<imgwidth; i++) { 		
		val=backbuffer[y*imgheight+i];
		if (val>max) max=val;
	}

	console.log(max);
	
	for (i=0; i<imgwidth; i++) { 	
	 	val=backbuffer[y*imgheight+i];	 		 	

	 	color=colormap[val];
		chart.append("rect")
			.attr("class","hist_y")
			.attr("x",imgwidth+75+i)
			.attr("y",parseInt(imgheight-(val/max)*0.25*imgheight))
			.attr("width",1)
			.attr("height",(val/max)*0.25*imgheight)
			.style("fill","rgb(8,8,130)")
			.style("stroke","rgb(8,8,130)")
			
			//.style("fill","rgb("+color[0]+","+color[1]+","+color[2]+")")
			//.style("stroke","rgb("+color[0]+","+color[1]+","+color[2]+")")
			.style("stroke-width","1px");
		 }

		
max=0;
for (i=0; i<imgheight; i++) { 	
	 	val=backbuffer[i*imgwidth+x];
	 	if (val>max) max=val;
	 }
	
for (i=0; i<imgheight; i++) { 	
	 	val=backbuffer[i*imgwidth+x];
	 	color=colormap[val];
		chart.append("rect")
			.attr("class","hist_y")
			.attr("x",2*imgwidth+75-i)
			.attr("y",imgheight-(val/max)*0.25*imgheight-0.3*imgheight)
			.attr("width",1)
			.attr("height",(val/max)*0.25*imgheight)
			.style("fill","rgb(130,8,8)")
			.style("stroke","rgb(130,8,8)")
			
			//.style("fill","rgb("+color[0]+","+color[1]+","+color[2]+")")
			//.style("stroke","rgb("+color[0]+","+color[1]+","+color[2]+")")
			.style("stroke-width","1px");
		 }

  

  var xScale=d3.scale.linear();
  var yScale=d3.scale.linear();
  xScale.range([0,imgwidth]); 
  xScale.domain([ymin,ymax]);       // bug: what's called 'xscale'/'yscale' is on the wrong position
  yScale.domain([xmin,xmax]);
  yScale.range([0,imgwidth]); 

  var xAxis=d3.svg.axis();
  var yAxis=d3.svg.axis();  
  xAxis.scale(xScale)       
       .orient("bottom");
  yAxis.scale(yScale)       
       .orient("bottom");

  //console.log(chart);
  offsetx=imgwidth+75;
  offsety=imgheight;

  chart.append("g")
        .attr("class","yaxis hist_x")
        .attr("transform","translate("+offsetx+","+offsety+")")
        .call(yAxis);
  offsety=0.7*imgheight;

  chart.append("g")
        .attr("class","xaxis hist_y")
        .attr("transform","translate("+offsetx+","+offsety+")")        
        .call(xAxis);        


  chart.append("text")      // text label for the x axis
  		.attr("class","xaxis")
        .attr("x",  1.5*imgwidth+50 )
        .attr("y",  imgheight+35 )
        .style("text-anchor", "middle")
        .attr("font-family", "sans-serif")
  		.attr("font-size", "16px")
  		.attr("font-weight", "bold")
        .text(xlabel);
  chart.append("text")      // text label for the x axis
    	.attr("class","yaxis")
        .attr("x", 1.5*imgwidth+50 )
        .attr("y", imgheight-120 )
        .attr("font-family", "sans-serif")
  		.attr("font-size", "16px")
  		.attr("font-weight", "bold")                
        .style("text-anchor", "middle")
        .text(ylabel);
	

 chart.append("svg:line")
 	.attr("class","hist_x")
    .attr("x1", 50)
    .attr("y1", y+25)
    .attr("x2",imgwidth+50)
    .attr("y2", y+25)
    .style("stroke", "rgb(8,8,130)");


 	chart.append("svg:line")
 	.attr("class","hist_y")
    .attr("x1", x+50)
    .attr("y1", 25)
    .attr("x2", x+50)
    .attr("y2", imgwidth+25)
    .style("stroke", "rgb(130,8,8)");    
}
function init_hist_xy () {

	console.log('init_hist');
	$("#heatmap_svg").on('click',update_hist_x_y);
	//$("#heatmap_svg").on('mousedown',update_hist_x_y);
}