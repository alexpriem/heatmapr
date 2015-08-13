// https://developer.mozilla.org/en-US/docs/Web/API/FileReader#readAsDataURL%28%29




function init_page() {
 

	var url=window.location.href;
	var data=url.split('/');	
	var dataset=data[4];
	console.log('init_page:',dataset);
	
/*	data={cmd:'reset'};
 	$.ajax({url:"/histogram/"+dataset+"/"+variabele, 
			type: "GET",
			'data':data,
			success: hist_handle_ajax,
			error: hist_handle_ajax_error,
		});
  */

  //$('#log').on('click',toggle_log);
  
}

$( document ).ready(init_page);