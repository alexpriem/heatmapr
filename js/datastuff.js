

var filter={'empty':false,
			'single':false,
			'int':true,
			'float':true,
			'string':true};
			


var click_action=function () {

	console.log('click_action');	
	update_state(this.id);
}



var handle_ajax_error=function (result) {

	$('#errorbox').html(result.status+ ' ' + result.statusText +result.responseText);
	$('#heatmap_div').hide();
}


function update_state  (action) {
	
	var url=window.location.href;
	var data=url.split('/');	
	var dataset=data[4];

	var data={dataset:dataset, 'action':action};
  
	 for (var item in filter) {	 	
         if (filter.hasOwnProperty(item)) {
            var clicked=filter[item];
            if (clicked) {
            		data['filter_'+item]=true;
            	}
            else {data['filter_'+item]=false;}
         } //if clicked
     }  //for


	$.ajax({url:"/dataset/"+dataset, 
			type: "GET",
			'data':data,
			success: handle_ajax,
			error: handle_ajax_error,
		});
}




var click_filter=function () {

	console.log('click_filter', this.id.slice(7));	
	var filter_item=$('#'+this.id).data('filter');
	console.log('filter:',filter);

	var state=filter[filter_item];
	if (state) 
		{filter[filter_item]=false;
		$('#toggle_'+filter_item).addClass('btn-default').removeClass('btn-info');
		}
	else 
		{filter[filter_item]=true;
		$('#toggle_'+filter_item).addClass('btn-info').removeClass('btn-default');
		}


	update_state('init');
}


function update_filter() {

	console.log('update_filter');
	$('.data_filter').removeClass('btn-info');
	$('.data_filter').removeClass('btn-default');
	 for (var item in filter) {
	 	console.log('update_filter', item);
         if (filter.hasOwnProperty(item)) {
            var clicked=filter[item];
            if (clicked) { 
            	$('#filter_'+item).addClass('btn-info');
            } else {
            	$('#filter_'+item).addClass('btn-default');
            }
         } //if clicked
     }  //for
}










var handle_ajax=function (result) {


	console.log('handle_ajax');
	r=JSON.parse(result);

	if (r.action=='makeplot') {
		plot_histograms(r);
		return;
	}

	if (r.action=='filtersetup') {
		show_filters(r);
		return;
	}

	if (r.action=='recodesetup') {
		show_recodeset(r);
		return;
	}


	if (r.action=='info') {
		var source   = $("#info-template").html();   			
	} else {
    var source   = $("#datacols-template").html();        
	}
    var template = Handlebars.compile(source); 


  //  columns={cols:[{colname:'asdfasdf'},{colname:'asasdf'}]};
  	var columns={cols:r.columns,dataset:r.dataset};

  	//console.log(columns);
    data_div=document.getElementById('data_container');
    data_div.innerHTML ='<h3>'+r.dataset+'</h3>'+'<p>'+r.msg+'</p>'+template(columns);
        
	$("#infotable").tablesorter(); 

    $('.data_action').on("click",click_action);
    $('.data_filter').on("click",click_filter);
    update_filter();
	//console.log(result);


}



function plot_histogram (chart, col){


	height=200;
	width=200;
	plotwidth=0.8*width
	plotheight=0.7*height
	delta=height-plotheight;
	yoffset=0.1*height
	xoffset=0.2*height
	bins=col.num_keys;
	if (bins>100) bins=100;
	bin_width= plotwidth/bins;
	console.log('bin_width:', bin_width, col.num_keys)
	if (bin_width>20) {
		bin_width=20;
	}
	data=col.data;
	maxy=col.maxy;
	fontsize=15;
	numticks=5;

	if ((col.miny=='') || (col.maxy=='')) return;
	
	console.log (col.colname, data.length, col.datatype, col.min, col.max); 

	for (var i=0; i<data.length; i++) {

		x=data[i][0];
		y=data[i][1];
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


function plot_histograms(r) {

    width=200;
    height=200;
	
	data_div=document.getElementById('data_container');
    s='<h3>'+r.dataset+'</h3>'+'<p>'+r.msg+'</p>\n';

	columns=r.columns;
	for (var i=0; i<columns.length; i++) {
		col=columns[i];
		data=col.data;
		if (data.length!=0) {
			s+='<svg class="chart" id="chart_'+col.nr+'"data-dataset="'+col.colname+'"></svg>\n';
		}		
	}

	data_div.innerHTML =s;

	for (var i=0; i<columns.length; i++) {
		col=columns[i];
		data=col.data;
		console.log(col.colname, data.length);
		if (data.length!=0) {					
			console.log(col.colname);
			var chart = d3.select("#chart_"+col.nr)
    						.attr("width", width)
    						.attr("height", height);
    		console.log(col.colname);
    		svg=plot_histogram(chart, col);
		}	
	}


	html='';


}



function init_interactive (){

	

 	$(".nav-pills").on("click", "a", function(e){     

      tab=$(this).attr('id'); // tab_ts of tab_map
      console.log('tabchange:',this, tab);
      $(this).tab('show');    
      if (tab=='tab_heatmap') {
        $('#data_div').hide();
        $('#heatmap_div').show();
		$('.leftbox').show();
      } 
      if (tab=='tab_data') {        
        $('#data_div').show();
        $('#heatmap_div').hide();                        
        $('.leftbox').hide();
      } 
      e.preventDefault();      
    });

    $('#data_container').css('margin-left',0);        
    $('#data_container').css('top',50); 
    $('.leftbox').hide();

   
   update_state('init');
} 