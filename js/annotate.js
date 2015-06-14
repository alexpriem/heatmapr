



function handle_annotation(txt) {


}

function handle_options (options) {

	defaults={"stroke":"red",
				"stroke-width":2,
				"fill":"red",
				"fill-opacity":0.5};

	var new_options={};
	for (var o in defaults) {
  		if (defaults.hasOwnProperty(o)) {  			
  			console.log(o, options[o],defaults[o]);
  			if (options.hasOwnProperty(o)) {
  				new_options[o]=options[o];
  			} else {
  				new_options[o]=defaults[o];
  			}  		 
	  }
	}
	console.log ('NEW_OPT',new_options);
	return new_options;
}


function init_annotation (heatmap, name, a){

	//console.log('init_annotation:',a);



	chart=heatmap.chart;
	if ('area' in a) { 
		//handle area

		console.log(a.area);
		opts=handle_options(a);
		console.log('area:',a,opts);

		rect=a.area;
		var x=heatmap.world_to_x(rect[0][0]);    // map to svg coord from heatmap coord
		var y=heatmap.world_to_y(rect[0][1]);		
		var width=heatmap.world_to_x(rect[1][0])-x;
		var height=y-heatmap.world_to_y(rect[1][1]);

		a.text_y_pos=(height+y)/2;
		console.log('x,y:u,v',x,y,rect[0]);
		console.log('w,h:u,v',width,height,rect[1]);
		chart.append("rect")
			.attr("id",name)
			.attr("x",x)
			.attr("y",y)
			.attr("height",height)
			.attr("width",width)
			.attr("stroke",opts.stroke)
			.attr("stroke-width",opts["stroke-width"])
			.attr("fill",opts.fill)
			.attr("fill-opacity",opts["fill-opacity"]);

	}


	if ('area_up' in a) { 
		opts=handle_options(a);

		rect=a.area_up;
		var x1=heatmap.world_to_x(rect[0][0]);
		var x2=heatmap.world_to_x(rect[1][0]);
		var y1=rect[0][1];
		var y2=rect[1][1];
		if (y2<y1)  {y1=y2;}

		var y=heatmap.world_to_y(y1);
		var y2=heatmap.world_to_y(heatmap.opties.y_max*0.9);



		chart.append("svg:path")
			.attr("id",name)
    		.attr("d", "M"+x1+","+y2+"L"+x1+","+y+"L"+x2+","+y+"L"+x2+","+y2)
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


	console.log('heatmap',heatmap);
	$('#'+name).on('click',heatmap.click_annotation);
	$('#'+name).on('hover',heatmap.show_area);
}


function init_annotations (heatmap, annotations) {

	for (var a in annotations) {
  		if (annotations.hasOwnProperty(a)) {
  			console.log(a);
    		init_annotation (heatmap, a, annotations[a]);
	  }
	}

}