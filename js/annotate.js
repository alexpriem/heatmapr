



function handle_annotation(txt) {


}



function init_annotation (heatmap, name, a){

	//console.log('init_annotation:',a);
	chart=heatmap.chart;
	if ('area' in a) { 
		//handle area
		console.log('area:',a);

		rect=a.area;
		var x=heatmap.world_to_x(rect[0][0]);    // map to svg coord from heatmap coord
		var y=heatmap.world_to_y(rect[0][1]);		
		var width=heatmap.world_to_x(rect[1][0])-x;
		var height=y-heatmap.world_to_y(rect[1][1]);

		console.log('x,y:u,v',x,y,rect[0]);
		console.log('w,h:u,v',width,height,rect[1]);
		chart.append("rect")
			.attr("id",name)
			.attr("x",x)
			.attr("y",y)
			.attr("height",height)
			.attr("width",width)
			.attr("stroke",'red')
			.attr("stroke-width",2)
			.attr("fill","red")
			.attr("fill-opacity",0.5)

	}

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