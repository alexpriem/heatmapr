

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
function MeasureText(text, bold, font, size)
{
    // This global variable is used to cache repeated calls with the same arguments
    var str = text + ':' + bold + ':' + font + ':' + size;
    if (typeof(__measuretext_cache__) == 'object' && __measuretext_cache__[str]) {
        return __measuretext_cache__[str];
    }

    var div = document.createElement('DIV');
        div.innerHTML = text;
        div.style.position = 'absolute';
        div.style.top = '-100px';
        div.style.left = '-100px';
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



var annotations_show=true;

function toggle_annotations () {

	if (annotations_show==true) {
		$('.annotation_label').hide();
		$('.annotation_text').hide();
		$('.annotation_obj').hide();
		$('.annotation_connector').hide();
		annotations_show=false;
	} else {
		$('.annotation_label').show();
		$('.annotation_text').show();
		$('.annotation_obj').show();
		$('.annotation_connector').show();
		annotations_show=true;
	}

}

function handle_annotation(txt) {


}

function handle_options (options) {

	defaults={"stroke":"blue",
				"stroke-width":2,
				"fill":"blue",
				"fill-opacity":0.5};

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
	if ('area' in a) { 
		//handle area

		//console.log(a.area);
		opts=handle_options(a);
		console.log('area:',heatmap, name);
	

		rect=a.area;
		var x0=heatmap.world_to_x(rect[0][0]);    s
		var x1=heatmap.world_to_x(rect[1][0]);    
		var y0=heatmap.world_to_y(rect[0][1]);		
		var y1=heatmap.world_to_y(rect[1][1]);		
		var width=x1-x0;
		var height=y0-y1;

		a.text_y_pos=(height+y0)/2;

		console.log('orig x0/y0, x1/y1:',rect[0][0],rect[0][1],rect[1][0],rect[1][1])
		console.log('x,y:',x0,y0);
		console.log('w,h:',width,height);
		chart.append("rect")
			.attr("id",name)
			.attr("x",x0)
			.attr("y",y1)
			.attr("class","annotation_obj")
			.attr("height",height)
			.attr("data-annotationid",i)
			.attr("width",width)
			.attr("stroke",opts.stroke)
			.attr("stroke-width",opts["stroke-width"])
			.attr("fill",opts.fill)
			.attr("fill-opacity",opts["fill-opacity"]);


		x2=x0+width;
		y2=y1+height/2;
		x3=h.opties.imgwidth+150;

		console.log(x0,y0,x1);

		chart.append("line")			
			.attr("x1", x2)
			.attr("y1", y2)
			.attr("x2", x3)
			.attr("y2", y2)						
			.attr("class","annotation_connector connector_"+i)
			.attr("stroke",opts.stroke)
			.attr("stroke-width",opts["stroke-width"]);

		chart.append("line")			
			.attr("x1", x3)
			.attr("y1", y2)
			.attr("x2", x3)
			.attr("y2", y2+25)
			.attr("class","annotation_connector connector_"+i)
			.attr("stroke",opts.stroke)
			.attr("stroke-width",opts["stroke-width"]);			

		textdimensions=MeasureText (a.label, false, 'Helvetica Neue','14')		
		chart.append('foreignObject')
		    .attr("width", 200)
		    .attr("height", textdimensions[1])
		    .attr('x', x3+10)
		    .attr('y', y2)
		    .attr('data-annotationid',i)
		    .attr("class",'annotation_label')
		    .attr("id",'alabel_'+i)
   	        .append("xhtml:body")		       	        
    		.html('<p>'+a.label+'</p>');

		textdimensions=MeasureText (a.text, false, 'Helvetica Neue','14')
		chart.append('foreignObject')
		    .attr("width", 200)
		    .attr("height", textdimensions[1])
		    .attr('x', x3)
		    .attr('y', 250)
		    .attr('data-annotationid',i)
		    .attr("class",'annotation_text')
		    .attr("id",'atext_'+i)
   	        .append("xhtml:body")		       	        
    		.html('<p>'+a.text+'</p>');
    	
	}


	if ('area_up' in a) { 
		opts=handle_options(a);

		rect=a.area_up;
		var x1=heatmap.world_to_x(rect[0][0]);
		var x2=heatmap.world_to_x(rect[1][0]);
		var y1=rect[0][1];
		var y2=rect[1][1];
		if (y2<y1)  {y1=y2;}
		
				var y1=heatmap.world_to_y(y1);
				var y2=heatmap.world_to_y(heatmap.opties.y_max*0.9);			


		chart.append("svg:path")
			.attr("id",name)
    		.attr("d", "M"+x1+","+y2+"L"+x1+","+y1+"L"+x2+","+y1+"L"+x2+","+y2)
			.attr("stroke",opts.stroke)
			.attr("stroke-width",opts["stroke-width"])
			.attr("fill",opts.fill)
			.attr("fill-opacity",opts["fill-opacity"])
			.attr('marker-end','url(#'+name+'_m)');

      	chart.append("svg:path")
    		.attr("d", "M"+(x2-5)+","+(y2+5)+"L"+x2+","+(y2)+"L"+(x2+5)+","+(y2+5))
			.attr("stroke",opts.stroke)
			.attr("stroke-width",opts["stroke-width"])
			.attr("fill","none");

      	chart.append("svg:path")
    		.attr("d", "M"+(x1-5)+","+(y2+5)+"L"+x1+","+(y2)+"L"+(x1+5)+","+(y2+5))
			.attr("stroke",opts.stroke)
			.attr("stroke-width",opts["stroke-width"])
			.attr("fill","none");
	}


	if ('area_down' in a) { 
		opts=handle_options(a);

		rect=a.area_down;
		var x1=heatmap.world_to_x(rect[0][0]);
		var x2=heatmap.world_to_x(rect[1][0]);
		var y1=rect[0][1];
		var y2=rect[1][1];
		if (y2<y1)  {y1=y2;}
		
				var y1=heatmap.world_to_y(y1);
				var y2=heatmap.world_to_y(heatmap.opties.y_max*0.9);			

		chart.append("svg:path")
			.attr("id",name)
    		.attr("d", "M"+x1+","+y1+"L"+x1+","+y2+"L"+x2+","+y2+"L"+x2+","+y1)
			.attr("stroke",opts.stroke)
			.attr("stroke-width",opts["stroke-width"])
			.attr("fill",opts.fill)
			.attr("fill-opacity",opts["fill-opacity"])
			.attr('marker-end','url(#'+name+'_m)');

      	chart.append("svg:path")
    		.attr("d", "M"+(x2-5)+","+(y1-5)+"L"+x2+","+(y1)+"L"+(x2+5)+","+(y1-5))
			.attr("stroke",opts.stroke)
			.attr("stroke-width",opts["stroke-width"])
			.attr("fill","none");

      	chart.append("svg:path")
    		.attr("d", "M"+(x1-5)+","+(y1-5)+"L"+x1+","+(y1)+"L"+(x1+5)+","+(y1-5))
			.attr("stroke",opts.stroke)
			.attr("stroke-width",opts["stroke-width"])
			.attr("fill","none");
	}

	if ('area_right' in a) { 
		opts=handle_options(a);

		rect=a.area_right;
		var x1=heatmap.world_to_x(rect[0][0]);
		var x2=heatmap.world_to_x(rect[1][0]);
		var y1=rect[0][1];
		var y2=rect[1][1];
		if (x2<x1)  {x1=x2;}
		
		var y1=heatmap.world_to_y(y1);
		var y2=heatmap.world_to_y(y2);			

		chart.append("svg:path")
			.attr("id",name)
    		.attr("d", "M"+x2+","+y2+"L"+x1+","+y2+"L"+x1+","+y1+"L"+x2+","+y1)
			.attr("stroke",opts.stroke)
			.attr("stroke-width",opts["stroke-width"])
			.attr("fill",opts.fill)
			.attr("fill-opacity",opts["fill-opacity"])
			.attr('marker-end','url(#'+name+'_m)');

      	chart.append("svg:path")
    		.attr("d", "M"+(x2-5)+","+(y1-5)+"L"+x2+","+(y1)+"L"+(x2-5)+","+(y1+5))
			.attr("stroke",opts.stroke)
			.attr("stroke-width",opts["stroke-width"])
			.attr("fill","none");

      	chart.append("svg:path")
    		.attr("d", "M"+(x2-5)+","+(y2-5)+"L"+x2+","+(y2)+"L"+(x2-5)+","+(y2+5))
			.attr("stroke",opts.stroke)
			.attr("stroke-width",opts["stroke-width"])
			.attr("fill","none");
	}

	if ('area_left' in a) { 
		opts=handle_options(a);

		rect=a.area_left;
		var x1=heatmap.world_to_x(rect[0][0]);
		var x2=heatmap.world_to_x(rect[1][0]);
		var y1=rect[0][1];
		var y2=rect[1][1];
		if (x2<x1)  {x1=x2;}
		
		var y1=heatmap.world_to_y(y1);
		var y2=heatmap.world_to_y(y2);			

		chart.append("svg:path")
			.attr("id",name)
    		.attr("d", "M"+x1+","+y2+"L"+x2+","+y2+"L"+x2+","+y1+"L"+x1+","+y1)
			.attr("stroke",opts.stroke)
			.attr("stroke-width",opts["stroke-width"])
			.attr("fill",opts.fill)
			.attr("fill-opacity",opts["fill-opacity"])
			.attr('marker-end','url(#'+name+'_m)');

      	chart.append("svg:path")
    		.attr("d", "M"+(x1+5)+","+(y1-5)+"L"+x1+","+(y1)+"L"+(x1+5)+","+(y1+5))
			.attr("stroke",opts.stroke)
			.attr("stroke-width",opts["stroke-width"])
			.attr("fill","none");

      	chart.append("svg:path")
    		.attr("d", "M"+(x1+5)+","+(y2-5)+"L"+x1+","+(y2)+"L"+(x1+5)+","+(y2+5))
			.attr("stroke",opts.stroke)
			.attr("stroke-width",opts["stroke-width"])
			.attr("fill","none");
	}


	if ('polygon' in a) {		
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
			.attr("fill-opacity",opts["fill-opacity"]);		
	}


	//console.log('heatmap',heatmap);
	$('#'+name).on('click',heatmap.click_annotation);
//	$('#alabel_'+i).on('click',click_annotation);
	$('#'+name).on('hover',heatmap.show_area);
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


function edit_annotations () {

console.log('edit_annotations');	
}


function init_annotations (heatmap, annotations) {

	var i=0;
	for (var a in annotations) {
  		if (annotations.hasOwnProperty(a)) {
  			console.log('init_annotations:',a);
    		show_annotation (heatmap, a, annotations[a], i);
    		i=i+1;
	  }
	}

}