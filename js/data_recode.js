
/* filter-button at top, for selecting rows in csv. Needs separate tab */


var recode_add_row=function() {

	rownr=$(this).attr("data-rownr");
	rvalues=$('.recodevalues');
	newrownr=rvalues.length;
	newrow=$('#recode_row_'+rownr).clone();
	console.log('add:',newrow.attr('id'))
	newrow.attr('id','recode_row_'+newrownr);
	$('#recode_row_'+rownr).after(newrow);
	return false;
}

var recode_del_row=function() {

	rownr=$(this).attr("data-rownr");
	console.log(rownr);
	
	rows=$('.recodevalues');
	if (rows.length>1) {
		$('#recode_row_'+rownr).remove();
	}  else {					// inputboxes niet verwijderen maar leeg maken.
		$(rows[0]).val('');			
		rows=$('.recodereplacements');
		$(rows[0]).val('');
	}
	return false;
}

var recode_undo_edit=function() {
	
	return false;
}

var recode_update=function() {
	
	console.log('filter_update');

	values=[];
	rvals=$('.recodevalues');
	rvals.each(function(index) { values.push($(this).val());   });
	replacements=[];
	freplacements=$('.recodereplacements');
	freplacements.each(function(index) { replacements.push($(this).val());   });
	

	data={'values':values,'replacements':replacements, 'datadir':datadir};

	console.log(data);
	$.ajax({url:"/set_recode/"+dataset+'/', 
			type: "POST",
			'data':data,
			success: handle_ajax,
			error: handle_ajax_error,
		});
	return false;
}





function show_recodeset(recodes){


	console.log(recodes);
	data_div=document.getElementById('data_container');    

	var source   = $("#recode-template").html();   				
    var template = Handlebars.compile(source);     
    
    if (recodes.length==0) {
    	recodes.push({'value':'','replacement':''})    
    }
    
    s=template({'rows':recodes});
	
	data_div.innerHTML =s;

	$('#update_recode').on('click',recode_update);
	$('#update_recode_edit').on('click',recode_undo_edit);
	$('.del').on('click',recode_del_row);
	$('.add').on('click',recode_add_row);
	
}



function init_page () {

		show_recodeset(defaults);
}


$( document ).ready(init_page);