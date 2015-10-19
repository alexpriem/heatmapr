


function histogram () {



}




hist_handle_ajax_error=function (result) {

		console.log("hist: ajax error");
		$('#errorbox').html(result.status+ ' ' + result.statusText +result.responseText);
		$('#heatmap_div').hide();
}

hist_handle_ajax=function (result) {

		console.log("histo klaar");
}




function add_histogram () {

	console.log('add_histogram');

	var url=window.location.href;
	var data=url.split('/');	
	var dataset=data[4];

    var varname=$('#histogram_var').val();
    var seltype=$('#histogram_part').val();
    var selval=$('#histogram_partvalue').val();
    var data={histogram_var:varname,
    		histogram_part:seltype, 
    		histogram_partvalue:selval};


    console.log(data);
	$.ajax({url:"/heatmap_histogram/"+dataset+'/', 
			type: "POST",
			'data':data,
			success: hist_handle_ajax,
			error: hist_handle_ajax_error,
	});


}



function heatmap_histogram (this_chart) {



	console.log('heatmap_histogram',this_chart);
	this.datasets=[];



	var source   = $("#histogram-template").html();        
    var histogram_controls_template = Handlebars.compile(source); 

    context={};
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

    $('#histogram_add').on('click', add_histogram);
	return this;
}