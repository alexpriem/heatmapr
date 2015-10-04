// https://developer.mozilla.org/en-US/docs/Web/API/FileReader#readAsDataURL%28%29




function show_labels(labels){


	console.log(labels);
	data_div=document.getElementById('data_container');    

	var source   = $("#labels-template").html();   				
    var template = Handlebars.compile(source);     
    

    label_ctx=[];
    for (i=0; i<labels.length; i++) {
    	label_ctx.push({col:labels[i][0], label:labels[i][1]});
    }
    s=template({'rows':label_ctx});
	
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