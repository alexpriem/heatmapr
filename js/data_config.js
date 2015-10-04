/* config-button at top, for selecting rows in csv. Needs separate tab */


var config_add_row=function() {

	rownr=$(this).attr("data-rownr");
	fcols=$('.configcol');
	newrownr=fcols.length;
	newrow=$('#config_row_'+rownr).clone();
	console.log('add:',newrow.attr('id'))
	newrow.attr('id','config_row_'+newrownr);
	$('#config_row_'+rownr).after(newrow);
	return false;
}

var config_del_row=function() {

	rownr=$(this).attr("data-rownr");
	console.log(rownr);
	

	rows=$('.configcol');
	if (rows.length>1) {
		$('#config_row_'+rownr).remove();
	}  else {					// inputboxes niet verwijderen maar leeg maken.
		$(rows[0]).val('');			
		rows=$('.configcomp');
		$(rows[0]).val('');
		rows=$('.configvalue');
		$(rows[0]).val('');

	}
	return false;
}

var config_undo_edit=function() {
	
	return false;
}

var config_update=function() {
	
	console.log('config_update');

	configcols=[];
	fcols=$('.configcol');
	fcols.each(function(index) { configcols.push($(this).val());   });
	configcomp=[];
	fcomp=$('.configcomp');
	fcomp.each(function(index) { configcomp.push($(this).val());   });
	configvalues=[];
	fvalues=$('.configvalue');
	fvalues.each(function(index) { configvalues.push($(this).val());   });
	
	// rudimentary check on empty cols.
	configlen=configcols.length;
	for (i=0; i<configlen;i++) {
		col=configcols[i];
		if (col=='') {
			configlen-=1;
			configcols.splice(i,1);
			configcomp.splice(i,1);
			configvalues.splice(i,1);
		}
	}

	var url=window.location.href;
	var data=url.split('/');	
	var dataset=data[4];

	data={'configcols':configcols,'configcompares':configcomp,'configvalues':configvalues};

	console.log(data);
	$.ajax({url:"/set_config/"+dataset+'/', 
			type: "POST",
			'data':data,
			success: handle_ajax,
			error: handle_ajax_error,
		});
	return false;
}





function show_configs(config){

	var url=window.location.href;
	var data=url.split('/');	
	var dataset=data[4];

	data_div=document.getElementById('data_container');

	var source   = $("#config-template").html();   				
    var template = Handlebars.compile(source); 
    console.log(config);
    
  

    if ((config.length)==0){
    	config.push({'enabled':'','colname':'','typehine':'','format':''})    
    }
    s=template({'rows':config});
	
	data_div.innerHTML =s;

	$('#update_config').on('click',config_update);
	$('#update_configedit').on('click',config_undo_edit);
	$('.del').on('click',config_del_row);
	$('.add').on('click',config_add_row);

  
}




function update_state  (action) {
	
	var url=window.location.href;
	var data=url.split('/');	
	var dataset=data[4];

	var data={dataset:dataset, 'action':action};
  
	 
	 for (var item in config) {	 	
         if (config.hasOwnProperty(item)) {
            var clicked=config[item];
            if (clicked) {
            		data['config_'+item]=true;
            	}
            else {data['config_'+item]=false;}
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

		show_configs(defaults);
}



$( document ).ready(init_page);