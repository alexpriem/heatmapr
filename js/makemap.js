
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

 
    var url=window.location.href;
    var data=url.split('/');    
    var dataset=data[4];
    
    data={'cmd':'makemap'};	
    for (var key in defaults) {
    	 if(defaults.hasOwnProperty(key)){
    	 	val=$('#'+key).val();
    	 	if (val!=undefined) {
    	 		data[key]=val
    	 	} else {
    	 		data[key]=defaults[key];
    	 	}
    	 }
    }
    console.log(data);
	$.ajax({url:"/makemap/"+dataset+'/', 
			type: "POST",
			'data':data,
			success: handle_ajax,
			error: handle_ajax_error,
		});


    url='/heatmap/'+dataset+'/'+data['x_var']+'/'+data['y_var'];
    $('#result').attr('href', url)


}


function init_page() {

    $('.combobox').combobox();    
    $('#makemap').on('click',makemap);

    for (var key in defaults) {
    	 if(defaults.hasOwnProperty(key)){
    	 	$('#'+key).val(defaults[key]);
    	 }
    }
}



$( document ).ready(init_page);