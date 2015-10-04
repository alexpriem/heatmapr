/* filter-button at top, for selecting rows in csv. Needs separate tab */


var filter_add_row=function() {

	rownr=$(this).attr("data-rownr");
	fcols=$('.filtercol');
	newrownr=fcols.length;
	newrow=$('#filter_row_'+rownr).clone();
	console.log('add:',newrow.attr('id'))
	newrow.attr('id','filter_row_'+newrownr);
	$('#filter_row_'+rownr).after(newrow);
	return false;
}

var filter_del_row=function() {

	rownr=$(this).attr("data-rownr");
	console.log(rownr);
	

	rows=$('.filtercol');
	if (rows.length>1) {
		$('#filter_row_'+rownr).remove();
	}  else {					// inputboxes niet verwijderen maar leeg maken.
		$(rows[0]).val('');			
		rows=$('.filtercomp');
		$(rows[0]).val('');
		rows=$('.filtervalue');
		$(rows[0]).val('');

	}
	return false;
}

var filter_undo_edit=function() {
	
	return false;
}

var filter_update=function() {
	
	console.log('filter_update');

	filtercols=[];
	fcols=$('.filtercol');
	fcols.each(function(index) { filtercols.push($(this).val());   });
	filtercomp=[];
	fcomp=$('.filtercomp');
	fcomp.each(function(index) { filtercomp.push($(this).val());   });
	filtervalues=[];
	fvalues=$('.filtervalue');
	fvalues.each(function(index) { filtervalues.push($(this).val());   });
	
	// rudimentary check on empty cols.
	filterlen=filtercols.length;
	for (i=0; i<filterlen;i++) {
		col=filtercols[i];
		if (col=='') {
			filterlen-=1;
			filtercols.splice(i,1);
			filtercomp.splice(i,1);
			filtervalues.splice(i,1);
		}
	}

	var url=window.location.href;
	var data=url.split('/');	
	var dataset=data[4];

	data={'filtercols':filtercols,'filtercompares':filtercomp,'filtervalues':filtervalues};

	console.log(data);
	$.ajax({url:"/set_filter/"+dataset+'/', 
			type: "POST",
			'data':data,
			success: handle_ajax,
			error: handle_ajax_error,
		});
	return false;
}





function show_filters(filters){

	var url=window.location.href;
	var data=url.split('/');	
	var dataset=data[4];

	data_div=document.getElementById('data_container');

	var source   = $("#filter-template").html();   				
    var template = Handlebars.compile(source); 
    console.log(filters);
    
  

    if ((filters.length)==0){
    	filters.push({'key':'','compare':'','value':''})    
    }
    s=template({'rows':filters});
	
	data_div.innerHTML =s;

	$('#update_filter').on('click',filter_update);
	$('#update_filteredit').on('click',filter_undo_edit);
	$('.del').on('click',filter_del_row);
	$('.add').on('click',filter_add_row);

  
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





function init_page () {

		show_filters(defaults);
}



$( document ).ready(init_page);