
var width=500;
var height=500;
var log=false;

var current_histogram=null;

var hist_handle_ajax_error=function (result) {

	$('#errorbox').html('<code>' +result.status+ ' ' + result.statusText + ' <pre>'+result.responseText+"</pre>")
	$('#heatmap_div').hide();
}




function safe_log  (val,log_min) {
		
	if (val>=0) {
		if ((val>=0) && (val<=log_min)) {
			return Math.log(log_min)/Math.LN10;   //null?
		}
		val=Math.log(val)/Math.LN10;
	} else {
		if ((val<=0) && (val>=-log_min)) {
			return -Math.log(log_min);
		}
		if (val<0) {
			val=-Math.log(-val)/Math.LN10;
		}
	}
	return val;
}




var hist_handle_ajax=function (result) {

	//console.log('handle_ajax', result);
	r=JSON.parse(result);

	if (r.action=='makeplot') {
		init_histogram(r.data);
		return;
	}
}




function click_log () {

	if (log==true) {
		log=false;
	} else {
		log=true;
	}	
	init_histogram(histogram);
}


function plot_single_histogram (chart, histogram){

	console.log('plot_single_histogram',histogram);
	data=histogram.data;
	stringdata=histogram.stringdata;
	console.log('plot_single_histogram',histogram, data.length, stringdata.length);
	if ((data.length==0) && ((stringdata.length>20) || (stringdata.length==0))) {
		$('#single_value').text ("Teveel niet-numerieke data: "+histogram.num_keys+" unieke waardes.");
		$('#overview').hide();
		return
	}

	if (histogram.num_keys==1) {
		if (histogram.data.length==1) {
			keyval=histogram.data[0][0];
			num=histogram.data[0][1];
		} else {
			keyval=histogram.stringdata[0][0];
			num=histogram.stringdata[0][1];
		}
		if (!histogram.empty) {
			$('#single_value').text ("1 waarde ("+keyval+"):"+num+' records');
		} else {
			$('#single_value').text ("Lege variabele, "+num+' records');
		}
		$('#overview').hide();
		return
	}

	

	plotwidth=0.8*width
	plotheight=0.7*height
	delta=height-plotheight;
	yoffset=50;
	xoffset=50;
	bins=data.length;
	if (bins>100) bins=100;
	bin_width= plotwidth/bins;
	console.log('bin_width:', bin_width, histogram.num_keys)
	if (bin_width>20) {
		bin_width=20;
	}
	
	maxy=histogram.maxy;
	fontsize=15;
	numticks=5;

	

	$('#minx').val(histogram.minx);
	$('#maxx').val(histogram.maxx);
	$('#miny').val(histogram.miny);
	$('#maxy').val(histogram.maxy);
	$('#bins').val(histogram.bins);

	console.log (histogram.colname, data.length, histogram.datatype, histogram.minx, histogram.maxx, histogram.miny, histogram.maxy, histogram.miny=='',histogram.maxy==''); 
	if ((histogram.miny==='') || (histogram.maxy==='')) return;
	
	console.log (histogram.colname, data.length, histogram.datatype, histogram.miny, histogram.maxy); 

	xScale=d3.scale.linear();	
	xScale.domain([histogram.minx,histogram.maxx]);

	if (data.length>1) {
  		xScale.range([xoffset,width-xoffset]);
  	} else {
  		xScale.range([xoffset,2*xoffset]);    // eigenlijk categorieindeling voor klein aantal keys
  	}


  	maxy=histogram.maxy;
  	var extrascale='';
  	if(histogram.maxy>10*histogram.maxy2) {
  		maxy=histogram.maxy2;
  		extrascale='*';
  		if(histogram.maxy2>10*histogram.maxy3) {
  			maxy=histogram.maxy2;
  			extrascale='**';
  		}
  	}
  	if (log==false) {
		yScale=d3.scale.linear();
	} else {
		yScale=d3.scale.log();
		if (histogram.miny==0) {
			histogram.miny=1;
		}
	} 

  	yScale.domain([maxy,histogram.miny]);	  	
    yScale.range([0,height-yoffset-15]);

  

	style='filled';
	style='line';
                      

	if (histogram.num_keys<14){				 // eigenlijk categorieindeling voor klein aantal keys
		xScale.domain([histogram.minx,histogram.maxx+0.5]);
		colormap=colormap_qualitative(histogram.num_keys);		
		for (i=0; i<data.length; i++) {
				x=data[i][0];
				y=data[i][1];	
				var color=colormap[i];	
				var colortxt='rgb('+color[0]+','+color[1]+','+color[2]+')';

				console.log(yScale(y), height,yoffset)								
				chart.append("rect")	
						.attr("class","hist")
						.attr("x",xScale(x))
						.attr("y",yScale(y)) //yScale(y))
						
						//.attr("x",i*bin_width+xoffset)
						//.attr("y",plotheight-val+delta-yoffset)
						.attr("width",bin_width)
						.attr("height",height-yScale(y)-yoffset)
						.style("fill",colortxt)
						.style("stroke","rgb(32,32,0)")						
						.style("stroke-width","1px");				
			}		
	}
	





	if ((style=='filled') && (histogram.num_keys>=14)) {
		if (bins>=100) {
			data.push(data[0]);
		}
		var linefunction=d3.svg.line()
                      .x(function(d) { console.log(d[0], d[1],xScale(d[0])); return xScale(d[0]); })
                      .y(function(d) { return yScale(d[1]); })                      					
					  .interpolate('step-after');

		var lineGraph = chart.append("path")
                            .attr("d", linefunction(data))
                            .attr("stroke", "blue")
	                        .attr("stroke-width", 2)
                            .attr("fill", "blue");
         }
	if ((style=='line') && (histogram.num_keys>=14)) {
		
		var linefunction=d3.svg.line()
                      .x(function(d) { console.log(d[0],d[1], xScale(d[0])); return xScale(d[0]); })
                      .y(function(d) { return yScale(d[1]); });
					  
		var lineGraph = chart.append("path")
                            .attr("d", linefunction(data))
                            .attr("fill",'none')
                            .attr("stroke", "blue")
	                        .attr("stroke-width", 2);
		}

  	var xAxis=d3.svg.axis();
  	var yAxis=d3.svg.axis();
  	if (data.length>1) {	
  		xAxis.scale(xScale)
  			.ticks(numticks)	  		
        	.orient("bottom");
	} else {
  		xAxis.scale(xScale)
  			.ticks(0)	  		
        	.orient("bottom");		
	}

    xAxis.tickFormat(d3.format("s"));
  	yAxis.scale(yScale)
  		.ticks(numticks)	  		
        .orient("left");
    yAxis.tickFormat(d3.format("s"));



	chart.append("g")
        .attr("class","xaxis mainx")
        .attr("transform","translate(0,"+(height-yoffset)+")")
        .attr('font-size','15px')
        .call(xAxis);

	chart.append("g")
        .attr("class","yaxis mainy")
        .attr("transform","translate("+(xoffset)+",0)")
        .attr('font-size','12px')
        .call(yAxis);

  	chart.append("text")      // text label for the x axis
	    	.attr("class","yaxis")
	        .attr("x", width/2+70 )
	        .attr("y", 15)
	        .attr("font-family", "Corbel")
	  		.attr("font-size", fontsize+"px")
	  		.attr("font-weight", "bold")
	        .style("text-anchor", "middle")
	        .text(histogram.colname+extrascale);


// missings/strings in histogram data

    if (stringdata.length>0) {
    	console.log('adding stringdata');    	
	  	xScale2=d3.scale.linear();	  		  	
	  	var range=[];
	  	var labels=[];
	  	var values=[];
	  	for (i=0; i<stringdata.length;i++) {
	  		range.push(i);
	  		var key=stringdata[i][0];
	  		values.push(stringdata[i][1]);	  		
	  		if (key in histogram.labels) {
	  			labels.push(histogram.labels[key]);
	  		} else {
	  			if (key=='') {
	  				key='(leeg)';
	  			}
	  			labels.push(key);
	  		}	  		
	  	}
	  	console.log(labels,range);
	  //	xScale2.domain(labels);
	  //	xScale2.domain(range);

		var startpos=width+xoffset;			
		if (data.length<=1) {
			startpos=3*xoffset;
		}
	  	xScale2.range([startpos,startpos+stringdata.length*50]);
	  	xScale2.domain([0,stringdata.length]);

    	var xAxis2=d3.svg.axis();
    	xAxis2.scale(xScale2)
  				.ticks(0)	  		
        		.orient("bottom");
		chart.append("g")
	        .attr("class","xaxis mainx")
	        .attr("transform","translate(0,"+(height-yoffset)+")")
	        .attr('font-size','15px')
	        .call(xAxis2);


		colormap=colormap_qualitative(stringdata.length);		
		for (i=0; i<stringdata.length; i++){
				x=stringdata[i][0];
				y=stringdata[i][1];

				var color=colormap[i];	
				var colortxt='rgb('+color[0]+','+color[1]+','+color[2]+')';

				chart.append("rect")	
					.attr("class","hist")
					.attr("x",startpos+i*50)
					.attr("y",yScale(y)) //yScale(y))
					
					//.attr("x",i*bin_width+xoffset)
					//.attr("y",plotheight-val+delta-yoffset)
					.attr("width",bin_width)
					.attr("height",height-yScale(y)-yoffset)
					.style("fill",colortxt)
					.style("stroke","rgb(32,32,0)")						
					.style("stroke-width","1px");
				var x=startpos+i*50-15;
				var y=height-20;
				chart.append("text")
					        .attr("x", 10)
					        .attr("y", 10)
	        				.attr("font-family", "Corbel")
	  						.attr("font-size", fontsize+"px")
	  						.attr("font-weight", "bold")
	        				.style("text-anchor", "middle")
	        				.text(labels[i])
	        				.attr("transform","translate("+(x)+","+(y)+")rotate(-45)")
	        	var y=height-50;
	        	chart.append("line")
	        				.attr("x1", x+25)
                          	.attr("y1", y)
                         	.attr("x2", x+25)
                         	.attr("y2", y+5)
                         	.attr("stroke-width", 1)
                         	.attr("stroke", "black");


				}

		}

}




function get_range(elem) {

 val=$('#'+elem).val();
 console.log('get_range:',elem,val);
 return val; 
}

function resize () {



	var url=window.location.href;

	var url=window.location.href;
	var data=url.split('/');	
	var dataset=data[4];
	var variabele=data[5];

	min_x=get_range('minx');
	max_x=get_range('maxx');
	min_y=get_range('miny');
	max_y=get_range('maxy');
	num_bins=get_range('bins');

	data={cmd:'resize',minx:min_x, maxx:max_x, miny:min_y, maxy:max_y,bins:num_bins};
	console.log('resize:', data);
 	$.ajax({url:"/histogram/"+dataset+"/"+variabele, 
			type: "GET",
			'data':data,

			success: hist_handle_ajax,
			error: hist_handle_ajax_error,
		});
  //init_histogram(); 



}


var checkresize=function (e) {

	if (e.keyCode==13) {
		console.log('resize');
		el=this.id;
		if ((el='miny') || (el=='maxy')) {
			var miny=$('#miny').val()
			var maxy=$('#maxy').val()
			histogram.miny=miny;
			histogram.maxy=maxy;			
			init_histogram(histogram);  
			//resize();
		} else {
			resize();
		}
	}
}



function init_histogram (histogram) {

	current_histogram=histogram;
	console.log(histogram);
	$('.xyinput').on('keyup',checkresize);
	data_div=document.getElementById('histogram_container');
    s='';
        
	s+='<svg class="chart" id="chart_0" data-dataset="'+histogram.colname+'"></svg>\n';
	
	data_div.innerHTML =s;

	var extrawidth=0;
	if ('stringdata' in histogram)	{
		extrawidth=histogram.stringdata.length*50+75;
	}
	var chart = d3.select("#chart_0")
					.attr("width", width+extrawidth)
					.attr("height", height);	
	svg=plot_single_histogram(chart, histogram);
}