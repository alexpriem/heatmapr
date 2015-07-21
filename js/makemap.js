
var handle_ajax_error=function (result) {

	$('#errorbox').html('<code>' +result.status+ ' ' + result.statusText + ' <pre>'+result.responseText+"</pre>")
	$('#heatmap_div').hide();
}



var handle_ajax=function (result) {


	console.log('handle_ajax');
	r=JSON.parse(result);

	console.log(r);
}




function makemap () {

 
 	var dataset='best2010';
 	data={};
 	data.x_var=$("#combo_x").val();
 	data.y_var=$("#combo_y").val();
	$.ajax({url:"/makemap/"+dataset+'/', 
			type: "POST",
			'data':data,
			success: handle_ajax,
			error: handle_ajax_error,
		});


}


function init_page() {

    $('#combo_x').combobox();
    $('#combo_y').combobox();
    $('#makemap').on('click',makemap);
}



$( document ).ready(init_page);