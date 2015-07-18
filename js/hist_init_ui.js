// https://developer.mozilla.org/en-US/docs/Web/API/FileReader#readAsDataURL%28%29




function init_page() {
 


	var dataset="best2010";
	var variabele="AR26";

	data={cmd:'init'};
 	$.ajax({url:"/histogram/"+dataset+"/"+variabele, 
			type: "GET",
			'data':data,
			success: hist_handle_ajax,
			error: hist_handle_ajax_error,
		});
  //init_histogram(); 

}

$( document ).ready(init_page);