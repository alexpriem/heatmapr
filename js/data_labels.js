// https://developer.mozilla.org/en-US/docs/Web/API/FileReader#readAsDataURL%28%29


var undo_edit=function() {
	
	return false;
}

var update_labels=function() {
	
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


function show_labels(labels){


	var url=window.location.href;
	var data=url.split('/');	
	var dataset=data[4];

	console.log(labels);
	data_div=document.getElementById('data_container');    

	var source   = $("#labels-template").html();   				
    var template = Handlebars.compile(source);     
    

    label_ctx=[];
    for (i=0; i<labels.length; i++) {
    	label_ctx.push({col:labels[i][0], label:labels[i][1]});
    }
    s=template({'rows':label_ctx,'dataset':dataset});
	
	data_div.innerHTML =s;

	$('#update').on('click',update_labels);
	$('#undo').on('click',undo_edit);
	
}



function init_page() {
 

	var url=window.location.href;
	var data=url.split('/');	
	var dataset=data[4];
	console.log('init_page:',dataset);

	show_labels(defaults);
	
}

$( document ).ready(init_page);