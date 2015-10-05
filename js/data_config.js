/* config-button at top, for selecting rows in csv. Needs separate tab */


var handle_ajax_error=function (result) {

	$('#errorbox').html(result.status+ ' ' + result.statusText +result.responseText);
}


var handle_ajax=function (result) {

	console.log('handle_ajax');
	r=JSON.parse(result);
	$('#errorbox').html(r.msg);
}

var config_undo_edit=function() {
	
	show_configs (defaults);
	return false;
}

var config_update=function() {
	
	console.log('config_update');

	var enableds=[];
	var colnames=[];
	var typehints=[];
	var formats=[];
	for (i=0; i<defaults.length; i++) {
		enabled=0;
		if ($('#enabled_'+i).hasClass('fa-check-square')) {
			enabled=1;
		}
		typehint=$('#typehint_'+i).val();
		format=$('#format_'+i).val();

		enableds.push(enabled);
		colnames.push(defaults[i].colname);
		typehints.push(typehint);
		formats.push(format);
	}	


	var url=window.location.href;
	var data=url.split('/');	
	var dataset=data[4];

	data={'enabled':enableds,
			'colnames':colnames,
			'typehint':typehints,
			'format':formats};

	console.log(data);
	$.ajax({url:"/set-config/"+dataset+'/', 
			type: "POST",
			'data':data,
			success: handle_ajax,
			error: handle_ajax_error,
		});
	return false;
}



function toggle_enable () {

	rownr=$(this).attr("data-row");
	console.log ('ok')
	if ($(this).hasClass('fa-check-square')) {
		$(this).removeClass('fa-check-square');
		$(this).addClass('fa-square-o');
	} else {
		$(this).removeClass('fa-square-o');
		$(this).addClass('fa-check-square');
	}
}


function show_configs(config){

	var url=window.location.href;
	var data=url.split('/');	
	var dataset=data[4];

	data_div=document.getElementById('data_container');

	var source   = $("#config-template").html();   				
    var template = Handlebars.compile(source); 
    //console.log(config);
    

    if ((config.length)==0){
    	config.push({'enabled':'','colname':'','typehine':'','format':''})    
    }
    s=template({'rows':config,'dataset':dataset});
	
	data_div.innerHTML =s;

	$('#update').on('click',config_update);
	$('#undo').on('click',config_undo_edit);


	$('.enabled').on('click',toggle_enable);
  
}



function init_page () {

		show_configs(defaults);
}



$( document ).ready(init_page);