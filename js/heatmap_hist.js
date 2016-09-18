var width=500;
var height=500;
var log=false;
var style='filled';

var current_histogram=null;





hist_handle_ajax_error=function (result) {

		console.log("hist: ajax error");
		$('#errorbox').html(result.status+ ' ' + result.statusText +result.responseText);
		$('#heatmap_div').hide();
}


hist_handle_ajax=function (result) {

console.log("hist: hist_handle_ajax");
r=JSON.parse(result);
console.log (r);
init_histogram (r);

console.log("histo klaar");
}




function init_histogram (histogram) {

	current_histogram=histogram;
	//console.log(histogram);	
	data_div=document.getElementById('histogram_container');
    s='';
        
	s+='<svg class="chart" id="chart_0" data-dataset="'+histogram.colname+'"></svg>\n';
	
	data_div.innerHTML =s;

	var extrawidth=0;
	if ('stringdata' in histogram)	{
		extrawidth=histogram.stringdata.length*50+75;
		extrawidth=0;
	}
	var chart = d3.select("#chart_0")
					.attr("width", width+extrawidth)
					.attr("height", height+200);	
	//svg=plot_histograms(chart, [histogram, histogram]);
	//svg=plot_histograms(chart, [histogram, histogram, histogram]);
	svg=plot_histograms(chart, [histogram, histogram, histogram, histogram]);

	//$('#chart_0').on('click',click_histogram);
}











function plot_histograms (chart, histograms){

	histogram_info=histograms[0];   // 1e histogram is bepalend voor de rest wbt settings
	
	console.log ('plot_histograms',histograms.length);

	for (var i=0; i<histograms.length; i++) {
		plot_histogram (chart, histograms.length, i, histogram_info, histograms[i]);
	}
}


function plot_histogram (chart, num_histograms, nr, histogram_info, histogram) {


	console.log('plot_histogram:',nr);

	if ('stringdata' in histogram)  {
		stringdata=histogram.stringdata;
	} else {
		stringdata=[[]];
	}


	num_keys=histogram.num_keys;
	plotwidth=0.8*width
	plotheight=0.7*height
	delta=height-plotheight;
	yoffset=50;
	xoffset=50;
	yaxiswidth=50;
	bins=data.length;
	if (bins>500) bins=500;
	bin_width= ((plotwidth/num_histograms)*0.8)/histogram.num_keys;
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




  	maxy=histogram.maxy;
  	var extrascale='';
  	if(histogram.maxy>10*histogram.maxy2) {
  		maxy=histogram.maxy2;  		
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
    yScale.range([0,height-yoffset]);   // 14: +2 voor borders

  

	         
  	var yAxis=d3.svg.axis();
  	
  	yAxis.scale(yScale)
  		.ticks(numticks)	  		
        .orient("left");
    yAxis.tickFormat(d3.format("s"));


	chart.append("g")
        .attr("class","yaxis mainy")
        .attr("transform","translate("+(xoffset)+",0)")
        .attr('font-size','12px')
        .call(yAxis);


    var title='';
    if (title in histogram) {
     	title=histogram.title;
  	    if (title.length>40) {
	    	title=title.slice(0,40);
		}
    }

  	chart.append("text")      // text label for the x axis
	    	.attr("class","yaxis")
	        .attr("x", width/2+70 )
	        .attr("y", 15)
	        .attr("font-family", "Corbel")
	  		.attr("font-size", fontsize+"px")
	  		.attr("font-weight", "bold")
	        .style("text-anchor", "middle")
	        .text(title);


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

		var startpos=yaxiswidth;			
		xScale2.range([yaxiswidth, width-25]);
		graphwidth=(width-25)-yaxiswidth;
	  	xScale2.domain([0,graphwidth]);

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

		// a1b1c1d1  a2b2c2d2 
		/*
		for (i=0; i<stringdata.length; i++){
				x=stringdata[i][0];
				y=stringdata[i][1];

				var color=colormap[i];	
				var colortxt='rgb('+color[0]+','+color[1]+','+color[2]+')';

				chart.append("rect")	
					.attr("class","hist")
					.attr("x",startpos+nr*(plotwidth/num_histograms)+i*bin_width)
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
	        				*/



		for (var i=0; i<stringdata.length; i++){
				x=stringdata[i][0];
				y=stringdata[i][1];

				var color=colormap[i];	
				var colortxt='rgb('+color[0]+','+color[1]+','+color[2]+')';

				
				chart.append("rect")	
					.attr("class","hist")
					.attr("x",startpos+i*(plotwidth/num_keys)+nr*bin_width )
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
	        /*
	        	var y=height-50;

	        	chart.append("line")
	        				.attr("x1", x+25)
                          	.attr("y1", y)
                         	.attr("x2", x+25)
                         	.attr("y2", y+5)
                         	.attr("stroke-width", 1)
                         	.attr("stroke", "black"); */


				}

		}

}





function heatmap_histogram (this_chart) {


	console.log('heatmap_histogram:',this_chart);
	this.datasets=[];

	var source   = $("#histogram-template").html();        
    var histogram_controls_template = Handlebars.compile(source); 

    context={vars:[{varname:'AR1'},{'varname':'AR2'}]};
    txt=histogram_controls_template(context);


    this_chart.append('foreignObject')
		    .attr("width", 600)
		    .attr("height", 250)
		    .attr('x',700)
		    .attr('y',0)
		    .attr("class",'histogram2')
		    .attr("id",'histogram2')
   	        .append("xhtml:body")		       	        
    		.html(txt);

    $('.sel_combobox').combobox()
    $('#histogram_add').on('click', add_histogram);
	return this;
}




function click_histogram_add () {


 console.log('add_histogram');

	var url=window.location.href;
	var data=url.split('/');	
	var dataset=data[4];
	var x_var=data[5];
	var y_var=data[6];

	query=$(this).attr('data-query');
	console.log('data-query:',query);

	if (query=='tot') {
		data=[[]];
	}
	if (query=='null_x') {
		data=[{'var':x_var,'comp':'=', 'val':'null'}];		
	}
	if (query=='null_y') {
		data=[{'var':y_var,'comp':'=', 'val':'null'}];	
	}

	if (query=='tot_min_null_x') {
		data=[{'var':x_var,'comp':'!=', 'val':'null'}];		
	}
	if (query=='tot_min_null_y') {
		data=[{'var':y_var,'comp':'!=', 'val':'null'}];	
	}

	if (query=='null_xy') {
		data=[{'var':x_var,'comp':'=', 'val':'null'},
			  {'var':y_var,'comp':'=', 'val':'null'}];
	}
	if (query=='area') {
		xmin=$(this).attr('data-xmin');
		xmax=$(this).attr('data-xmax');
		ymin=$(this).attr('data-ymin');
		ymax=$(this).attr('data-ymax');
		data=[	{'var':x_var,'comp':'>', 'val':xmin},
				{'var':x_var,'comp':'<', 'val':xmax},
				{'var':y_var,'comp':'>', 'val':ymin},
				{'var':y_var,'comp':'<', 'val':ymax}];
	}
	if (query=='x_area') {
		xmin=$(this).attr('data-min');
		xmax=$(this).attr('data-max');
		data=[{'var':x_var,'comp':'>', 'val':xmin},
				{'var':x_var,'comp':'<', 'val':xmax}];
	}

	if (query=='y_area') {
		ymin=$(this).attr('data-min');
		ymax=$(this).attr('data-max');
		data=[	{'var':y_var,'comp':'>', 'val':ymin},
				{'var':y_var,'comp':'<', 'val':ymax}];
	}


	
	min_x=$('#hist_minx').val();
	max_x=$('#hist_maxx').val();
	min_y=$('#hist_miny').val();
	max_y=$('#hist_maxy').val();
	num_bins=$('#hist_bins').val();
	varname=$('#hist_var').html();

    console.log('data:',data);
	$.ajax({url:"/heatmap_histogram/"+dataset+'/', 
			type: "POST",
			'data':{'cmd':data,'var':varname, minx:min_x, maxx:max_x, miny:min_y, maxy:max_y,bins:num_bins, num_cmds:data.length},
			success: hist_handle_ajax,
			error: hist_handle_ajax_error,
	});

}