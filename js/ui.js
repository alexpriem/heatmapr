	
var colormapname='blue';
var size=1;
var transform='linear';
var crashnr=0;

var histmax=0;

var inv_x=0;
var inv_y=0;
var inv_xy=0;
var inv_grad=0;
var newdata=[];

var click_colormap=function click_colormap (evt) {
	colormapname=$(this).attr('data-colormap');
	
	colormap=colormaps[colormapname];
	colormaplength=colormap.length-1;

	console.log('click_colormap',colormapname,  colormaplength);
	$('.transformname ').removeClass('active_selectie');
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
 for (colormapname in colormaps)  break;
 colormap=colormaps[colormapname];
 colormaplength=colormap.length-1;
 console.log('init_colormap:',colormapname,colormaplength);
}





function calc_heatmap () {


	newdata=[];	
	hist=new Array(colormap.length);
	for (i=0; i<hist.length; i++) {
		hist[i]=0;
	}
	console.log('calc_heatmap',size);
	for (var i=0; i<height; i+=size) {
		for (var j=0; j<width; j+=size) {		
			val=0;

			ptr=i*width+j;
			if (size==1) val=data[ptr];
			if (size>1) {
				for (cx=0; cx<size; cx++) {
					for (cy=0; cy<size; cy++) {
						val+=data[ptr+cx+cy*width];
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
	    			
			indexval=~~((val-tminval)/(tdelta)*colormaplength);  		
			
			if ((indexval<0) || (indexval>=colormaplength)){
				if (crashnr<10)
					console.log('crash:indexval, negval,tminval,delta:',indexval, val, tminval,tdelta);
				crashnr++;

				if (indexval<0) indexval=0;
				if (indexval>=colormaplength) indexval=colormaplength-2;
			}

			indexval=parseInt(indexval);
			newdata.push(indexval+1);
			hist[indexval]++;
		} //j
//		console.log("i:",i);
	}	//i


	histmax=0;
	for (i=0; i<hist.length; i++) 
		if (hist[i]>histmax) histmax=hist[i];
 
console.log('hist:',hist);
//console.log('hist2:',newdata);
console.log("calc_heatmap, len:",newdata.length);
}



function draw_heatmap() {

	console.log("draw_heatmap:",size, colormapname,transform);

	calc_heatmap();
	draw_histogram();	
	var indexval=0;
	var color=[];
	console.log("draw_heatmap:",newdata.length);
	for (i=0,j=0; i<newdata.length; i++,j+=4) {
			indexval=newdata[i];
			if (indexval<0) { console.log ("zero:",indexval);}
			if (indexval>255) { console.log ("255:",indexval); }
			color=colormap[indexval];
			try {
	    		color=colormap[indexval];
	    	} catch (err) {
	    		console.log('crash:',indexval); 
	    	}

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
	$('.transformname ').removeClass('active_selectie');
	$(this).addClass('active_selectie');	
	draw_heatmap();
	return false;
}

function init_sizes() {

	var html='<li class="sel_heading"> Sizes:</li>';
		

	html+='<li class="sizename" data-size="1">'+width+"x"+height+'</li>';
	sizetable=[2,5,10,20,50,100,200,500,1000,2000,5000];
	j=0;
	size=sizetable[0];
	while ((width/size>9) && (height/size)>9) {		
		html+='<li class="sizename" data-size="'+size+'">'+Math.floor(width/size)+"x"+Math.floor(height/size)+'</li>';
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
		tmaxval=maxval;
		tminval=minval;
	}
	if (transform=='sqrt') {
		tmaxval=Math.sqrt(maxval);
		tminval=Math.sqrt(minval);
	}
	if (transform=='log') {
		tmaxval=Math.log(maxval);
		if (tminval>0) {
			tminval=Math.log(minval);
			}
		else {
			tminval=0;
		}
	}
	if (transform=='log10') {
		tmaxval=Math.log(maxval)/Math.LN10;		
		if (tminval>0) {
			tminval=Math.log(minval)/Math.LN10;
			}
		else {
			tminval=0;
		}

	}
	tdelta=tmaxval-tminval;
	console.log(transform, tminval, tmaxval);
	draw_heatmap();
	return false;
}


function init_gradient_transforms() {
 	$('.transformname').on('click',click_transform);
 	$('.transformname').on('mouseenter ',enter_selectie);
  	$('.transformname').on('mouseout ',leave_selectie);
  	$('.transformname').slice(0,1).addClass('active_selectie');	
  	transform='linear';
  	tmaxval=maxval;
  	tminval=minval;
  	tdelta=tmaxval-tminval;
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
  xScale.range([0,width]); 
  xScale.domain([xmin,xmax]);
  yScale.domain([ymax,ymin]);
  yScale.range([0,height]); 

  var xAxis=d3.svg.axis();
  var yAxis=d3.svg.axis();  
  xAxis.scale(xScale)       
       .orient("bottom");
  yAxis.scale(yScale)       
       .orient("left");

  //console.log(chart);
  chart.append("g")
        .attr("class","xaxis")
        .attr("transform","translate(50,"+(height+25)+")")
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
var barlength=height/3;
var barstep=(barlength/colormaplength);
console.log(barlength, barstep);
chart.append("rect")
	.attr("class","colormap")
	.attr("x",width+75)
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
		.attr("x",width+75)
		.attr("y",25+10+barlength-barstep*i)
		.attr("width",20)
		.attr("height",barstep*(step+1))
		.style("fill","rgb("+color[0]+","+color[1]+","+color[2]+")")
		.style("stroke","rgb("+color[0]+","+color[1]+","+color[2]+")")
		.style("stroke-width","1px");

 }


  var colorScale=d3.scale.linear();
  colorScale.domain([maxval,minval]);
  colorScale.range([0,barlength]); 

  var colorAxis=d3.svg.axis();  
  colorAxis.scale(colorScale)       
       .orient("right");

  scalepos=width+95;
  chart.append("g")
        .attr("class","yaxis colormap")
        .attr("transform","translate("+scalepos+",35)")
        .call(colorAxis);        


 
}



function draw_histogram () {

console.log("draw_histogram:", histmax, colormaplength);

$('.hist_2d').remove();
for (i=0; i<hist.length; i++) {
 	color=colormap[i];
	chart.append("rect")
		.attr("class","hist_2d")
		.attr("x",width+75+i)
		.attr("y",height-(hist[i]/histmax)*0.4*height)
		.attr("width",1)
		.attr("height",(hist[i]/histmax)*0.4*height)
		.style("fill","rgb("+color[0]+","+color[1]+","+color[2]+")")
		.style("stroke","rgb("+color[0]+","+color[1]+","+color[2]+")")
		.style("stroke-width","1px");
 }

}