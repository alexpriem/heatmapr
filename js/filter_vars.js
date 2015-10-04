
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