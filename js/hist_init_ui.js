// https://developer.mozilla.org/en-US/docs/Web/API/FileReader#readAsDataURL%28%29




function init_page() {
 

	var url=window.location.href;
	var data=url.split('/');	
	var dataset=data[4];
	var variabele=data[5];
	console.log('init_page:',dataset,variabele);


	init_histogram(histogram);
/*	data={cmd:'reset'};
 	$.ajax({url:"/histogram/"+dataset+"/"+variabele, 
			type: "GET",
			'data':data,
			success: hist_handle_ajax,
			error: hist_handle_ajax_error,
		});
  */

}

$( document ).ready(init_page);