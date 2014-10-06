/* settings */	

var skipzero=true;
var histmax=0;


/* storage */

var colormap=[];
var val=0;
var chart;
var backbuffer, transposebuffer;
var imgData, mapdata;


var xpix2img=parseInt(imgwidth/xpixels);
var ypix2img=parseInt(imgheight/ypixels);

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






var calc_minmax=function calc_heatmap () {

	console.log("calc_heatmap:");
	
	hist=new Array(gradsteps);
	for (i=0; i<gradsteps; i++) {
		hist[i]=0;
	}

	var gradient_node=document.getElementById("cg_a");
	if (gradient_node.need_data_recalc==false) return;

	var weigh_x=opties['weighx'];
	var weigh_y=opties['weighy'];
	console.log('weighx/y:', weigh_x, weigh_y);
	console.log('calc_heatmap:',xpixels, ypixels, size);
	
	var ptr2=0;
	maxval=null;	
	minval=null;
	size=1;  // XXX 
	for (var i=0; i<ypixels; i+=size) {
		for (var j=0; j<xpixels;  j+=size) {		
			val=0;
			ptr=j*ypixels+i;
			if (size==1) val=data[ptr];
			else {
				if (size>1) {
					for (cx=0; cx<size; cx++) {
						for (cy=0; cy<size; cy++) {
							val+=data[ptr+cx+cy*xpixels];
							}
						}				//cy
				}  // size >1
			}
			

			val=val/(size*size);
	    	if (transform=='sqrt') {
	    		if (val>0) {
					val=Math.sqrt(val);
				} else {
					val=-Math.sqrt(-val);
				}
	    	}
			if (transform=='log2') {
				if (val>0) {
					val=Math.log(val);
				} else { 
					val=-Math.log(-val);
				}
	    	}
			if (transform=='log10') {
				if (val>0) {
					val=Math.log(val)/Math.LN10;
				} else { 
					val=-Math.log(-val)/Math.LN10;
				}
	    	}
	    			
			
			if (weigh_x) {
				val=(val/sum_x[j])*xmean;
			}
			if (weigh_y) {
				val=(val/sum_y[i])*ymean;
			}
			ptr2++;		
			transposebuffer[ptr2]=val;			
			if ((val>maxval) || (maxval==null)) maxval=val;
			if ((val<minval) || (minval==null)) minval=val;

		} //j
//		console.log("i:",i);
	}	//i


	
	var gradmax=gradient_node.getAttribute('gradient_max');
	var gradmin=gradient_node.getAttribute('gradient_min');
	var gradsteps=gradient_node.getAttribute('gradient_steps');
	if (gradmax=='max') {
		gradient_node.setAttribute('gradient_max_data', maxval);		
	} else {
		if (gradient_node.hasAttribute('gradient_max_data')) {
			gradient_node.deleteAttribute('gradient_max_data');			
		}		
	}
	if (gradmin=='min') {
		gradient_node.setAttribute('gradient_min_data', minval);		
	} else {
		if (gradient_node.hasAttribute('gradient_min_data')) {
			gradient_node.deleteAttribute('gradient_min_data');			
		}		
	}
	
}



function bin_data () {

	var totalpixels=xpixels*ypixels;
	var gradient_node=document.getElementById("cg_a");
	var gradmax=gradient_node.getAttribute('gradient_max');
	var gradmin=gradient_node.getAttribute('gradient_min');
	var gradsteps=gradient_node.getAttribute('gradient_steps');
	var inv_grad=gradient_node.gradient_invert;
	
	if (gradient_node.hasAttribute('gradient_max_data')) {
		var gradmax=gradient_node.getAttribute('gradient_max_data');
	}
	if (gradient_node.hasAttribute('gradient_min_data')) {
		var gradmin=gradient_node.getAttribute('gradient_min_data');
	}

	var delta=gradmax-gradmin;

	var line=0;
	for (i=0; i<imgwidth*imgheight; i++) {
		backbuffer[i]=0;
	}
	xstep=xpix2img*size;
	ystep=ypix2img*size;
	ptr=-xstep; // whut?
	u=0;
	v=0;

	for (i=0; i<totalpixels; i++)	{	
		val=transposebuffer[i];

		indexval=~~((val-gradmin)/(delta)*gradsteps);  					
		if (indexval<0) indexval=0;
		if (indexval>=gradsteps) indexval=gradsteps-1;

		indexval=parseInt(indexval);
		hist[indexval]++;
		if ((inv_grad)  && (indexval!=0)) {			
				indexval=colormaplength-indexval;
		}

		ptr=(imgheight-v*ystep)*imgwidth; 
		ptr+=u*xstep;

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
}



/* draw_heatmap:
	- heatmap uitrekenen
	- minima/maxima bepalen
   - colormap tekenen; 
   - heatmap tekenen.

*/

var draw_heatmap=function draw_heatmap() {

	console.log("draw_heatmap:");
	calc_minmax();
	bin_data();
	draw_histogram();	

	/* eigenlijke heatmap plotten */

	var indexval=0;
	var color=[];
	var nr=0;

	var xstep=xpix2img*size;
	var ystep=ypix2img*size;

	var gradient_node=document.getElementById("cg_a");
	var gradsteps=gradient_node.getAttribute('gradient_steps');
	var colormapname=gradient_node.getAttribute('colormapname');
	colormap=gradient_node.colormaps[colormapname](gradsteps);

	console.log('draw_heatmap, colormap:',colormapname, gradsteps, colormap);

	console.log("draw_heatmap:",backbuffer.length);
	for (i=0,j=0; i<backbuffer.length; i++,j+=4) {
			indexval=backbuffer[i];
			if ((indexval>0) && (nr<-50)) {
						console.log(nr, i,j,indexval);
						nr+=1;
					}
			if ((indexval!=0) || (!skipzero)) {	  // waardes die 0 zijn niet plotten
				color=colormap[indexval];			
	    		mapdata[j] =  color[0];  
	    		mapdata[j+1] = color[1];  
	    		mapdata[j+2] = color[2];  
	    		mapdata[j+3] = 0xff; 
			} else {
				mapdata[j] =  0xff;   // background color: white
	    		mapdata[j+1] = 0xff; 
	    		mapdata[j+2] = 0xff; 
	    		mapdata[j+3] = 0xff; 
	    	}

		}	
	if (opties['plot_mean']==true){
		console.log('plot_mean:',xstep,xpix2img, ystep, ypix2img);
		color=opties['plot_mean_color'];
		for (i=0; i<mean_x.length; i++) {
			avgval=mean_x[i];
			ptr=(i*xpix2img+imgwidth*(imgheight-ypix2img*avgval))*4;
			mapdata[ptr]=color[0];
			mapdata[ptr+1]=color[1];
			mapdata[ptr+2]=color[2];
			mapdata[ptr+3]=color[3];
		}
	}
	if (opties['plot_median']==true){
		color=opties['plot_median_color'];
		for (i=0; i<median_x.length; i++) {
			medval=median_x[i];
			ptr=(i*xstep+ystep*imgwidth*(imgheight-medval))*4;			
			mapdata[ptr]=color[0];
			mapdata[ptr+1]=color[1];
			mapdata[ptr+2]=color[2];
			mapdata[ptr+3]=color[3];
		}
	}

	if (opties['info_datafile']!=null){
		color=opties['info_color'];
		for (i=0; i<extradata.length; i++) {
			i=extradata[i][0];
			j=i=extradata[i][1];
			ptr=(i*size+size*imgwidth*(imgheight-j))*4;
			mapdata[ptr]=color[0];
			mapdata[ptr+1]=color[1];
			mapdata[ptr+2]=color[2];
			mapdata[ptr+3]=color[3];
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



function init_print() {
   $('.print').on('click',click_print);
   $('.print').on('mouseenter ',enter_selectie);
   $('.print').on('mouseout ',leave_selectie);
}


function print_ok () {
	console.log("print ok");
}

function print_fail () {
	console.log('print failed');
	s='\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'
	s+="Printen niet gelukt. Opties voor command-line-reproductie:\n\n";
	s+='import contour\n\n'
	s+='args=dict(\n\t'
	var firstkey=true;
	opties['default_colormap']=colormapname;
	opties['default_size']=size;
	opties['default_transform']=transform;
	opties['gradmin']=gradmin;
	opties['gradmax']=gradmax;
	opties['gradsteps']=gradsteps;

	console.log('transform=',transform);

	var optiekeys=[];
	for (key in opties) {		
    	if (opties.hasOwnProperty(key)) {
    		optiekeys.push(key);
    	}
    }
    optiekeys.sort();

    delete opties['datamin'];
    delete opties['datamax'];
    delete opties['xmax'];
    delete opties['xmin'];
    delete opties['ymax'];
    delete opties['ymin'];


    for (var i=0; i<optiekeys.length; i++) {
    		key=optiekeys[i];
    		if (!(firstkey)) {
    			s+=',\n\t';
    		}
			val=opties[key];
			console.log(key,val, typeof(val));
			if (typeof(val)=='number')  {
    			s+=key+'='+val;
    		}
    		if (typeof(val)=='boolean') {
    			if (val==true) {
    				s+=key+'=True'
    			}
	   			if (val==false) {
    				s+=key+'=False'
    			}

    		}
			if (typeof(val)=='string') {
				s+=key+'="'+val+'"';	
			}
    		firstkey=false;    	
    }
    s+=')\nc=contour.contour()\nc.run_contour(args)\n';

    $('#printcode').html(s);	
}

function click_print () {


	var printtype=$(this).attr('data-print');
	//$.get('#',{'cmd':printtype})
 	$.ajax({
            cache: false,
            url: "/"+printtype,
            type: "GET"
            
        })
 		.done(print_ok)
 		.fail(print_fail);

}

  function draw_axes () {

  if (logx) var xScale=d3.scale.log();
  else	var xScale=d3.scale.linear();
  if (logy) var yScale=d3.scale.log();
  else	var yScale=d3.scale.linear();
    
  
  if ((logx) && (xmin<=0)) xmin=1;
  xScale.domain([xmin,xmax]);  
  xScale.range([0,imgwidth]); 

  if ((logy) && (ymin<=0)) ymin=1;
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
        .attr("transform","translate(75,"+(imgheight+25)+")")
        .call(xAxis);
  chart.append("g")
        .attr("class","yaxis")
        .attr("transform","translate(75,25)")
        .call(yAxis);        

  chart.append("text")      // text label for the x axis
  		.attr("class","xaxis")
        .attr("x", imgwidth/2+70 )
        .attr("y",  imgheight+70 )
        .style("text-anchor", "middle")
        .attr("font-family", "Corbel")
  		.attr("font-size", "16px")
  		.attr("font-weight", "bold")
        .text(xlabel);
  chart.append("text")      // text label for the x axis
    	.attr("class","yaxis")
        .attr("x", 0 )
        .attr("y", 0)
        .attr("font-family", "Corbel")
  		.attr("font-size", "16px")
  		.attr("font-weight", "bold")        
        .attr("transform","translate(20,"+(imgheight/2)+")rotate(270)")
        .style("text-anchor", "middle")
        .text(ylabel);
  chart.append("text")      // text label for the x axis
    	.attr("class","yaxis")
        .attr("x", imgwidth/2+70 )
        .attr("y", 15)
        .attr("font-family", "Corbel")
  		.attr("font-size", "16px")
  		.attr("font-weight", "bold")         
        .style("text-anchor", "middle")
        .text(title);

}



function draw_histogram () {

console.log("draw_histogram:", histmax);
//console.log(colormap);

histwidth=500;
histheight=0.4*imgheight;
barwidth=500/gradsteps;

var hist_offset_x=125;

var gradient_node=document.getElementById("cg_a");
console.log(gradient_node);
var gradsteps=gradient_node.getAttribute('gradient_steps');
var colormapname=gradient_node.getAttribute('colormapname');
console.log('draw_histogram, colormap:',colormapname, gradsteps);
colormap=gradient_node.colormaps[colormapname](gradsteps);

return;

$('.hist_2d').remove();
$('.hist_x').remove();
$('.hist_y').remove();
for (i=1; i<gradsteps; i++) {
 	color=colormap[i];
 	colorstring="rgb("+color[0]+","+color[1]+","+color[2]+")";
 	if (gradsteps>30) {
 		borderstyle=colorstring;
 	} else {
 		borderstyle="#5a5a5a";
 	}
 	//console.log(hist[i],histmax,imgheight-(hist[i]/histmax)*0.4*imgheight); 	
 	chart.append("rect")
		.attr("class","hist_2d")
		.attr("x",imgwidth+hist_offset_x+i*barwidth)
		.attr("y",imgheight-(hist[i]/histmax)*histheight+25)
		.attr("width",barwidth)
		.attr("height",(hist[i]/histmax)*histheight)
		.style("fill",colorstring)	
		.style("stroke",borderstyle)
		.style("stroke-width","1px");		
 }

  
  console.log('hist:',transform);
  var heatmap_hist_xScale=d3.scale.linear();
  
  heatmap_hist_xScale.range([0,gradsteps*barwidth]);
  heatmap_hist_xScale.domain([tgradmin,tgradmax]);

  var heatmap_hist_yScale=d3.scale.linear();
  heatmap_hist_yScale.range([0,histheight]);
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
  offsetx=imgwidth+hist_offset_x;
  offsety=imgheight+25;

  chart.append("g")
        .attr("class","xaxis hist_2d")
        .attr("transform","translate("+offsetx+","+offsety+")")
        .call(heatmap_hist_xAxis); 
  offsety=imgheight-histheight+25;
  chart.append("g")
        .attr("class","yaxis hist_2d")
        .attr("transform","translate("+offsetx+","+offsety+")")
        .call(heatmap_hist_yAxis); 

        /*
        .attr("class","yaxis hist_2d")
        .attr("transform","translate("+offsetx+","+offsety+")")
        .call(heatmap_hist_yAxis);*/

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
		return false;
	}
	
	$('.hist_2d').remove();
	$('.hist_x').remove();
	$('.hist_y').remove();
	$('.pointinfotext').remove();	

	var offsetx_hist=100;  //distance between heatmap and side-histograms
	var offsety_hist=25;   // distance between bottom of screen & side-histograms
	var offsetspace_hist=-40;   // distance between side-histograms
	var graphheight=0.25*imgheight;
	delta=(xmax-xmin);
	val=(x/imgwidth)*delta+xmin;
	xval=val.toFixed(2);

	/* text upper right corner */
 	chart.append("text")      
    	.attr("class","pointinfotext")
        .attr("x", 1.5*imgwidth+100 )
        .attr("y", 50 )
        .attr("font-family", "Corbel")
        .text(xlabel+':'+xval);
		
	delta=(ymax-ymin);
	val=((imgheight-y)/imgheight)*delta+ymin;
	yval=val.toFixed(0);
	chart.append("text")      
    	.attr("class","pointinfotext")
        .attr("x", 1.5*imgwidth+100 )
        .attr("y", 50+16)
         .attr("font-family", "Corbel")
     
        .text(ylabel+':'+yval);

	val=transposebuffer[(imgheight-y)/size*imgwidth+x/size];
	chart.append("text")      
    	.attr("class","pointinfotext")
        .attr("x", 1.5*imgwidth+100 )
        .attr("y", 50+32)
         .attr("font-family", "Corbel")
     
        .text('#count:'+val);

/* histogram y */

	histy_max=0;
	for (i=0; i<imgwidth; i++) { 		
		val=backbuffer[y*imgheight+i];
		if (val>histy_max) histy_max=val;
	}

	//console.log(histy_max);
	
	for (i=0; i<imgwidth; i++) { 	
	 	val=backbuffer[y*imgheight+i];	 		 	

	 	color=colormap[val];
		chart.append("rect")
			.attr("class","hist_y")
			.attr("x",imgwidth+offsetx_hist+i)
			.attr("y",parseInt(imgheight-(val/histy_max)*graphheight)+offsety_hist)
			.attr("width",1)
			.attr("height",(val/histy_max)*graphheight)
			.style("fill","rgb(8,8,0)")
			.style("stroke","rgb(8,8,0)")			
			//.style("fill","rgb("+color[0]+","+color[1]+","+color[2]+")")
			//.style("stroke","rgb("+color[0]+","+color[1]+","+color[2]+")")
			.style("stroke-width","1px");
		 }

		
histx_max=0;
for (i=0; i<imgheight; i++) { 	
	 	val=backbuffer[i*imgwidth+x];
	 	if (val>histx_max) histx_max=val;
	 }
	
for (i=0; i<imgheight; i++) { 	
	 	val=backbuffer[i*imgwidth+x];
	 	color=colormap[val];
		chart.append("rect")
			.attr("class","hist_y")
			.attr("x",2*imgwidth+offsetx_hist-i)
			.attr("y",imgheight-(val/histx_max)*graphheight-graphheight+offsety_hist+offsetspace_hist)
			.attr("width",1)
			.attr("height",(val/histx_max)*graphheight)
			.style("fill","rgb(130,8,8)")
			.style("stroke","rgb(130,8,8)")
			
			//.style("fill","rgb("+color[0]+","+color[1]+","+color[2]+")")
			//.style("stroke","rgb("+color[0]+","+color[1]+","+color[2]+")")
			.style("stroke-width","1px");
		 }

  

  var xxScale=d3.scale.linear();
  var yxScale=d3.scale.linear();
  var xyScale=d3.scale.linear();
  var yyScale=d3.scale.linear();
  
  xxScale.range([0,imgwidth]); 
  xxScale.domain([ymin,ymax]);       // bug: what's called 'xscale'/'yscale' is on the wrong position
  xyScale.range([0,0.25*imgheight]); 
  xyScale.domain([histy_max*(tgradmax/gradsteps),0]);       // bug: what's called 'xscale'/'yscale' is on the wrong position

  yxScale.range([0,imgwidth]); 
  yxScale.domain([xmin,xmax]);   
  yyScale.range([0,0.25*imgheight]); 
  yyScale.domain([histx_max*(tgradmax/gradsteps),0]);

  var xxAxis=d3.svg.axis();
  var xyAxis=d3.svg.axis();  
  var yxAxis=d3.svg.axis();
  var yyAxis=d3.svg.axis();  
  
  xxAxis.scale(xxScale)       
       .orient("bottom");
  xyAxis.scale(xyScale)       
       .orient("left");
  yxAxis.scale(yxScale)       
       .orient("bottom");
  yyAxis.scale(yyScale)       
       .orient("left");
  
  //console.log(chart);
  offsetx=imgwidth+offsetx_hist;
  offsetyx=imgheight+offsety_hist
  offsetyy=imgheight-2*graphheight+offsety_hist+offsetspace_hist;

  chart.append("g")
        .attr("class","yaxis hist_x")
        .attr("transform","translate("+offsetx+","+offsetyx+")")
        .call(yxAxis);
  chart.append("g")
        .attr("class","yaxis hist_x")
        .attr("transform","translate("+offsetx+","+offsetyy+")")
        .call(yyAxis);

  offsetx=imgwidth+offsetx_hist;
  offsetyx=imgheight-graphheight+offsety_hist+offsetspace_hist;
  offsetyy=imgheight-graphheight+offsety_hist;

  chart.append("g")
        .attr("class","xaxis hist_y")
        .attr("transform","translate("+offsetx+","+offsetyx+")")        
        .call(xxAxis);        
  chart.append("g")
        .attr("class","xaxis hist_y")
        .attr("transform","translate("+offsetx+","+offsetyy+")")        
        .call(xyAxis);        


  chart.append("text")      // text label for the x axis
  		.attr("class","xaxis hist_x")
        .attr("x",  1.5*imgwidth+offsetx_hist )
        .attr("y",  imgheight+offsety_hist+35 )
        .style("text-anchor", "middle")
        .attr("font-family", "Corbel")
  		.attr("font-size", "16px")
  		.attr("font-weight", "bold")
        .text(xlabel+ '(voor '+ylabel+'='+yval+')');
  chart.append("text")      // text label for the x axis
    	.attr("class","yaxis hist_y")
        .attr("x", 1.5*imgwidth+offsetx_hist )
        .attr("y", imgheight-graphheight+offsety_hist-offsetspace_hist-45 )
        .attr("font-family", "Corbel")
  		.attr("font-size", "16px")
  		.attr("font-weight", "bold")                
        .style("text-anchor", "middle")
        .text(ylabel+ '(voor '+xlabel+'='+xval+')');
	

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


function click_stats () {

	var id=$(this).attr('id');
	var f=$(this).attr('data-stats');
	var state=opties[f];
	if (state==true)	{
		state=false;
		$(this).removeClass('active_selectie');		
	} 
	else {
		state=true;
		$(this).addClass('active_selectie');	
	}
	opties[f]=state;
	console.log(opties);
	draw_heatmap();

}




function init_stats(widget_id, transform) {

 	$('.stats').on('click',click_stats);
 	$('.stats').on('mouseenter ',enter_selectie);
  	$('.stats').on('mouseout ',leave_selectie);  	

  	$('.stats').each(function(i,obj){
  		var f=$(this).attr('data-stats');
  		opties[f]=false;
  	});
}
