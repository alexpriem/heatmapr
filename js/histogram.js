
var width=500;
var height=500;

var hist_handle_ajax_error=function (result) {

	$('#errorbox').html('<code>' +result.status+ ' ' + result.statusText + ' <pre>'+result.responseText+"</pre>")
	$('#heatmap_div').hide();
}



var hist_handle_ajax=function (result) {

	console.log('handle_ajax', result);
	r=JSON.parse(result);

	if (r.action=='makeplot') {
		init_histogram(r);
		return;
	}
}


function plot_single_histogram (chart, col){


	plotwidth=0.8*width
	plotheight=0.7*height
	data=col.data;
	delta=height-plotheight;
	yoffset=0.1*height
	xoffset=0.2*height
	bins=data.length;
	if (bins>100) bins=100;
	bin_width= plotwidth/bins;
	console.log('bin_width:', bin_width, col.num_keys)
	if (bin_width>20) {
		bin_width=20;
	}
	
	maxy=col.maxy;
	fontsize=15;
	numticks=5;

	console.lo

	$('#minx').val(col.minx);
	$('#maxx').val(col.maxx);
	$('#miny').val(col.miny);
	$('#maxy').val(col.maxy);

	if ((col.miny=='') || (col.maxy=='')) return;
	
	console.log (col.colname, data.length, col.datatype, col.min, col.max); 

	for (var i=0; i<data.length; i++) {

		x=data[i][0];
		y=data[i][1];
		console.log(x,y);
		var	val=y/maxy*height;

		xScale=d3.scale.linear();
	  	xScale.domain([col.minx,col.maxx]);
	  	xScale.range([0,width]);

	  	maxy=col.maxy;
	  	var extrascale='';
	  	if(col.maxy>10*col.maxy2) {
	  		maxy=col.maxy2;
	  		extrascale='*';
	  		if(col.maxy2>10*col.maxy3) {
	  			maxy=col.maxy2;
	  			extrascale='**';
	  		}
	  	}
		yScale=d3.scale.linear();
	  	yScale.domain([maxy,col.miny]);	  	
	    yScale.range([yoffset,plotheight+yoffset]);

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


		//console.log('val:',x,y,val, height-val);
		chart.append("rect")	
				.attr("class","hist")
				.attr("x",i*bin_width+xoffset)
				.attr("y",plotheight-val+delta-yoffset)
				.attr("width",bin_width)
				.attr("height",val)
				.style("fill","rgb(8,8,0)")
				.style("stroke","rgb(8,8,0)")
				//.style("fill","rgb("+color[0]+","+color[1]+","+color[2]+")")
				//.style("stroke","rgb("+color[0]+","+color[1]+","+color[2]+")")
				.style("stroke-width","1px");				


	  chart.append("text")      // text label for the x axis
	    	.attr("class","yaxis")
	        .attr("x", width/2+70 )
	        .attr("y", 15)
	        .attr("font-family", "Corbel")
	  		.attr("font-size", fontsize+"px")
	  		.attr("font-weight", "bold")
	        .style("text-anchor", "middle")
	        .text(col.colname+extrascale);

		}	


}




function get_range(elem) {

 val=$('#'+elem).val();
 console.log('get_range:',elem,val);
 return val; 
}

function resize () {


	var dataset="best2010";
	var variabele="AR26";

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



function init_histogram (r) {


	$('.range').on('keyup',checkresize);
	data_div=document.getElementById('histogram_container');
    s='<h3>'+r.msg+'</h3>\n';
    histogram=r.data;
    console.log('histogram:',r,histogram);
	s+='<svg class="chart" id="chart_0" data-dataset="'+histogram.colname+'"></svg>\n';
	
	data_div.innerHTML =s;
	
	var chart = d3.select("#chart_0")
					.attr("width", width)
					.attr("height", height);
	console.log(histogram.colname);
	svg=plot_single_histogram(chart, histogram);
}