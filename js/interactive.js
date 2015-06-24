

var handle_ajax_error=function (result) {

	$('#errorbox').html('<code>' +result.status+ ' ' + result.statusText + ' <pre>'+result.responseText+"</pre>")
	$('#heatmap_div').hide();
}



var handle_ajax=function (result) {


	r=JSON.parse(result);
    var source   = $("#datacols-template").html();        
    var template = Handlebars.compile(source); 


  //  columns={cols:[{colname:'asdfasdf'},{colname:'asasdf'}]};
  	var columns={cols:r.columns};

  	console.log(columns);
    data_div=document.getElementById('data_container');
    data_div.innerHTML ='<h3>'+r.dataset+'</h3>'+'<p>'+r.msg+'</p>'+template(columns);
    

    $('.data_action').on("click",click_action);
	console.log(result);


}

var click_action=function () {

	console.log('click_action');	
	var dataset='best2010';
	var datadir='e:/data';

	$.ajax({url:"/dataset/"+dataset, 
			type: "GET",
			data:{dataset:dataset,datadir:datadir, action:this.id}, 
			success: handle_ajax,
			error: handle_ajax_error,

		});

}

function init_interactive (){

	

 	$(".nav-pills").on("click", "a", function(e){     

      tab=$(this).attr('id'); // tab_ts of tab_map
      console.log('tabchange:',this, tab);
      $(this).tab('show');    
      if (tab=='tab_heatmap') {
        $('#data_div').hide();
        $('#heatmap_div').show();
      } 
      if (tab=='tab_data') {        
        $('#data_div').show();
        $('#heatmap_div').hide();                        
      } 
      e.preventDefault();      
    });

    $('#data_container').css('margin-left',0);        
    $('#data_container').css('top',50); 


   


	var dataset="best2010";
	var datadir='e:/data';
	$.ajax({url:"/dataset/"+dataset, 
			type: "GET",
			data:{dataset:dataset,datadir:datadir, action:'init'}, 
			success: handle_ajax,
			error: handle_ajax_error,

		});
} 