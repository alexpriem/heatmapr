
var filter={'empty':false,
			'single':false,
			'int':true,
			'float':true,
			'string':true};
			


var handle_ajax_error=function (result) {

	$('#errorbox').html('<code>' +result.status+ ' ' + result.statusText + ' <pre>'+result.responseText+"</pre>")
	$('#heatmap_div').hide();
}


function update_state  (action) {

	var dataset='best2010';
	var datadir='e:/data';

	var data={dataset:dataset,datadir:datadir, 'action':action};
  
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



var click_action=function () {

	console.log('click_action');	
	update_state(this.id);
}


var click_filter=function () {

	console.log('click_filter', this.id.slice(7));	
	var filter_item=$('#'+this.id).data('filter');
	console.log('filter:',filter);

	var dataset='best2010';
	var datadir='e:/data';

	var state=filter[filter_item];
	if (state) 
		{filter[filter_item]=false;
		$('#toggle_'+filter_item).addClass('btn-default').removeClass('btn-info');
		}
	else 
		{filter[filter_item]=true;
		$('#toggle_'+filter_item).addClass('btn-info').removeClass('btn-default');
		}


	update_state('init');
}


function update_filter() {

	console.log('update_filter');
	$('.data_filter').removeClass('btn-info');
	$('.data_filter').removeClass('btn-default');
	 for (var item in filter) {
	 	console.log('update_filter', item);
         if (filter.hasOwnProperty(item)) {
            var clicked=filter[item];
            if (clicked) { 
            	$('#filter_'+item).addClass('btn-info');
            } else {
            	$('#filter_'+item).addClass('btn-default');
            }
         } //if clicked
     }  //for
}


var handle_ajax=function (result) {


	console.log('handle_ajax');
	r=JSON.parse(result);
    var source   = $("#datacols-template").html();        
    var template = Handlebars.compile(source); 


  //  columns={cols:[{colname:'asdfasdf'},{colname:'asasdf'}]};
  	var columns={cols:r.columns};

  	//console.log(columns);
    data_div=document.getElementById('data_container');
    data_div.innerHTML ='<h3>'+r.dataset+'</h3>'+'<p>'+r.msg+'</p>'+template(columns);
    

    $('.data_action').on("click",click_action);
    $('.data_filter').on("click",click_filter);
    update_filter();
	//console.log(result);


}

function init_interactive (){

	

 	$(".nav-pills").on("click", "a", function(e){     

      tab=$(this).attr('id'); // tab_ts of tab_map
      console.log('tabchange:',this, tab);
      $(this).tab('show');    
      if (tab=='tab_heatmap') {
        $('#data_div').hide();
        $('#heatmap_div').show();
		$('.leftbox').show();
      } 
      if (tab=='tab_data') {        
        $('#data_div').show();
        $('#heatmap_div').hide();                        
        $('.leftbox').hide();
      } 
      e.preventDefault();      
    });

    $('#data_container').css('margin-left',0);        
    $('#data_container').css('top',50); 
    $('.leftbox').hide();

   
   update_state('init');
} 