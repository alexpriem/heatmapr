	
var colormapname='blue';
var size=1;
var transform='log10';
var crashnr=0;

var histmax=0;

var inv_x=0;
var inv_y=0;
var inv_xy=0;
var inv_grad=0;


var click_colormap=function click_colormap (evt) {
	colormapname=$(this).attr('data-colormap');
	
	colormap=colormaps[colormapname];
	colormaplength=colormap.length-1;

	console.log('click_colormap',colormapname,  colormaplength);
	$('.colormapname ').removeClass('active_selectie');
	$(this).addClass('active_selectie');

	//console.log('click_colormap',colormap);
	draw_heatmap();
	draw_colormap();
	return false;
}



function init_colormaps()
{

var html='<li class="sel_heading"> Colormaps: </li>';
for (var key in colormaps) {
  if (colormaps.hasOwnProperty(key)) {
    html+='<li class="colormapname" data-colormap="'+key+'">'+key+'</li>';
  }
}

$('#sel_colormap').html(html);
$('.colormapname').on('click',click_colormap);
$('.colormapname').on('mouseenter ',enter_selectie);
$('.colormapname').on('mouseout ',leave_selectie);

$('.colormapname').slice(0,1).addClass('active_selectie');
 //for (colormapname in colormaps)  break;
 colormap=colormaps[colormapname];
 colormaplength=colormap.length-1;
 console.log('init_colormap:',colormapname,colormaplength);
}





function calc_heatmap () {

	console.log("calc_heatmap: invx, invy, invxy, inv_grad:",inv_x, inv_y, inv_xy, inv_grad);

	
	hist=new Array(colormap.length);
	for (i=0; i<hist.length; i++) {
		hist[i]=0;
	}


	console.log('calc_heatmap',size);
	for (var i=0; i<imgheight; i++) {
		for (var j=0; j<imgwidth;  j+=size) {		
			val=0;

			if (inv_xy) 
				ptr=j*imgheight+i;
			else
				ptr=i*imgwidth+j;
			if (size==1) val=data[ptr];
			if (size>1) {
				for (cx=0; cx<size; cx++) {
					for (cy=0; cy<size; cy++) {
						val+=data[ptr+cx+cy*imgwidth];
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
	    			
	    			
			indexval=~~((val-tgradmin)/(tdelta)*colormaplength);  					
			if ((indexval<0) || (indexval>=colormaplength)){
				if (crashnr<10)
					console.log('crash:indexval, negval,tgradmin,delta:',indexval, val, tgradmin,tdelta);
				crashnr++;

				if (indexval<0) indexval=0;
				if (indexval>=colormaplength) indexval=colormaplength-2;
			}

			indexval=parseInt(indexval);
			hist[indexval]++;
			if (inv_grad) {
				indexval=colormaplength-indexval;
			}

			if (inv_y) {
				ptr=(imgheight-i)*imgwidth; 
			} else {
				ptr=i*imgwidth;
			}

			if (inv_x) {
				ptr+=imgwidth-j;
			} else {
				ptr+=j;
			}

			backbuffer[ptr]=indexval;
			if (size>1) {
				for (cx=0; cx<size; cx++) {
					for (cy=0; cy<size; cy++) {
						backbuffer[ptr+cy*imgwidth+cx]=indexval;
						}
					}				//cy
			}  // size >1
			
			
		} //j
//		console.log("i:",i);
	}	//i


	histmax=0;
	for (i=1; i<hist.length; i++) 
		if (hist[i]>histmax) histmax=hist[i];
 
console.log('hist:',hist);
//console.log('hist2:',backbuffer);
console.log("calc_heatmap, len:",backbuffer.length);
}



function draw_heatmap() {

	console.log("draw_heatmap:",size, colormapname,transform);
	calc_heatmap();
	//draw_histogram();	
	var indexval=0;
	var color=[];
	console.log("draw_heatmap:",backbuffer.length);
	for (i=0,j=0; i<backbuffer.length; i++,j+=4) {
			indexval=backbuffer[i];
			color=colormap[indexval];
	    	mapdata[j] =  color[0];  // imgd[i];
	    	mapdata[j+1] = color[1];  //i & 0xff; //color[1];  // imgd[i];
	    	mapdata[j+2] = color[2];  // imgd[i];
	    	mapdata[j+3] = 0xff; //i & 0x3f;  // imgd[i];
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
		

	html+='<li class="sizename" data-size="1">'+imgwidth+"x"+imgheight+'</li>';
	sizetable=[2,5,10,20,50,100,200,500,1000,2000,5000];
	j=0;
	size=sizetable[0];
	while ((imgwidth/size>9) && (imgheight/size)>9) {		
		html+='<li class="sizename" data-size="'+size+'">'+Math.floor(imgwidth/size)+"x"+Math.floor(imgheight/size)+'</li>';
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

	console.log("click_transform:", transform);	
	if (transform=='linear') {
		tgradmax=gradmax;
		tgradmin=gradmin;
	}
	if (transform=='sqrt') {
		tgradmax=Math.sqrt(gradmax);
		tgradmin=Math.sqrt(gradmin);
	}
	if (transform=='log') {
		tgradmax=Math.log(gradmax);
		if (tgradmin>0) {
			tgradmin=Math.log(gradmin);
			}
		else {
			tgradmin=0;
		}
	}
	if (transform=='log10') {
		tgradmax=Math.log(gradmax)/Math.LN10;		
		if (tgradmin>0) {
			tgradmin=Math.log(gradmin)/Math.LN10;
			}
		else {
			tgradmin=0;
		}

	}
	tdelta=tgradmax-tgradmin;
	console.log(transform, tgradmin, tgradmax);
	draw_heatmap();
	return false;
}


function init_gradient_transforms() {
 	$('.transformname').on('click',click_transform);
 	$('.transformname').on('mouseenter ',enter_selectie);
  	$('.transformname').on('mouseout ',leave_selectie);
  	$('.transformname').slice(0,1).addClass('active_selectie');	
  	transform='linear';
  	tgradmax=gradmax;
  	tgradmin=gradmin;
  	tdelta=tgradmax-tgradmin;
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
}



function draw_colormap () {

console.log("draw_colormap", colormaplength);

$('.colormap').remove();
var step=4;
var barlength=imgheight/3;
var barstep=(barlength/colormaplength);
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
  
 for (i=0; i<colormap.length; i+=step) {
 	color=colormap[i];
	chart.append("rect")
		.attr("class","colormap")
		.attr("x",imgwidth+75)
		.attr("y",25+10+barlength-barstep*i)
		.attr("width",20)
		.attr("height",barstep*(step+1))
		.style("fill","rgb("+color[0]+","+color[1]+","+color[2]+")")
		.style("stroke","rgb("+color[0]+","+color[1]+","+color[2]+")")
		.style("stroke-width","1px");

 }


  var colorScale=d3.scale.linear();
  colorScale.domain([gradmax,gradmin]);
  colorScale.range([0,barlength]); 

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

$('.hist_2d').remove();
$('.hist_x').remove();
$('.hist_y').remove();
for (i=1; i<hist.length; i++) {
 	color=colormap[i];
	chart.append("rect")
		.attr("class","hist_2d")
		.attr("x",imgwidth+75+i)
		.attr("y",imgheight-(hist[i]/histmax)*0.4*imgheight)
		.attr("width",1)
		.attr("height",(hist[i]/histmax)*0.4*imgheight)
		.style("fill","rgb("+color[0]+","+color[1]+","+color[2]+")")
		.style("stroke","rgb("+color[0]+","+color[1]+","+color[2]+")")
		.style("stroke-width","1px");
 }


  var xScale=d3.scale.linear();  
  xScale.range([0,hist.length]); 
  xScale.domain([0,histmax]);
  
  var xyAxis=d3.svg.axis();  
  xyAxis.scale(xScale)   
  		.ticks(5)    
       .orient("bottom");
  //console.log(chart);
  offsetx=imgwidth+75;
  offsety=imgheight;

  chart.append("g")
        .attr("class","xaxis hist_2d")
        .attr("transform","translate("+offsetx+","+offsety+")")
        .call(xyAxis);
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
	y=parseInt(imgheight-(evt.pageY-$(this).position().top-25));
	console.log(x, y);
	if ((x<0) || (y<0) || (x>imgwidth) || (y>imgheight)) return;
	
	$('.hist_2d').remove();
	$('.hist_x').remove();
	$('.hist_y').remove();

	max=0;
	for (i=0; i<imgwidth; i++) { 		
		val=data[y*imgheight+i];
		if (val>max) max=val;
	}

	for (i=0; i<imgwidth; i++) { 	
	 	val=data[y*imgheight+i];
	 	color=colormap[val];
		chart.append("rect")
			.attr("class","hist_x")
			.attr("x",imgwidth+75+i)
			.attr("y",imgheight-(val/max)*0.25*imgheight)
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
	 	val=data[i*imgwidth+x];
	 	if (val>max) max=val;
	 }
	
for (i=0; i<imgheight; i++) { 	
	 	val=data[i*imgwidth+x];
	 	color=colormap[val];
		chart.append("rect")
			.attr("class","hist_y")
			.attr("x",imgwidth+75+i)
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
  xScale.domain([xmin,xmax]);
  yScale.domain([ymax,ymin]);
  yScale.range([0,imgheight]); 

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

	

 chart.append("svg:line")
 	.attr("class","hist_x")
    .attr("x1", 50)
    .attr("y1", y+25)
    .attr("x2", width+50)
    .attr("y2", y+25)
    .style("stroke", "rgb(130,8,8)");


 	chart.append("svg:line")
 	.attr("class","hist_y")
    .attr("x1", x+50)
    .attr("y1", 25)
    .attr("x2", x+50)
    .attr("y2", imgwidth+25)
    .style("stroke", "rgb(8,8,130)");    
}
function init_hist_xy () {

	console.log('init_hist');
	 $("#heatmap_svg").on('click',update_hist_x_y);
	// $("#heatmap_svg").on('mousedown',update_hist_x_y);
}