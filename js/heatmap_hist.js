


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


	if (query=='tot') {
		data=[[]];
	}
	if (query=='null_x') {
		data=[{'var':x_var,'comp':'=', 'val':'null'}];		
	}
	if (query=='null_y') {
		data=[{'var':y_var,'comp':'=', 'val':'null'}];	
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



    console.log(data);
	$.ajax({url:"/heatmap_histogram/"+dataset+'/', 
			type: "POST",
			'data':{'cmd':data},
			success: hist_handle_ajax,
			error: hist_handle_ajax_error,
	});

}