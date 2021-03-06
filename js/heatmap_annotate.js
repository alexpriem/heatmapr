








/**
* Measures text by creating a DIV in the document and adding the relevant text to it.
* Then checking the .offsetWidth and .offsetHeight. Because adding elements to the DOM is not particularly
* efficient in animations (particularly) it caches the measured text width/height.
* 
* @param  string text   The text to measure
* @param  bool   bold   Whether the text is bold or not
* @param  string font   The font to use
* @param  size   number The size of the text (in pts)
* @return array         A two element array of the width and height of the text
*/

var text_width=200;



function MeasureText(html, textwidth, bold, font, size)
{
    // This global variable is used to cache repeated calls with the same arguments
    var str = html + ':' + bold + ':' + font + ':' + size;
    if (typeof(__measuretext_cache__) == 'object' && __measuretext_cache__[str]) {
        return __measuretext_cache__[str];
    }

    var div = document.createElement('DIV');
        div.innerHTML = html;
        div.style.position = 'absolute';
        div.style.top = '-100px';
        div.style.left = '-100px';
        div.style.width = textwidth+'px';   //
        div.style.fontFamily = font;
        div.style.fontWeight = bold ? 'bold' : 'normal';
        div.style.fontSize = size + 'pt';
    document.body.appendChild(div);
    
    var size = [div.offsetWidth, div.offsetHeight];

    document.body.removeChild(div);
    
    // Add the sizes to the cache as adding DOM elements is costly and can cause slow downs
    if (typeof(__measuretext_cache__) != 'object') {
        __measuretext_cache__ = [];
    }
    __measuretext_cache__[str] = size;
    
    return size;
}


function show_area () {


}



function edit_annotation (a) {

	$('#overlay').css('visibility','visible');   

		//sel_id=$('#selectie_id').val(sel_id);
	$('#selectie_xvar').html('X:'+a.xvar);
	$('#selectie_yvar').html('Y:'+a.yvar);

	$('#selectie_id').val(a.selectie_id);
	$('#selectie_xmin').val(a.xmin);
	$('#selectie_xmax').val(a.xmax);
	$('#selectie_ymin').val(a.ymin);		
	$('#selectie_ymax').val(a.ymax);
	$('#text_xpos').val(a.text_xpos);		
	$('#text_ypos').val(a.text_ypos);
	$('#connector_direction').val(a.connector_direction);
	$('#selectie_filename').val(a.filename);
	$('#selectie_txt').val(a.txt);
	$('#label_txt').val(a.label);
	edit_annotation_flag=true;
}



function toggle_annotations () {

	if (annotations_show==true) {
		$('.annotation_label').hide();
		$('.annotation_text').hide();
		$('.annotation_obj').hide();
		$('.annotation_connector').hide();
		annotations_show=false;
	} else {
		$('.annotation_label').show();
		$('.annotation_text').hide();
		$('.annotation_obj').show();
		$('.annotation_connector').show();
		annotations_show=true;
	}

}



function handle_options (options) {

	defaults={"stroke":"blue",
				"stroke-width":2,
				"fill":"blue"};

	var new_options={};
	for (var o in defaults) {
  		if (defaults.hasOwnProperty(o)) {  			
  	//		console.log(o, options[o],defaults[o]);
  			if (options.hasOwnProperty(o)) {
  				new_options[o]=options[o];
  			} else {
  				new_options[o]=defaults[o];
  			}  		 
	  }
	}
//	console.log ('handle_options:',new_options);
	return new_options;
}

/*

function click_annotation () {

	console.log('click_annotation')
	console.log('clicked',$(this).attr("data-annotationid")); 


}
*/


function show_annotation (heatmap, name, a, i){

	console.log('init_annotation:',a);





	chart=heatmap.chart;
	if (a.areatype=='area') { 
		//handle area
		
		opts=handle_options(a);
		console.log('area-annotation:',a);
	
		
		var x0=heatmap.world_to_x(a.xmin);    s
		var x1=heatmap.world_to_x(a.xmax);    
		var y0=heatmap.world_to_y(a.ymin);		
		var y1=heatmap.world_to_y(a.ymax);		
		var width=x1-x0;
		var height=y0-y1;

		

		console.log('orig x0/y0, x1/y1:',a.xmin, a.ymin, a.xmax, a.ymax)
		console.log('x,y:',x0,y0);
		console.log('w,h:',width,height);
		chart.append("rect")
			.attr("id",'annotation_obj_'+i)
			.attr("x",x0)
			.attr("y",y1)
			.attr("class","annotation annotation_obj")
			.attr("height",height)
			.attr("data-annotationid",i)
			.attr("width",width)
			.attr("stroke",opts.stroke)
			.attr("stroke-width",opts["stroke-width"])
			.attr("fill",opts.fill);
			

		sidebar_text_xpos=h.opties.imgwidth+150;
		if (a.connector_direction=='right') {
			x2=x0+width;	
			sidebar_text_xpos=h.opties.imgwidth+150;
		}
		if (a.connector_direction=='topright') {
			x2=x0+0.75*width;	
			sidebar_text_xpos=h.opties.imgwidth+150;
		}
		if (a.connector_direction=='bottomright') {
			x2=x0+width;	
			sidebar_text_xpos=h.opties.imgwidth+150;
		}


		console.log(x0,y0,x1);

		if ((a.connector_direction=='right') || (a.connector_direction=='bottomright') || (a.connector_direction=='topright')) {
			chart.append("line")			
				.attr("x1", x2)
				.attr("y1", a.text_ypos+15)
				.attr("x2", a.text_xpos)
				.attr("y2", a.text_ypos+15)						
				.attr("class","annotation annotation_connector connector_"+i)
				.attr("stroke",opts.stroke)
				.attr("stroke-width",opts["stroke-width"]);
			}



		if (a.connector_direction=='topright') {
			chart.append("line")			
				.attr("x1", x2)
				.attr("y1", a.text_ypos+15)
				.attr("x2", x2)
				.attr("y2", y1)						
				.attr("class","annotation annotation_connector connector_"+i)
				.attr("stroke",opts.stroke)
				.attr("stroke-width",opts["stroke-width"]);
		}

		if (a.connector_direction=='bottomright') {
			chart.append("line")			
				.attr("x1", x2)
				.attr("y1", a.text_ypos+15)
				.attr("x2", x2)
				.attr("y2", y0)						
				.attr("class","annotation annotation_connector connector_"+i)
				.attr("stroke",opts.stroke)
				.attr("stroke-width",opts["stroke-width"]);
		}

/*
		chart.append("line")			
			.attr("x1", a.text_xpos)
			.attr("y1", a.text_ypos)
			.attr("x2", a.text_xpos)
			.attr("y2", a.text_xpos+25)
			.attr("class","annotation annotation_connector connector_"+i)
			.attr("stroke",opts.stroke)
			.attr("stroke-width",opts["stroke-width"]);			
*/

		textdimensions=MeasureText (a.label, text_width, true, 'Helvetica Neue','14')		
		labelheight=textdimensions[1];

		$('#heatmap_container_0').append('<div id="alabel_'+i+'"><p>'+a.label+'</p></div>');

		$('#alabel_'+i).css("width", 200)
		    .css("height", labelheight+15)
		    .css("position", 'absolute')
		    .css("left", a.text_xpos+10)
		    .css("top", a.text_ypos)
		    .attr('data-annotationid',i)
		    .attr("class",'annotation annotation_label');		    	

    	txt_html='<div id="atext_'+i+'" <h5><strong>'+a.label+'</strong></h5><p>'+a.text+'</p></div>';

		textdimensions=MeasureText (txt_html, text_width, false, 'Helvetica Neue','14');
		textheight=textdimensions[1];
		$('#heatmap_container_0').append(txt_html);
		
		$('#atext_'+i)		
		    .css("width", text_width)
		    .css("height", textheight)
		    .css('left', sidebar_text_xpos)
		    .css('top', 250)
		    .attr('data-annotationid',i)
		    .attr("class",'annotation annotation_text');		    
    	


		if ((a.connector_direction=='right') || (a.connector_direction=='bottomright') || (a.connector_direction=='topright')) {
		
			var bottom_pos=250+textheight*0.65;
			if (bottom_pos<a.text_ypos+labelheight) {
				bottom_pos=a.text_ypos+labelheight;
			}
			chart.append("line")	
				.attr('id','annotation_textc_'+i)		
				.attr("x1", sidebar_text_xpos)
				.attr("y1", 250)
				.attr("x2", sidebar_text_xpos)
				.attr("y2", bottom_pos)
				.attr("class","annotation annotation_text")
				.attr("stroke",opts.stroke)
				.attr("stroke-width",opts["stroke-width"]);			    	
		}
		console.log('done');
	}


	if (a.areatype=='area_up') { 
		opts=handle_options(a);
		
		var x1=heatmap.world_to_x(a.xmin);
		var x2=heatmap.world_to_x(a.xmax);
		var y1=a.ymin;
		var y2=a.ymax;
		if (y2<y1)  {y1=y2;}
		
				var y1=heatmap.world_to_y(y1);
				var y2=heatmap.world_to_y(heatmap.opties.y_max*0.9);			


		chart.append("svg:path")
			.attr("id",name)
    		.attr("d", "M"+x1+","+y2+"L"+x1+","+y1+"L"+x2+","+y1+"L"+x2+","+y2)
			.attr("stroke",opts.stroke)
			.attr("class","annotation")
			.attr("stroke-width",opts["stroke-width"])
			.attr("fill",opts.fill)
			//.attr("fill-opacity",opts["fill-opacity"])
			.attr('marker-end','url(#'+name+'_m)');

      	chart.append("svg:path")
    		.attr("d", "M"+(x2-5)+","+(y2+5)+"L"+x2+","+(y2)+"L"+(x2+5)+","+(y2+5))
			.attr("stroke",opts.stroke)
			.attr("class","annotation")
			.attr("stroke-width",opts["stroke-width"])
			.attr("fill","none");

      	chart.append("svg:path")
    		.attr("d", "M"+(x1-5)+","+(y2+5)+"L"+x1+","+(y2)+"L"+(x1+5)+","+(y2+5))
			.attr("stroke",opts.stroke)
			.attr("class","annotation")
			.attr("stroke-width",opts["stroke-width"])
			.attr("fill","none");
	}


	if (a.areatype=='area_down') { 
		opts=handle_options(a);
		
		var x1=heatmap.world_to_x(a.xmin);
		var x2=heatmap.world_to_x(a.xmax);
		var y1=a.ymin;
		var y2=a.ymax;
		if (y2<y1)  {y1=y2;}
		
				var y1=heatmap.world_to_y(y1);
				var y2=heatmap.world_to_y(heatmap.opties.y_max*0.9);			

		chart.append("svg:path")
			.attr("id",name)
    		.attr("d", "M"+x1+","+y1+"L"+x1+","+y2+"L"+x2+","+y2+"L"+x2+","+y1)
			.attr("stroke",opts.stroke)
			.attr("class","annotation")
			.attr("stroke-width",opts["stroke-width"])
			.attr("fill",opts.fill)
			//.attr("fill-opacity",opts["fill-opacity"])
			.attr('marker-end','url(#'+name+'_m)');

      	chart.append("svg:path")
    		.attr("d", "M"+(x2-5)+","+(y1-5)+"L"+x2+","+(y1)+"L"+(x2+5)+","+(y1-5))
			.attr("stroke",opts.stroke)
			.attr("class","annotation")
			.attr("stroke-width",opts["stroke-width"])
			.attr("fill","none");

      	chart.append("svg:path")
    		.attr("d", "M"+(x1-5)+","+(y1-5)+"L"+x1+","+(y1)+"L"+(x1+5)+","+(y1-5))
			.attr("stroke",opts.stroke)
			.attr("class","annotation")
			.attr("stroke-width",opts["stroke-width"])
			.attr("fill","none");
	}

	if (a.areatype=='area_right') { 
		opts=handle_options(a);
		
		var x1=heatmap.world_to_x(a.xmin);
		var x2=heatmap.world_to_x(a.xmax);
		var y1=a.ymin;
		var y2=a.ymax;
		if (x2<x1)  {x1=x2;}
		
		var y1=heatmap.world_to_y(y1);
		var y2=heatmap.world_to_y(y2);			

		chart.append("svg:path")
			.attr("id",name)
    		.attr("d", "M"+x2+","+y2+"L"+x1+","+y2+"L"+x1+","+y1+"L"+x2+","+y1)
			.attr("stroke",opts.stroke)
			.attr("stroke-width",opts["stroke-width"])
			.attr("class","annotation")
			.attr("fill",opts.fill)
			//.attr("fill-opacity",opts["fill-opacity"])
			.attr('marker-end','url(#'+name+'_m)');

      	chart.append("svg:path")
    		.attr("d", "M"+(x2-5)+","+(y1-5)+"L"+x2+","+(y1)+"L"+(x2-5)+","+(y1+5))
			.attr("stroke",opts.stroke)
			.attr("class","annotation")
			.attr("stroke-width",opts["stroke-width"])
			.attr("fill","none");

      	chart.append("svg:path")
    		.attr("d", "M"+(x2-5)+","+(y2-5)+"L"+x2+","+(y2)+"L"+(x2-5)+","+(y2+5))
			.attr("stroke",opts.stroke)
			.attr("class","annotation")
			.attr("stroke-width",opts["stroke-width"])
			.attr("fill","none");
	}

	if (a.areatype=='area_left') { 
		opts=handle_options(a);
		
		var x1=heatmap.world_to_x(a.xmin);
		var x2=heatmap.world_to_x(a.xmax);
		var y1=a.ymin;
		var y2=a.ymax;
		if (x2<x1)  {x1=x2;}
		
		var y1=heatmap.world_to_y(y1);
		var y2=heatmap.world_to_y(y2);			

		chart.append("svg:path")
			.attr("id",name)
    		.attr("d", "M"+x1+","+y2+"L"+x2+","+y2+"L"+x2+","+y1+"L"+x1+","+y1)
			.attr("stroke",opts.stroke)
			.attr("class","annotation")
			.attr("stroke-width",opts["stroke-width"])
			.attr("fill",opts.fill)
			//.attr("fill-opacity",opts["fill-opacity"])
			.attr('marker-end','url(#'+name+'_m)');

      	chart.append("svg:path")
    		.attr("d", "M"+(x1+5)+","+(y1-5)+"L"+x1+","+(y1)+"L"+(x1+5)+","+(y1+5))
			.attr("stroke",opts.stroke)
			.attr("class","annotation")
			.attr("stroke-width",opts["stroke-width"])
			.attr("fill","none");

      	chart.append("svg:path")
    		.attr("d", "M"+(x1+5)+","+(y2-5)+"L"+x1+","+(y2)+"L"+(x1+5)+","+(y2+5))
			.attr("stroke",opts.stroke)
			.attr("class","annotation")
			.attr("stroke-width",opts["stroke-width"])
			.attr("fill","none");
	}


	if (a.areatype=='polygon') {		
		p=a.polygon;
		opts=handle_options(a);
		var d3poly=[];
		for (i=0; i<p.length; i++) {
			d3poly.push({'x':p[i][0], 'y':p[i][1]});
		}
		d3poly.push({'x':p[0][0], 'y':p[0][1]});

		var lineFunction = d3.svg.line()
								.x(function(d) { return heatmap.world_to_x(d.x); })
								.y(function(d) { return heatmap.world_to_y(d.y); });

		chart.append("path")
			.attr("id",name)
            .attr("d", lineFunction(d3poly))
			.attr("stroke",opts.stroke)
			.attr("stroke-width",opts["stroke-width"])
			.attr("fill",opts.fill)
			//.attr("fill-opacity",opts["fill-opacity"]);		
	}


	//console.log('heatmap',heatmap);
	
}



function show_annotations () {



	$('#histogramdiv').hide();
	$('.hist_y').hide();
	$('.hist_x').hide();

 console.log('show_annotations');

 h=heatmaps[0];
 annotations=h.opties.annotate;
 
 var i=0;
 for (var a in annotations) { 		
  		if (annotations.hasOwnProperty(a)) {
  			console.log(a);
    		show_annotation (h, a, annotations[a],i);
    		i=i+1;
	  }
	}
}



function update_edit_annotations () {
	
	if (edit_annotations) {		
		$('#edit_annotations').addClass('active');
	} else {
		$('#edit_annotations').removeClass('active');
	}
}




function toggle_edit_annotations () {



	if (edit_annotations) {
		edit_annotations=false;				
	} else {
		edit_annotations=true;		
	}
	update_edit_annotations ();
	console.log('edit_annotations:',edit_annotations );	
}


function init_annotations (heatmap, annotations) {

	var i=0;
	console.log('init_annotations:', annotations.length);
	
	for (var a in annotations) {
  		if (annotations.hasOwnProperty(a)) {
  			console.log('init_annotations:',a);
    		show_annotation (heatmap, a, annotations[a], i);
    		i=i+1;
	  }
	}

 $('.annotation_label').on('click',heatmap.click_annotation);
 $('.annotation_obj').on('click',heatmap.click_annotation);
 $('.annotation_obj').on('mouseenter',heatmap.enter_annotation );
 $('.annotation_obj').on('mouseleave',heatmap.leave_annotation );
 
}

