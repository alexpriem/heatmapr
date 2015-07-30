
var width=500;
var height=500;

var hist_handle_ajax_error=function (result) {

	$('#errorbox').html('<code>' +result.status+ ' ' + result.statusText + ' <pre>'+result.responseText+"</pre>")
	$('#heatmap_div').hide();
}



var hist_handle_ajax=function (result) {

	//console.log('handle_ajax', result);
	r=JSON.parse(result);

	if (r.action=='makeplot') {
		init_histogram(r.data);
		return;
	}
}


function plot_single_histogram (chart, histogram){

	console.log('plot_single_histogram',histogram);

	plotwidth=0.8*width
	plotheight=0.7*height
	data=histogram.data;
	delta=height-plotheight;
	yoffset=0.1*height
	xoffset=0.2*height
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

	console.log (histogram.colname, data.length, histogram.datatype, histogram.minx, histogram.maxx, histogram.miny, histogram.maxy, histogram.miny=='',histogram.maxy==''); 
	if ((histogram.miny==='') || (histogram.maxy==='')) return;
	
	console.log (histogram.colname, data.length, histogram.datatype, histogram.miny, histogram.maxy); 

	xScale=d3.scale.linear();
  	xScale.domain([histogram.minx,histogram.maxx]);
  	xScale.range([xoffset,width]);

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
	yScale=d3.scale.linear();
  	yScale.domain([maxy,histogram.miny]);	  	
    yScale.range([0,plotheight+2*yoffset]);

    var xAxis=d3.svg.axis();
  	var yAxis=d3.svg.axis();	
  	xAxis.scale(xScale)
  		.ticks(numticks)	  		
        .orient("bottom");
    xAxis.tickFormat(d3.format("s"));
  	yAxis.scale(yScale)
  		.ticks(numticks)	  		
        .orient("left");
    yAxis.tickFormat(d3.format("s"));


	chart.append("g")
        .attr("class","xaxis mainx")
        .attr("transform","translate("+(xoffset)+","+(height-yoffset)+")")
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


	style='filled';
                      

	if (histogram.num_keys<14){
		colormap=colormap_qualitative(histogram.num_keys);		
		for (i=0; i<data.length; i++) {
				x=data[i][0];
				y=data[i][1];	
				var color=colormap[i];	
				var colortxt='rgb('+color[0]+','+color[1]+','+color[2]+')';
				var	val=y/maxy*height;
				console.log(colormap[i]);
				chart.append("rect")	
						.attr("class","hist")
						.attr("x",i*bin_width+xoffset)
						.attr("y",plotheight-val+delta-yoffset)
						.attr("width",bin_width)
						.attr("height",val)
						.style("fill",colortxt)
						.style("stroke","rgb(8,8,0)")
						//.style("fill","rgb("+color[0]+","+color[1]+","+color[2]+")")
						//.style("stroke","rgb("+color[0]+","+color[1]+","+color[2]+")")
						.style("stroke-width","1px");				
			}
		return;
	}
	data.push(data[0]);
	if (style=='filled') {
		var linefunction=d3.svg.line()
                      .x(function(d) { console.log(d[0], xScale(d[0])); return xScale(d[0]); })
                      .y(function(d) { return yScale(d[1]); })
					  .interpolate('step-after');

		var lineGraph = chart.append("path")
                            .attr("d", linefunction(data))
                            .attr("stroke", "blue")
	                        .attr("stroke-width", 2)
                            .attr("fill", "blue");
         }
	if (style=='line') {
		var linefunction=d3.svg.line()
                      .x(function(d) { console.log(d[0], xScale(d[0])); return xScale(d[0]); })
                      .y(function(d) { return yScale(d[1]); });
					  
		var lineGraph = chart.append("path")
                            .attr("d", linefunction(data))
                            .attr("stroke", "blue")
	                        .attr("stroke-width", 2);
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

	data={cmd:'resize',minx:min_x, maxx:max_x, miny:min_y, maxy:max_y};
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
		resize();
	}
}



function init_histogram (histogram) {


	console.log(histogram);
	$('.range').on('keyup',checkresize);
	data_div=document.getElementById('histogram_container');
    s='';
        
	s+='<svg class="chart" id="chart_0" data-dataset="'+histogram.colname+'"></svg>\n';
	
	data_div.innerHTML =s;
	
	var chart = d3.select("#chart_0")
					.attr("width", width)
					.attr("height", height);	
	svg=plot_single_histogram(chart, histogram);
}