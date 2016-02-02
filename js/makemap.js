

var expert=false; 

var handle_ajax_error=function (result) {

	$('#errorbox').html('<code>' +result.status+ ' ' + result.statusText + ' <pre>'+result.responseText+"</pre>")
	$('#heatmap_div').hide();
}



var handle_ajax=function (result) {

  	var url=window.location.href;
    var data=url.split('/');    
    var dataset=data[4];
    var xyi=data[5].split('_');
    
	console.log('handle_ajax:', data);
	r=JSON.parse(result);
	console.log(r);
	
	var result_url='/heatmap/'+dataset + '/' + r.x_var + '/' + r.y_var + '/' + r.heatmap_index + '/';
	$('#resultdiv').html('<a href="'+result_url+'" id="result"> Resultaat</a> ');      
}




function make_heatmap (addmap) {

    

    console.log('makemap:expertmode:',expert);
    var url=window.location.href;
    var data=url.split('/');    
    var dataset=data[4];
    
    var data={'cmd':'makemap','add_new_heatmap':addmap};


    console.log("make_heatmap");
    for (var key in defaults) {
    	 if(defaults.hasOwnProperty(key)){    	 	
    	 	ex=$('#'+key).hasClass('expert');
    	 	val=$('#'+key).val();
            console.log(key,val,ex);
            if ((expertmode==false) && (ex==true)) {
                data[key]=defaults[key];
                continue;
            } 
    	 	if (val==undefined) {
    	 		data[key]=defaults[key];
    	 		continue;
    	 	} 

            data[key]=val;           
    	 }
    }

    data['dataset']=dataset;
    data['expertmode']=expert;
    //return;
    console.log(data);
	$.ajax({url:"/make_heatmap/", 
			type: "POST",
			'data':data,
			success: handle_ajax,
			error: handle_ajax_error,
		});  	
}



function makemap () {

	addmap=false;
	$('#makemap_result').html('<div id="resultdiv" class="error">  Wacht op resultaat </div>');
	$('#add_result').html('');
	make_heatmap (addmap);    	
}


function addmap () {

	desc=$('#description').val().trim();
	if (desc.length==0)  {
		$('#description_error').html('Omschrijving moet ingevuld zijn bij toevoegen heatmaps');
		return;
	}
	$('#description_error').html('');

	addmap=true;
	make_heatmap (addmap);    
	$('#makemap_result').html('');	
	$('#addmap_result').html('<div id="resultdiv" class="error">  Wacht op resultaat </div>');
}


function toggle_expert () {

 console.log('toggle_expert',expert);
 if (expert) {
 	$('.expert').hide();
    $('#expertmode_label').html('uit');
 	expert=false;
 } else { 
	$('.expert').show();
    $('#expertmode_label').html('aan');
 	expert=true;
 }

}


function init_page() {

    $('.combobox').combobox();    
    $('#makemap').on('click',makemap);
    $('#addmap').on('click',addmap);
    $('#expertmode').on('click', toggle_expert);

    if (expert==false) {
    	$('.expert').hide();     
        $('#expertmode_label').html('uit');   
    } else { 
	    $('.expert').show();       
        $('#expertmode_label').html('aan');
	}

    for (var key in defaults) {
    	 if(defaults.hasOwnProperty(key)){
    	 	$('#'+key).val(defaults[key]);
    	 }
    }
}



$( document ).ready(init_page);
