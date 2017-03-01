


var enter_navitem=function  () {
	elname='#'+this.id
 if ($(elname).hasClass('active')) {
 		$(elname).addClass('hover_active').removeClass('active'); 		
 		//console.log ('hover_navbar, active:',this.id);		
 		//$('#'+this.id).attr('background-color','#84afd3');
 } else { 		
 		$(elname).addClass('hover_inactive'); 	
 }
}


var leave_navitem=function  () {
	elname='#'+this.id
 if ($(elname).hasClass('hover_active')) {
 		$(elname).addClass('active').removeClass('hover_active'); 		
 } else {
 	//	console.log ('hover_navbar, inactive:',this.id);
 		$(elname).removeClass('hover_inactive'); 	
 }
}



var click_navbar=function () {

	console.log('click_navbar:', this.id);
}




var selected_annotation=undefined;

transform_value=function  (val,transform, log_min) {

	if (transform=='sqrt') {
		if (val>0) {
			val=Math.sqrt(val);
		} else {
			val=-Math.sqrt(-val);
		}
	}
	if (transform=='log') {
		if (val>=0) {
			if ((val>=0) && (val<=log_min)) {
				return Math.log(log_min)/Math.LN10;   //null?
			}
			val=Math.log(val)/Math.LN10;
		} else {
			if ((val<=0) && (val>=-log_min)) {
				return -Math.log(log_min);
			}
			if (val<0) {
				val=-Math.log(-val)/Math.LN10;
			}
		}
	}
	return val;
}



	handle_selection_ajax_error=function (result) {

			console.log("ajax error");
			$('#errorbox').html(result.status+ ' ' + result.statusText +result.responseText);
			$('#heatmap_div').hide();
	}

	handle_selection_ajax=function (result) {

			console.log("selectie klaar");
			//h=new heatmap_histogram ('heatmap_svg_0',500, 250);
			//this.histogram=h;
			var h=heatmaps[0];	
			console.log (result);
			var annotaties=result.annotaties;
			$('.annotation').remove();
			$('#dragrect_0').remove();
			init_annotations (h, annotaties);
			
	}



	function delete_selection () {	
		update_selection (mode='delete');
	}

	function save_selection () {	
		update_selection (mode='edit');
	}



	function update_selection  (mode) {	

		
		sel_id=parseInt($('#selectie_id').val());
		sel_xmin=parseFloat($('#selectie_xmin').val());
		sel_xmax=parseFloat($('#selectie_xmax').val());
		sel_ymin=parseFloat($('#selectie_ymin').val());
		sel_ymax=parseFloat($('#selectie_ymax').val());
		text_xpos=$('#text_xpos').val();		
		text_ypos=$('#text_ypos').val();
		connector_direction=$('#connector_direction').val();
		filename=$('#selectie_filename').val();
		text=$('#selectie_txt').val();
		label=$('#label_txt').val();
		
		console.log('update_selection,sel_id:',sel_id);

		if (sel_xmin>sel_xmax) {
			t=sel_xmax; sel_xmax=sel_xmin; sel_xmin=t;
		}
		if (sel_ymin>sel_ymax) {
			t=sel_ymax; sel_ymax=sel_ymin; sel_ymin=t;
		}

		areatype='area';
		//areatype=$('#areatype').val(); 


		var url=window.location.href;
		var data=url.split('/');	
		var dataset=data[4];
		var heatmap_xvar=data[5];
		var heatmap_yvar=data[6];
		var heatmap_index=data[7];

		var h=heatmaps[0];
		num_annotaties=0;
		var annotaties={};
		if ('annotate' in h.opties) {			
			var annotaties=h.opties.annotate;
//			console.log(annotaties);

			if ($.isEmptyObject(annotaties)) {
				num_annotaties=0;			
			} else {
			 	num_annotaties=Object.keys(annotaties).length;
			}
		} 
		
		console.log('num_annotaties:',num_annotaties);

		var data={dataset:dataset, 
					'xvar':heatmap_xvar,
					'yvar':heatmap_yvar,
					'heatmap_index':heatmap_index					
				};


		for (var i in annotaties) {
		  if (annotaties.hasOwnProperty(i)) {
		  		a=annotaties[i];

		  		if (mode=='delete') {
		  			if (a.selectie_id==sel_id) {
		  				num_annotaties=num_annotaties-1;
		  				continue;
		  			}
		  		}

		    			    	
				data['xmin_'+i]=a.xmin;
				data['xmax_'+i]=a.xmax;
				data['ymin_'+i]=a.ymin;
				data['ymax_'+i]=a.ymax;
				data['text_xpos_'+i]=a.text_xpos;
				data['text_ypos_'+i]=a.text_ypos;
				data['connector_direction_'+i]=a.connector_direction;
				data['filename_'+i]=a.filename;
				data['text_'+i]=a.text;
				data['label_'+i]=a.label;
				data['areatype_'+i]=a.areatype;
				data['selectie_id_'+i]=a.selectie_id;
			}
		}


		if (mode=='edit') {
			nr=num_annotaties; // nieuwe selectie: nieuw id aanmaken.
			if ((edit_annotations) && (edit_annotation_flag)){   // we zijn in editmode en een bestaande selectie aan het editten. 
							// id van gedditte selectie oppikken
				nr=sel_id;
			}

			

			data['xmin_'+nr]=sel_xmin;
			data['xmax_'+nr]=sel_xmax;			
			data['ymin_'+nr]=sel_ymin;
			data['ymax_'+nr]=sel_ymax;
			//data['nr_'+nr]=nr;			
			data['text_xpos_'+nr]=text_xpos;
			data['text_ypos_'+nr]=text_ypos;		
			data['connector_direction_'+nr]=connector_direction;
			data['filename_'+nr]=filename;
			data['text_'+nr]=text;
			data['label_'+nr]=label;
			data['areatype_'+nr]=areatype;
			data['selectie_id_'+nr]=nr;

			if ((edit_annotation_flag==false) ) {  // nieuwe annotatie  
				num_annotaties=num_annotaties+1;
			}

		}


		data['num_annotaties']=num_annotaties;

		console.log(data);
			
		$.ajax({url:"/heatmap_subsel/"+dataset+'/', 
				type: "POST",
				'data':data,
				dataType:'json',
				success: handle_selection_ajax,
				error: handle_selection_ajax_error,
			});


		$('#overlay').css('visibility','hidden');
		edit_annotation_flag=false;
	}


	function cancel_selection () {	
		
		$('#overlay').css('visibility','hidden');
	}



function draw_legend (legend_labels, legend_colors) {

	var legend=d3.select('#legend');
	var opt=opties[0];
	var legend_x=55; // opties.multimap_numcols*opties.imgwidth+50;	

	for (var i=0; i<legend_labels.length; i++) {
		var txt=legend_labels[i][1];
		//console.log('LEGEND:',txt);
		legend.append("text")      // text label for the x axis
	    	.attr("id","legendtxt_"+i)
	    	.attr("class","title")
	        .attr("x", legend_x )
	        .attr("y", 18*i+15)
	        .attr("font-family", "Calibri")
	  		.attr("font-size", fontsize+"px")
	  		.attr("font-weight", "bold")
	        .style("text-anchor", "middle")
	        .text(txt);	  	
	    	    
	    legend.append ("rect")
	    	.attr("id","legend_r_"+i)
	    	.attr("x",legend_x-50)
	    	.attr("y",18*i+8)
			.attr("height",8)
			.attr("width",8)
			.attr("stroke",'#444')
			.attr("stroke-width",1)
			.attr("fill",legend_colors[i]);

		}
}



function heatmap (data, opties, nr) {
	this.skipzero=true;
	this.hist=null;
	this.histmax=0;


	/* storage */

	this.chart=null;
	this.backbuffer=null;
	this.backbuffer_cats=null;
	this.transposebuffer=null;
	this.transposebuffer_cats=null;
	this.imgData=null;
	this.mapdata=null;
	this.data=data;
	this.opties=opties;
	this.nr=nr;

	var _this = this;

	var xpix2img=parseInt(opties.imgwidth/opties.x_steps);
	var ypix2img=parseInt(opties.imgheight/opties.y_steps);



	this.init_databuffers =function (svg_el, canvas_el) {

		var opties=_this.opties;
		var imgwidth=opties.imgwidth;
		var imgheight=opties.imgheight;
		var c,s;

		//console.log('init_databuffers:', svg_el, canvas_el, imgwidth, imgheight);

		var c=document.getElementById(canvas_el);
	    c.setAttribute("width", imgwidth);
    	c.setAttribute("height", imgwidth);
    	_this.ctx = c.getContext('2d');
    	var s=document.getElementById(svg_el);
    	s.setAttribute("width", imgwidth*2+200);
    	s.setAttribute("height", imgheight+100);

		_this.chart = d3.select('#'+svg_el);

		// first, create a new ImageData to contain our pixels
		_this.imgData = _this.ctx.createImageData(imgwidth, imgheight); // width x height
		var transpose_size=opties.x_steps*opties.y_steps
		try {
		    _this.transposebuffer= new Float32Array  (transpose_size);
		    if (multimap){
		    	_this.transposebuffer_cats= new Float32Array  (transpose_size);
		    }
		    } catch(x){
		    _this.transposebuffer= new Array  (transpose_size);		//IE fallback
		    if (multimap){
		    	_this.transposebuffer_cats= new Array  (transpose_size);
		    }

		}

		var imgsize=imgwidth*imgheight;
		try {
		    _this.backbuffer= new Uint32Array  (imgsize);
		    if (multimap){
		    	_this.backbuffer_cats= new Uint32Array  (imgsize);
		    }
		    } catch(x){
		    _this.backbuffer= new Array  (imgsize);		//IE fallback
		    if (multimap){
		    	_this.backbuffer_cats= new Array  (imgsize);
		    }

		}
		_this.mapdata = _this.imgData.data;
	}



	this.update_minmax=function (minval,maxval) {

		//console.log('update_minmax:min/max:',minval,maxval );

		var opties=_this.opties;
		var gradient_node=document.getElementById("cg_a");
		var gradmax=gradient_node.getAttribute('gradient_max');
		var gradmin=gradient_node.getAttribute('gradient_min');
		var gradsteps=gradient_node.getAttribute('gradient_steps');


		if (gradmax=='max') {
			gradient_node.setAttribute('gradient_max_data', maxval);
			_this.grad_maxval=maxval;
		} else {
			if (gradient_node.hasAttribute('gradient_max_data')) {
				gradient_node.removeAttribute ('gradient_max_data');				
			}
			_this.grad_maxval=gradmax;
		}
		if (gradmin=='min') {
			gradient_node.setAttribute('gradient_min_data', minval);
			_this.grad_minval=minval;
		} else {
			if (gradient_node.hasAttribute('gradient_min_data')) {
				gradient_node.removeAttribute ('gradient_min_data');
			}
			_this.grad_minval=gradmin;
		}

		if (opties.missing_color=='min'){
			_this.missing_color=gradient_node.colormap[0];
		} else {
			_this.missing_color=opties.missing_color;
		}
		//console.log('missing_color:',_this.missing_color);
	}





	this.bin_data=function  () {

		//console.log("bin_data");
		var gradient_node=document.getElementById("cg_a");

		var opties=_this.opties;
		var log_min=gradient_node.getAttribute('log_min');

		var weighx=opties.weighx;
		var weighy=opties.weighy;
		var x_steps=opties.x_steps;
		var y_steps=opties.y_steps;
		var transform=gradient_node.getAttribute('transform');

		//console.log('bin_data:',x_steps, y_steps);
		//console.log('weighx/y:', weighx, weighy);
		var data=_this.data;

		var ptr2=0;
		var maxval=data[0];
		var minval=data[0];
		var xmean=_this.xmean;
		var ymean=_this.ymean;
		var sum_x=_this.sum_x;
		var sum_y=_this.sum_y;
		var transposebuffer=_this.transposebuffer;

		//console.log('xmean,ymean:\n', xmean, ymean, typeof(size))

		ptr=0;
		for (var i=0; i<y_steps; i++) {
			for (var j=0; j<x_steps;  j++) {
				val=0;
				ptr=j*y_steps+i;
				val=data[ptr];
				if (val>maxval) maxval=val;
				if (val<minval) minval=val;
				val=transform_value(val,transform, log_min);

				if (weighx) {
					val=(val/sum_x[j])*xmean;
				}
				if (weighy) {
					val=(val/sum_y[i])*ymean;
				}
				transposebuffer[ptr2]=val;
				ptr2++;
				ptr++;
			} //j
	//		console.log("i:",i);
		}	//i

		_this.update_minmax(minval, maxval);
	}




	this.spread_bins=function  () {

		var opties=_this.opties;
		var totalpixels=opties.x_steps*opties.y_steps;
		var gradient_node=document.getElementById("cg_a");
		var gradsteps=gradient_node.getAttribute('gradient_steps');
		var transform=gradient_node.getAttribute('transform');
		var log_min=gradient_node.getAttribute('log_min');
		var inv_grad=gradient_node.getAttribute('gradient_invert')=='true';
		var imgheight=opties.imgheight;
		var imgwidth=opties.imgwidth;
		var size=1; //gradient_node.size;

		var histmax=_this.histmax;
		var transposebuffer=_this.transposebuffer;
		var transposebuffer_cats=_this.transposebuffer_cats;
		var backbuffer=_this.backbuffer;
		var backbuffer_cats=_this.backbuffer_cats;

/*
		if (gradient_node.hasAttribute('gradient_max_data')) {
			var gradmax=gradient_node.getAttribute('gradient_max_data');
		} else {
			var gradmax=gradient_node.getAttribute('gradient_max');
		}
		if (gradient_node.hasAttribute('gradient_min_data')) {
			var gradmin=gradient_node.getAttribute('gradient_min_data');
		} else {
			var gradmin=gradient_node.getAttribute('gradient_min');
		}
*/

		gradmin=_this.grad_minval;
		gradmax=_this.grad_maxval;
		// console.log('spread_bins: transform, gradmin/gradmax',transform, gradmin,gradmax);
		var gradmax=transform_value(gradmax,transform, log_min);
		var gradmin=transform_value(gradmin,transform, log_min);

		var delta=gradmax-gradmin;
		//console.log('spread_bins, gradmin/gradmax, multimap',gradmin,gradmax,multimap);


		var line=0;
		for (i=0; i<opties.imgwidth*opties.imgheight; i++) {
			backbuffer[i]=0;
		}
		xstep=xpix2img*size;
		ystep=ypix2img*size;
		//console.log('xstep, ystep',xstep,ystep);

		u=0;
		v=1;
		//console.log('xstep/ystep:',xstep,ystep, xpix2img, ypix2img, size);
		_this.hist=new Array(gradsteps);
		var hist=_this.hist;
		for (i=0; i<gradsteps; i++) {
			hist[i]=0;
		}
		//console.log('totalpixels,ptr:',totalpixels, opties.imgheight, opties.imgwidth);

		//console.log('val2index:',gradmin, delta,gradsteps);

		j=0;


		for (i=0; i<totalpixels; i++)	{
			val=transposebuffer[i];
			/*
			if ((val!=0) && (j<50)) {
				console.log("%d", val);
				j++;
			}
			*/

			indexval=~~((val-gradmin)/(delta)*gradsteps);
			if (indexval<0) indexval=0;
			if (indexval>=gradsteps) indexval=gradsteps-1;

			indexval=parseInt(indexval);
			hist[indexval]++;
			/*
			if ((inv_grad)  && (indexval!=0)) {
					indexval=colormaplength-indexval;
			}
			*/

			ptr=(imgheight-v*ystep)*imgwidth;
			ptr+=u*xstep;


			//if (line==0) { console.log("val=",val);}
			//ptr=u*xstep+v*ystep*imgwidth;
			for (cy=0; cy<ystep; cy++) {
				for (cx=0; cx<xstep; cx++) {
					backbuffer[ptr+cy*imgwidth+cx]=indexval;
					}
				}
			u++;
			line+=xstep;
			if (line>=imgwidth) {
				u=0;
				v++;
				line=0;
			}
		} // for i
		u=0;
		v=1;

		if (multimap) {
			var cat =null;
			var nr=0;
			//console.log('multimap');
			for (i=0; i<totalpixels; i++)	{
				cat=transposebuffer_cats[i];
				nr+=1;
				ptr=(imgheight-v*ystep)*imgwidth;
				ptr+=u*xstep;
				for (cy=0; cy<ystep; cy++) {
					for (cx=0; cx<xstep; cx++) {
						backbuffer_cats[ptr+cy*imgwidth+cx]=cat;
					}
				}
				u++;
				line+=xstep;
				if (line>=imgwidth) {
					u=0;
					v++;
					line=0;
				}
			}  // for i
		} // multimap
	//console.log('HISTMAX:',hist)
	histmax=hist[0];
	for (i=1; i<gradsteps; i++)
		if (hist[i]>histmax) histmax=hist[i];

	_this.histmax=histmax;
	//console.log(hist);

	//console.log('hist2:',backbuffer);
	}



	/* draw_heatmap:
		- heatmap uitrekenen
		- minima/maxima bepalen
	   - colormap tekenen;
	   - heatmap tekenen.

	*/

	this.draw_heatmap=function () {

		console.log("draw_heatmap:");
	//	console.trace();

		var opties=_this.opties;
		if (opties.displaymode=='dotplot') {
			_this.draw_dotplot();
		}
		if (opties.displaymode=='text') {
			_this.draw_text();
		}

		if ((opties.diplaymode=='text')  && (opties.text_show_background==false)) return;

		_this.spread_bins();	


		var mapdata=_this.mapdata;
		var backbuffer=_this.backbuffer;
		var backbuffer_cats=_this.backbuffer_cats;

		/* eigenlijke heatmap plotten */

		var indexval=0;
		var color=[];
		var nr=0;

	//	$('.dot').remove();		//remove dotplot
		var opties=_this.opties;
		var gradient_node=document.getElementById("cg_a");
		var size=gradient_node.size;
		//console.log('draw_heatmap, size:',size);
		var xstep=xpix2img*size;
		var ystep=ypix2img*size;

		if (_this.colormap==undefined) {
			var colormap=gradient_node.colormap;
		} else {
			var colormap=_this.colormap;
		}
		var imgwidth=opties.imgwidth;
		var imgheight=opties.imgheight;
		var mean_x=_this.mean_x;
		var median_x=_this.median_x;
		var extradata=_this.extradata;
		var cat=null;

	//	console.log('draw_heatmap, colormap:', colormap);

	//	console.log("draw_heatmap:",backbuffer.length);
		for (i=0,j=0; i<backbuffer.length; i++,j+=4) {
				indexval=backbuffer[i];
				/*
				if ((indexval>0) && (nr<50)) {
							console.log(nr, i,j,indexval);
							nr+=1;
						}
				*/

				if ((indexval!=0) || (!_this.skipzero)) {	  // waardes die 0 zijn niet plotten					
						color=colormap[indexval];
		    			mapdata[j] =  color[0];
			    		mapdata[j+1] = color[1];
			    		mapdata[j+2] = color[2];
			    		mapdata[j+3] = 0xff;
		    		
				} else {
					color=_this.missing_color;
					mapdata[j] =  color[0]; 
		    		mapdata[j+1] = color[1]; 
		    		mapdata[j+2] = color[2]; 
		    		mapdata[j+3] = color[3];
		    	}

			}
		if (opties['plot_mean']==true){
			var maxx=_this.opties.x_max;
			var minx=_this.opties.x_min;
			var maxy=_this.opties.y_max;
			var miny=_this.opties.y_min;


			var meanScaleX=d3.scale.linear();
			meanScaleX.domain([minx,maxx]);
			meanScaleX.range([75,imgwidth+75]);

			var meanScaleY=d3.scale.linear();
			meanScaleY.domain([miny,maxy]);
			meanScaleY.range([25+imgheight,25]);
			var chart=_this.chart;

			var lineFunction = d3.svg.line()
                       		    .x(function(d) { x=meanScaleX(d.x);  console.log('x=',x); return x; })
                           		.y(function(d) { y=meanScaleY(d.y);  console.log('y=',y); return y; })
                          		.interpolate("linear");
            lineData=[];
			for (i=0; i<mean_x.length; i++) {				
				step=(maxx-minx)/mean_x.length;
				xval=minx+step*i;
				lineData.push({x:xval, y:mean_x[i]})
			}

			var lineGraph = chart.append("path")
							.attr("id","plot_mean")
							.attr("class","extrainfo")
                            .attr("d", lineFunction(lineData))
                            .attr("stroke", "blue")
                            .attr("stroke-width", 2)
                            .attr("fill", "none");
		}
		if (opties['plot_median']==true){
			var maxx=_this.opties.x_max;
			var minx=_this.opties.x_min;
			var maxy=_this.opties.y_max;
			var miny=_this.opties.y_min;


			var medianScaleX=d3.scale.linear();
			medianScaleX.domain([minx,maxx]);
			medianScaleX.range([75,imgwidth+75]);

			var medianScaleY=d3.scale.linear();
			medianScaleY.domain([miny,maxy]);
			medianScaleY.range([25+imgheight,25]);
			var chart=_this.chart;



			var lineFunction = d3.svg.line()
                       		    .x(function(d) { x=medianScaleX(d.x);  console.log('x=',x); return x; })
                           		.y(function(d) { y=medianScaleY(d.y);  console.log('y=',y); return y; })
                          		.interpolate("linear");
            lineData=[];
			for (i=0; i<median_x.length; i++) {				
				step=(maxx-minx)/median_x.length;
				xval=minx+step*i;
				lineData.push({x:xval, y:median_x[i]})
			}

			var lineGraph = chart.append("path")
							.attr("id","plot_median")
							.attr("class","extrainfo")
                            .attr("d", lineFunction(lineData))
                            .attr("stroke", "blue")
                            .attr("stroke-width", 2)
                            .attr("fill", "none");
		}

		info_datafile=opties['info_datafile'];
		if ((info_datafile!=null) && (info_datafile!='')) {
			color=opties['info_color'];
			console.log(linedata);
			for (var i=0; i<linedata.length; i++) {
				u=linedata[i][0];
				v=linedata[i][1];
				var ptr=(u*size+size*imgwidth*(imgheight-v))*4;
				mapdata[ptr]=color[0];
				mapdata[ptr+1]=color[1];
				mapdata[ptr+2]=color[2];
				mapdata[ptr+3]=color[3];
			}

			var chart=_this.chart;
			var maxx=_this.opties.x_max;
			var minx=_this.opties.x_min;			

			var lineScaleX=d3.scale.linear();
			lineScaleX.domain([0,imgwidth]);
			lineScaleX.range([75,imgwidth+75]);

			var lineScaleY=d3.scale.linear();
			lineScaleY.domain([0,imgheight]);
			lineScaleY.range([25+imgheight,25]);


			var lineFunction = d3.svg.line()
                       		    .x(function(d) { x=lineScaleX(d.x);  return x; })
                           		.y(function(d) { y=lineScaleY(d.y);   return y; })
                          		.interpolate("linear");
            lineData=[];
			for (i=0; i<mean_x.length; i++) {				
				lineData.push({x:linedata[i][0], y:linedata[i][1]})
			}

			var lineGraph = chart.append("path")
							.attr("id","plot_median")
							.attr("class","extrainfo")
                            .attr("d", lineFunction(lineData))
                            .attr("stroke", "blue")
                            .attr("stroke-width", 2)
                            .attr("fill", "none");


		}
		//console.log('putdata');
		_this.ctx.putImageData(_this.imgData, 0, 0);
	}



  




	export_ok=function  () {
		console.log("export ok");
	}
	export_fail=function  () {
		console.log("export failed");
	}
	

	print_ok=function  () {
		console.log("print ok");
	}

	print_fail=function  () {
		console.log("print failed");

	}

	this.click_print=function  () {


		console.log('click_print');		
		//$.get('#',{'cmd':printtype})
	 	$.ajax({url:this.href,
	            cache: false,
	            url: '#',
	            type: "POST",
	            data: {'print':true}           
	        })
	 		.done(print_ok)
	 		.fail(print_fail);

	}

	this.click_export=function  () {


		console.log('export_html');		
		//$.get('#',{'cmd':printtype})
	 	$.ajax({url:this.href,
	            cache: false,
	            url: '#',
	            type: "POST",
	            data: {'export':true}           
	        })
	 		.done(export_ok)
	 		.fail(export_fail);

	}









	  this.draw_axes=function  () {

	  console.log('draw_axes');
	  var opties=_this.opties;
	  var x_log=opties.x_log;
	  var y_log=opties.y_log;

	  var x_data_type=opties.x_data_type;
	  var y_data_type=opties.y_data_type;

	  var numticks=opties['numticks']
	  var xmin=opties.x_min;
	  var ymin=opties.y_min;
	  var ymax=opties.y_max+1;   // off by one, again.
	  var xmax=opties.x_max+1;
	  if (opties.x_relative) {
	  	xmin=opties.x_relative_min;
	  	xmax=opties.x_relative_max;
	  }
	  if (opties.y_relative) {
	  	ymin=opties.y_relative_min;
	  	ymax=opties.y_relative_max;
	  }


	  var imgwidth=opties.imgwidth;
	  var imgheight=opties.imgheight;
	  if ((x_log) && (xmin<=0)) xmin=1;
	  if ((y_log) && (ymin<=0)) ymin=1;

	  if (x_log) {
	  		xScale=d3.scale.log();     // naar object-namespace
	  		xScale.domain([xmin,xmax]);
	  	}
	  else {
	  		if (x_data_type=='nominal')	{
	  				xScale=d3.scale.linear();
	  				xScale.domain([xmin,xmax]);
	  				var x_data_type_simple='nominal';
	  			}
	  		if ((x_data_type=='date_year' ) || (x_data_type=='date_quarter') || (x_data_type=='date_month') || (x_data_type=='date_week') || (x_data_type=='date_day')) 	{
	  				xScale=d3.time.scale();
	  				opties.x_mindate=new Date(opties.x_min);
	  				opties.x_maxdate=new Date(opties.x_max);
	  				xScale.domain([opties.x_mindate,opties.x_maxdate]);
	  				//console.log(opties.x_mindate,opties.x_maxdate);
	  				var x_data_type_simple='date';
	  			}
	  	    }


	  if (y_log) {
	  		yScale=d3.scale.log();
	  		yScale.domain([ymax,ymin]);
	  	}
	  else	 {
	  		if (y_data_type=='nominal')	{
	  				yScale=d3.scale.linear();
	  				yScale.domain([ymax,ymin]);
	  				var y_data_type_simple='nominal';
	  			}
	  		if ((y_data_type=='date_year' ) || (y_data_type=='date_quarter') || (y_data_type=='date_month') || (y_data_type=='date_week') || (y_data_type=='date_day')) 	{
	  				opties.y_mindate=new Date(opties.y_min);
	  				opties.y_maxdate=new Date(opties.y_max);
	  				yScale=d3.time.scale();
	  				yScale.domain([opties.y_mindate,opties.y_maxdate]);
	  				//console.log(opties.y_mindate,opties.y_maxdate);
	  				var y_data_type_simple='date';
	  			}
	  	    }


	  xScale.range([0,imgwidth]);
	  yScale.range([0,imgheight]);
 	  _this.xScale=xScale;
	  _this.yScale=yScale;


	  var xAxis=d3.svg.axis();
	  var yAxis=d3.svg.axis();	



	  xAxis.scale(xScale)	  	
	        .orient("bottom");
	  if ((x_data_type=='nominal') && (!x_log)) {
	  	if ((xmax-xmin)>500) {
			xAxis.tickFormat(d3.format(" s"));
		} else {
			xAxis.tickFormat(d3.format(" d"));
		}	  	
	  }
	  if (x_data_type=='date_year') {
	  	xAxis.tickFormat(d3.time.format('%Y'));	
	  }
	  if (x_data_type=='date_month') {
	  	xAxis.tickFormat(d3.time.format('%b %Y'));	
	  }
	  if (x_data_type=='date_week') {
	  	xAxis.tickFormat(d3.time.format('%e %b %Y'));	
	  }
	  if (x_data_type=='date_day') {
	  	xAxis.tickFormat(d3.time.format('%e %b %Y'));	
	  }


	  yAxis.scale(yScale)	  		
	        .orient("left");
	  if ((y_data_type=='nominal') && (!y_log)) {	  
		if ((ymax-ymin)>500) {
			yAxis.tickFormat(d3.format(" s"));
		} else {
			yAxis.tickFormat(d3.format(" d"));
		}
	  }
	  if (y_data_type=='date_year') {
	  	yAxis.tickFormat(d3.time.format('%Y'));	
	  }
	  if (y_data_type=='date_month') {
	  	yAxis.tickFormat(d3.time.format('%b %Y'));	
	  }
	  if (y_data_type=='date_week') {
	  	yAxis.tickFormat(d3.time.format('%e %b %Y'));	
	  }
	  if (y_data_type=='date_day') {
	  	yAxis.tickFormat(d3.time.format('%e %b %Y'));	
	  }


	  if ( ((multimap) && (smallsize==true))  || (numticks==parseInt(numticks))) {
	  		numticks=4;
	  		xAxis.ticks(numticks)
	  	  	yAxis.ticks(numticks)
	  }
	  console.log('NUMTICKS:',numticks)

	  fontsize=opties['fontsize'];

	  //console.log(chart);
	  var chart=_this.chart;

		chart.append("rect")
			.attr("id",'dragrect_'+_this.nr)
			.attr("x",0)
			.attr("y",0)
			.attr("height",0)
			.attr("width",0)
			.attr("stroke",'black')
			.attr("stroke-width",1)
			.attr("fill","none");

	  chart.append("g")
	  		.attr("id","xaxis_"+_this.nr)
	        .attr("class","xaxis mainx xaxis_" + _this.nr)
	        .attr("transform","translate(75,"+(imgheight+25)+")")
	        .attr('font-size','32px')
	        .call(xAxis);

	  chart.append("g")
	  		.attr("id","yaxis_"+_this.nr)
	        .attr("class","yaxis mainy yaxis_"+_this.nr)
	        .attr("transform","translate(75,25)")
	        .call(yAxis);

	  chart.selectAll(".tick >text")
	  		.attr("font-family", "Calibri")
	  		.attr("font-weight", "normal")
	  		.attr('font-size',fontsize+'px');

	  var xlabeloffset=0;
	  if (x_data_type_simple=='date') {
	  	chart.selectAll(".mainx")
	  			.selectAll(".tick >text")
	  			.attr("transform", "translate(-10,0)rotate(-45)")	  			
	  			.style("text-anchor", "end");
		xlabeloffset=8;
	  	}
	  	chart.selectAll(".mainx")
	  			.selectAll(".tick >text")
	  			.attr("class","xticks_"+this.nr);
		chart.selectAll(".mainy")
	  			.selectAll(".tick >text")
	  			.attr("class","yticks_"+this.nr);
		


	  chart.append("text")      // text label for the x axis	  		
	  		.attr("class","xaxis xlabel_"+_this.nr)
	        .attr("x", imgwidth/2+70 )
	        .attr("y",  imgheight+70 )

	        .style("text-anchor", "middle")
	        .attr("font-family", "Corbel")
	  		.attr("font-size", fontsize+"px")
	  		 .attr("transform","translate(0,"+(fontsize-15)+xlabeloffset+")")
	  		.attr("font-weight", "bold")
	        .text(opties.x_label);
	  chart.append("text")      // text label for the x axis
	    	.attr("class","yaxis ylabel_"+_this.nr)
	        .attr("x", 0 )
	        .attr("y", 0)
	        .attr("font-family", "Calibri")
	  		.attr("font-size", fontsize+"px")
	  		.attr("font-weight", "bold")
	        .attr("transform","translate(20,"+(imgheight/2)+")rotate(270)")
	        .style("text-anchor", "middle")
	        .text(opties.y_label);

	  var title=opties.title;
	  if (multimap) {
	  	title=opties.multimap_title;
	  }
	  chart.append("text")      // text label for the x axis
	    	.attr("id","title_"+_this.nr)
	    	.attr("class","title")
	        .attr("x", imgwidth/2+70 )
	        .attr("y", 15)
	        .attr("font-family", "Calibri")
	  		.attr("font-size", fontsize+"px")
	  		.attr("font-weight", "bold")
	        .style("text-anchor", "middle")
	        .text(title);
	        /*
	  if (y_data_type_simple=='date') {
	  	chart.selectAll(".mainy")
	  			.selectAll(".tick >text")
	  			.attr("transform", "translate(-10,0)rotate(-45)")
	  			.style("text-anchor", "end");
		ylabeloffset=8;
	  	}
	  	*/


	  		/* legenda voor multimap */

	}







	this.draw_text=function  () {

		//console.log('draw text');
		var opties=_this.opties;
		var chart=_this.chart;
			var xmin=opties.x_min;
			var xmax=opties.x_max+1;
			var ymin=opties.y_min;
			var ymax=opties.y_max+1;
			var x_steps=opties.x_steps;
			var y_steps=opties.y_steps;
			var transform=opties.transform;

	    	var dx=(xmax-xmin)/(x_steps);
	    	var dy=(ymax-ymin)/(y_steps);


		//console.log('start text, size', size);
		var xoffset=0.5*dx;
		var yoffset=0.5*dy;
		for (i=0; i<x_steps; i++){
			for (j=0; j<y_steps; j++){
				ptr=y_steps*j+i;
				val=_this.transposebuffer[ptr];

				if (val<0) val=-val;
				xval=i*dx+xmin+xoffset;
				yval=(y_steps-j-1)*dy+ymin+yoffset
				for (k=0; k<val; k++) {
					chart.append("svg:text")
						.attr("class","txt")
	          			.attr("x", function (d,i) { return xScale(xval); } )
	          			.attr("y", function (d) { return xScale(yval); } )
	          			.attr("transform","translate(75,25)")
	          			.text(function(d) { return val; });
	          		}


			}
		}

	   chart.selectAll(".txt")
        .attr("font-family", "Calibri")
        .attr("font-weight", "normal")
        .attr('font-size',fontsize+'px');
        if (opties.text_show_background==false) {
			$('.heatmap_canvas').hide();
		} else {
			$('.heatmap_canvas').show();
		}
	}

		// dotplot starts here


	this.draw_dotplot=function  () {


		var opties=_this.opties;
		if (opties.displaymode=='dotplot') {
			$('.dot').remove();
			$('.dot_grid').remove();

			var chart=_this.chart;
			var xmin=opties.x_min;
			var xmax=opties.x_max+1;
			var ymin=opties.y_min;
			var ymax=opties.y_max+1;
			var x_steps=opties.x_steps;
			var y_steps=opties.y_steps;
			var transform=opties.transform;

	    	var dx=(xmax-xmin)/(x_steps);
	    	var dy=(ymax-ymin)/(y_steps);



			//console.log('draw_dotplot',xmin, xmax, x_steps, dx,dy);

			var dot_dotsize=opties.dot_dotsize;
			var dot_boxsize=opties.dot_boxsize;

			var dot_color=opties.dot_color;
			var use_gradient=opties.dot_use_gradient;
			var bimodal=opties.gradient_bimodal;
			var gradient_node=document.getElementById("cg_a");
			if (use_gradient) {

				if (gradient_node.hasAttribute('gradient_max_data')) {
					var gradmax=gradient_node.getAttribute('gradient_max_data');
				} else {
					var gradmax=gradient_node.getAttribute('gradient_max');
				}
				if (gradient_node.hasAttribute('gradient_min_data')) {
					var gradmin=gradient_node.getAttribute('gradient_min_data');
				} else {
					var gradmin=gradient_node.getAttribute('gradient_min');
				}

				var gradcenter=gradient_node.getAttribute('gradient_center');
				var log_min=gradient_node.getAttribute('log_min');
				var gradmax=transform_value(gradmax,transform,log_min);
				var gradcenter=transform_value(gradcenter,transform, log_min);
				var gradmin=transform_value(gradmin,transform, log_min);
				var gradsteps=gradient_node.getAttribute('gradient_steps');

				if (bimodal) {
					var delta=gradmax-gradcenter;
					var delta2=gradcenter-gradmin;
					var colormap=gradient_node.colormap;
					var colormap2=gradient_node.colormap2;
					//console.log('bimodal:',delta,delta2,colormap,colormap2)
				} else {
					var delta=gradmax-gradmin;
					var colormap=gradient_node.colormap;
				}
				var color='';
			}


			var size=gradient_node.size
			//console.log('start dotplot, size', size);
			var xoffset=0.5*dx-0.5*dot_boxsize*dx;
			var yoffset=0.5*dy-0.5*dot_boxsize*dy;
			for (i=0; i<x_steps; i++){
				for (j=0; j<y_steps; j++){
					ptr=y_steps*j+i;
					val=_this.transposebuffer[ptr];
					if (use_gradient) {
			//			console.log(val);
			//			console.log(colormap[val]);

						//console.log('setval:',bimodal,val,gradmin,gradcenter,gradmax);
						if (bimodal) {
							if (val>gradcenter) {
								indexval=~~((val-gradcenter)/(delta)*gradsteps);
								if (indexval<0) indexval=0;
								if (indexval>=gradsteps) indexval=gradsteps-1;
								//console.log('take1:',indexval);
								color=colormap[indexval];
							} else {
								indexval=~~((val-gradmin)/(delta2)*gradsteps);
								//console.log('take2:',indexval);
								if (indexval<0) indexval=0;
								if (indexval>=gradsteps) indexval=gradsteps-1;
								color=colormap2[indexval];
							}
						} else {
							indexval=~~((val-gradmin)/(delta)*gradsteps);
							if (indexval<0) indexval=0;
							if (indexval>=gradsteps) indexval=gradsteps-1;
							color=colormap[indexval];
						}
						dot_color="rgb("+color[0]+","+color[1]+","+color[2]+")";
					}
					if (val<0) val=-val;
					xval=i*dx+xmin+xoffset;
					yval=(y_steps-j-1)*dy+ymin+yoffset
					for (k=0; k<val; k++) {
						chart.append("svg:circle")
							.attr("class","dot")
		          			.attr("cx", function (d,i) { return xScale(xval+dot_boxsize*dx*Math.random()); } )
		          			.attr("cy", function (d) { return xScale(yval+dot_boxsize*dy*Math.random()); } )
		          			.attr("transform","translate(75,25)")
		          			.attr("r", dot_dotsize)
		          			.style("fill",dot_color);
		          		}

				}
			}
	   	}

	var xoffset=0.5*dx;
	var yoffset=0.5*dy;
	var gridcolor='rgb(90,90,90)';
	for (i=1; i<x_steps; i++){
		xval=i*dx+xmin+xoffset;
		chart.append("svg:line")
			.attr('class','dot_grid')
			.attr('stroke-width',0.25)
			.attr('stroke',gridcolor)
			.attr("x1", xScale(xval))
            .attr("y1", yScale(ymin-dy+yoffset))
            .attr("x2", xScale(xval))
            .attr("y2", yScale(ymax-dy+yoffset));
		}
	for (j=0; j<y_steps; j++){
		yval=(y_steps-j-1)*dy+ymin+yoffset;
		chart.append("svg:line")
			.attr('class','dot_grid')
			.attr('stroke-width',0.25)
			.attr('stroke',gridcolor)
			.attr("x1", xScale(xmin+dx+xoffset))
            .attr("y1", yScale(yval))
            .attr("x2", xScale(xmax+dx+xoffset))
            .attr("y2", yScale(yval));
		}


	   	  	// dotplot done
	   	console.log('dotplot done');
	}





	this.world_to_x=function (x) {
		var opties=_this.opties;
		var imgwidth=opties.imgwidth;
		var xmax=opties.x_max; //+1;
		var xmin=opties.x_min;
		var delta=(xmax-xmin);
		//var val=((x-75)/imgwidth)*delta+xmin;

		var val=((x-xmin)/delta)*imgwidth+75;

		return val;
	}

	this.world_to_y=function (y) {
		var opties=_this.opties;
		var imgheight=opties.imgheight;
		var ymax=opties.y_max;//+1;   // off by one, again.
		var ymin=opties.y_min;
		var delta=(ymax-ymin);
		//var val=(((imgheight-y)+25)/imgheight)*delta+ymin;

		var val=imgheight-((y-ymin)/delta*imgheight)+25;
		//console.log('y,val:',y,val);
		return val;
	}


	this.x_to_world=function (x) {
		var opties=_this.opties;
		var imgwidth=opties.imgwidth;
		var xmax=opties.x_max+1;
		var xmin=opties.x_min;
		var delta=(xmax-xmin);
		//var val=((x-75)/imgwidth)*delta+xmin;
		var val=(x/imgwidth)*delta+xmin;
		return val;
	}

	this.y_to_world=function (y) {
		var opties=_this.opties;
		var imgheight=opties.imgheight;
		var ymax=opties.y_max+1;   // off by one, again.
		var ymin=opties.y_min;
		var delta=(ymax-ymin);
		var val=((imgheight-y)/imgheight)*delta+ymin;		

		return val;
	}


	this.update_hist_x_y=function  (evt) {



		//console.clear();
		console.log("update_hist_x_y");
		_this.dragging=false;

		var opties=_this.opties;
		var chart=_this.chart;

		var ymax=opties.y_max+1;   // off by one, again.
		var ymin=opties.y_min;
		var xmax=opties.x_max+1;
		var xmin=opties.x_min;

		var gradient_node=document.getElementById("cg_a");
		var gradmax=gradient_node.getAttribute('gradient_max');
		var gradmin=gradient_node.getAttribute('gradient_min');
		var gradsteps=gradient_node.getAttribute('gradient_steps');
		var inv_grad=gradient_node.getAttribute('gradient_invert')=='true';
		if (gradient_node.hasAttribute('gradient_max_data')) {
			var gradmax=gradient_node.getAttribute('gradient_max_data');
		}
		if (gradient_node.hasAttribute('gradient_min_data')) {
			var gradmin=gradient_node.getAttribute('gradient_min_data');
		}
		var imgheight=opties.imgheight;
		var imgwidth=opties.imgwidth;
		var transposebuffer=_this.transposebuffer;
		var backbuffer=_this.backbuffer;
		var colormap=gradient_node.colormap;

		if (annotations_show) {				// select ongedaan  maken.
			if (selected_annotation!=undefined) {
				$('#annotation_obj_'+selected_annotation).attr('class','annotation annotation_obj');
			}
			$('.annotation_label').show();
			$('.annotation_text').hide();
			$('.annotation_obj').show();
			$('.annotation_connector').show();
		}


		var xoffset=75;
		var yoffset=25;

		x=parseInt(evt.pageX-$(this).position().left)-xoffset;
		y=parseInt(evt.pageY-$(this).position().top)-yoffset;
		console.log('x,y:',x, y);
		
		
		if ((x<0) || (y<0) || (x>imgwidth) || (y>imgheight)) {
			console.log ('exit: x,y',x,y);
			return false;
		}

		$('.hist_x').remove();
		$('.hist_y').remove();
		$('.pointinfotext').remove();

		var offsetx_hist=125;  //distance between heatmap and side-histograms
		var offsety_hist=25;   // distance between bottom of screen & side-histograms
		var offsetspace_hist=-40;   // distance between side-histograms
		var graphheight=0.25*imgheight;

		var xval=_this.x_to_world(x);
		var yval=_this.y_to_world(y);

		var deltax=(xmax-xmin)/opties.x_steps;
		var deltay=(ymax-ymin)/opties.y_steps;
		var x_val=parseInt(Math.floor((xval-xmin)/deltax) * deltax + xmin);
		var y_val=parseInt(Math.floor((yval-ymin)/deltay) * deltay + ymin);

		console.log('x,y',xval, yval)
		
		console.log('x**',(xval-xmin), (xval-xmin)/deltax, Math.floor((xval-xmin)/deltax))
		console.log('x_,y_',x_val, y_val)

		/* text upper right corner */

		/*
	 	chart.append("text")
	    	.attr("class","pointinfotext")
	        .attr("x", 1.5*imgwidth+100 )
	        .attr("y", 50 )
	        .attr("font-family", "Corbel")
	        .attr("font-size", "15px")
	        .attr("font-weight", "bold")
	        .text(opties.x_label+':'+xval);

	    
		yval=yval.toFixed(0);
		chart.append("text")
	    	.attr("class","pointinfotext")
	        .attr("x", 1.5*imgwidth+100 )
	        .attr("y", 50+16)
	        .attr("font-family", "Corbel")
	        .attr("font-size", "15px")
	        .attr("font-weight", "bold")
	        .text(opties.y_label+':'+yval);

		val=transposebuffer[(imgheight-y)/size*imgwidth+x/size];
		chart.append("text")
	    	.attr("class","pointinfotext")
	        .attr("x", 1.5*imgwidth+100 )
	        .attr("y", 50+32)
	        .attr("font-family", "Corbel")
	        .attr("font-size", "15px")
	        .attr("font-weight", "bold")
	        .text('#count:'+val);  */



	/* histogram y */

	

		histy_max=0;
		for (i=0; i<imgwidth-1; i++) {
			val=backbuffer[y*imgheight+i];	
			//console.log('x:',y*imgwidth+i, val);		
			if (val>histy_max) histy_max=val;		
		}
		

		for (i=0; i<imgwidth-1; i++) {
		 	val=backbuffer[y*imgheight+i];
		//	console.log('x,y:', imgwidth+offsetx_hist+i, parseInt(imgheight-(val/histy_max)*graphheight)+offsety_hist );
		 	color=colormap[val];
		 	if (histy_max==0)  {
		 		bin_height=0;
		 		height=0;
		 	} else {
		 		bin_height=parseInt(imgheight-(val/histy_max)*graphheight)+offsety_hist;
		 		height=(val/histy_max)*graphheight;
		 	}		 	

			chart.append("rect")
				.attr("class","hist_y")
				.attr("x",imgwidth+offsetx_hist+i)
				.attr("y",bin_height)
				.attr("width",1)
				.attr("height",height)
				.style("fill","rgb(8,8,0)")
				.style("stroke","rgb(8,8,0)")
				//.style("fill","rgb("+color[0]+","+color[1]+","+color[2]+")")
				//.style("stroke","rgb("+color[0]+","+color[1]+","+color[2]+")")
				.style("stroke-width","1px");
			 }


	histx_max=0;
	for (i=0; i<imgheight-1; i++) {
		 	val=backbuffer[i*imgwidth+x];	
//		 	console.log('y:',i*imgwidth+x, val);	 	
		 	if (val>histx_max) histx_max=val;
		 }


// histogram x

	for (i=0; i<imgheight-1; i++) {
		 	val=backbuffer[i*imgwidth+x];
		 	if (histx_max==0)  {
		 		bin_height=0;
		 		height=0;
		 	} else {
		 		bin_height=parseInt(imgheight-(val/histx_max)*graphheight-graphheight+offsety_hist+offsetspace_hist);
		 		height=(val/histx_max)*graphheight;
		 	}		 	

		 	color=colormap[val];
			chart.append("rect")
				.attr("class","hist_y")
				.attr("x",2*imgwidth+offsetx_hist-i)
				.attr("y",bin_height)
				.attr("width",1)
				.attr("height",height)
				.style("fill","rgb(130,8,8)")
				.style("stroke","rgb(130,8,8)")
				.style("stroke-width","1px");
			 }



	  var xxScale=d3.scale.linear();
	  var yxScale=d3.scale.linear();
	  var xyScale=d3.scale.linear();
	  var yyScale=d3.scale.linear();

	  xxScale.range([0,imgwidth]);
	  xxScale.domain([ymin,ymax]);       // bug: what's called 'xscale'/'yscale' is on the wrong position
	  xyScale.range([0,0.25*imgheight]);
	  xyScale.domain([histy_max*(gradmax/gradsteps),0]);       // bug: what's called 'xscale'/'yscale' is on the wrong position

	  yxScale.range([0,imgwidth]);
	  yxScale.domain([xmin,xmax]);
	  yyScale.range([0,0.25*imgheight]);
	  yyScale.domain([histx_max*(gradmax/gradsteps),0]);

	  var xxAxis=d3.svg.axis();
	  var xyAxis=d3.svg.axis();
	  var yxAxis=d3.svg.axis();
	  var yyAxis=d3.svg.axis();

	  xxAxis.scale(xxScale)
	       .orient("bottom");
	  xyAxis.scale(xyScale)
	       .orient("left");
	  yxAxis.scale(yxScale)
	       .orient("bottom");
	  yyAxis.scale(yyScale)
	       .orient("left");

	  //console.log(chart);
	  offsetx=imgwidth+offsetx_hist;
	  offsetyx=imgheight+offsety_hist
	  offsetyy=imgheight-2*graphheight+offsety_hist+offsetspace_hist;

	  chart.append("g")
	        .attr("class","yaxis hist_x")
	        .attr("transform","translate("+offsetx+","+offsetyx+")")
	        .call(yxAxis);
	  chart.append("g")
	        .attr("class","yaxis hist_x")
	        .attr("transform","translate("+offsetx+","+offsetyy+")")
	        .call(yyAxis);

	  offsetx=imgwidth+offsetx_hist;
	  offsetyx=imgheight-graphheight+offsety_hist+offsetspace_hist;
	  offsetyy=imgheight-graphheight+offsety_hist;

	  chart.append("g")
	        .attr("class","xaxis hist_y")
	        .attr("transform","translate("+offsetx+","+offsetyx+")")
	        .call(xxAxis);
	  chart.append("g")
	        .attr("class","xaxis hist_y")
	        .attr("transform","translate("+offsetx+","+offsetyy+")")
	        .call(xyAxis);

	  chart.selectAll('.hist_x >text')
	        .attr("font-family", "Corbel")
	  		.attr("font-size", "16px")
	  		.attr("font-weight", "normal");

	  chart.selectAll('.hist_y')
	  		.selectAll('.tick >text')
	        .attr("font-family", "Corbel")
	  		.attr("font-size", "16px")
	  		.attr("font-weight", "normal");

	  chart.selectAll('.hist_x')
	  		.selectAll('.tick >text')
	        .attr("font-family", "Corbel")
	  		.attr("font-size", "16px")
	  		.attr("font-weight", "normal");



	  chart.append("text")      // text label for the x axis
	  		.attr("class","xaxis hist_x")
	        .attr("x",  1.5*imgwidth+offsetx_hist )
	        .attr("y",  imgheight-graphheight+offsety_hist-offsetspace_hist -45   )
	        .style("text-anchor", "middle")
	        .attr("font-family", "Corbel")
	  		.attr("font-size", "16px")
	  		.attr("font-weight", "bold")
	        .text(opties.x_label+ '(voor '+opties.y_label+'='+y_val+' +/- '+deltay.toFixed(1)+')');

	  chart.append("text")      // text label for the x axis
	    	.attr("class","yaxis hist_y")
	        .attr("x", 1.5*imgwidth+offsetx_hist )
	        .attr("y", imgheight- (2*graphheight +offsetspace_hist +offsety_hist +50)) 
	        .attr("font-family", "Corbel")
	  		.attr("font-size", "16px")
	  		.attr("font-weight", "bold")
	        .style("text-anchor", "middle")
	        .text(opties.y_label+ '(voor '+opties.x_label+'='+x_val+' +/- '+ deltax.toFixed(0)+')');


	  draw_legend(labels_histxy, colors_histxy);


	  chart.append("svg:line")
	 	.attr("class","hist_x")
	    .attr("x1", xoffset)
	    .attr("y1", y+yoffset)
	    .attr("x2",imgwidth+xoffset)
	    .attr("y2", y+yoffset)
	    .style("stroke", "rgb(8,8,130)");


	  chart.append("svg:line")
	 	.attr("class","hist_y")
	    .attr("x1", x+xoffset)
	    .attr("y1", 25)
	    .attr("x2", x+xoffset)
	    .attr("y2", imgwidth+25)
	    .style("stroke", "rgb(130,8,8)");
	}


	this.handle_drag=function(evt) {
		if (_this.dragging==true) {


			var svgEl= document.getElementById("dragrect_"+_this.nr);	
			if (svgEl==null)  {
				  var chart=_this.chart;

					chart.append("rect")
							.attr("id",'dragrect_'+_this.nr)
							.attr("x",0)
							.attr("y",0)
							.attr("height",0)
							.attr("width",0)
							.attr("stroke",'black')
							.attr("stroke-width",1)
							.attr("fill","none");
			}
			
			var x=parseInt(evt.pageX-$(this).position().left);
			var y=parseInt(evt.pageY-$(this).position().top);

			
			var xdelta=-(evt.clientX- _this.origX);
			var ydelta=-(evt.clientY- _this.origY);
			
			var xdelta=x-_this.x0;
			var ydelta=y-_this.y0;

			console.log ('dragging:', _this.x0, _this.y0, x,y, xdelta, ydelta );
      		      		
			if (xdelta<0) {
				svgEl.setAttribute("x",  x);
				svgEl.setAttribute("width",  -xdelta);
			} else {
				svgEl.setAttribute("x",   _this.x0 );
				svgEl.setAttribute("width",  xdelta);
			}
						
			if (ydelta<0) {
				svgEl.setAttribute("y",  y);
				svgEl.setAttribute("height",  -ydelta);
			} else {
				svgEl.setAttribute("y",   _this.y0 );
				svgEl.setAttribute("height",  ydelta);
			}

			svgEl.style.stroke = "#ff0000";

		}
	}

	this.init_dragging=function (evt) {
		_this.dragging=false;
		console.clear();
		console.log('init_drag');
		
		_this.x0=parseInt(evt.pageX-$(this).position().left);
		_this.y0=parseInt(evt.pageY-$(this).position().top);
	}

	this.end_dragging=function (evt) {
		_this.dragging=false;
		var opties=_this.opties;

		console.log('end_drag');		
		var svgEl= document.getElementById('dragrect_'+_this.nr);
		svgEl.style.stroke = "#0000ff";

		var x=parseInt(evt.pageX-$(this).position().left);
		var y=parseInt(evt.pageY-$(this).position().top);

		console.log('x0, y0, x1,y1',_this.x0,_this.y0,x,y);
		$('#selectbox').remove();
		if ((_this.x0==x) && (_this.y0==y))  		
		{
			var svgEl= document.getElementById("dragrect_"+_this.nr);	
			svgEl.setAttribute("height",  0);
			svgEl.setAttribute("width",  0);			
			return;
		}
		

		

		s='';
		var sel_xmin=_this.x_to_world(_this.x0-75).toFixed(2);
		var sel_xmax=_this.x_to_world(x-75).toFixed(2);
		var sel_ymin=_this.y_to_world(_this.y0).toFixed(2);
		var sel_ymax=_this.y_to_world(y).toFixed(2);

		var x0=h.world_to_x(sel_xmin);    s
		var x1=h.world_to_x(sel_xmax);    
		var y0=h.world_to_y(sel_ymin);		
		var y1=h.world_to_y(sel_ymax);		
		var width=x1-x0;
		var height=y0-y1;		

		
		var text_ypos=parseInt(y1+height/2);
		var text_xpos=parseInt(h.opties.imgwidth+150);
		var connector_direction='right';

	//	$('#selectieform').show();
		


				// nieuw selectie_id bepalen
		annotatie_ids=[];
		annotaties=opties.annotate;
		for (var annotatie_key in annotaties) {
 			   if (annotaties.hasOwnProperty(annotatie_key)) {
 			   	annotatie_ids.push(parseInt(annotaties[annotatie_key].selectie_id));
 			   }
    		}

    	if (annotatie_ids.length==0) {
    		selectie_id=0;
    	} else {
    			selectie_id=Math.max.apply(Math, annotatie_ids)+1;
    	}



		new_annotation={};
		new_annotation.xvar=opties.xvar;
		new_annotation.yvar=opties.yvar;

		new_annotation.xmin=sel_xmin;
		new_annotation.xmax=sel_xmax;
		new_annotation.ymin=sel_ymin;
		new_annotation.ymax=sel_ymax;

		new_annotation.selectie_id=selectie_id;
		new_annotation.text_xpos=text_xpos;
		new_annotation.text_ypos=text_ypos;
		new_annotation.connector_direction=connector_direction;
		new_annotation.filename='selectie_'+selectie_id;
		new_annotation.txt='';
		new_annotation.label='';


		edit_annotation (new_annotation);
//		$('#overlay').css('visibility','visible');
		console.log('all done');
		edit_annotation_flag=false;
	}








	this.init_hist_xy=function  () {

		console.log('init_hist');
		this.dragging=false;
		$("#heatmap_container_0").on('mousedown', _this.init_dragging);
		$("#heatmap_container_0").on('mousemove', _this.handle_drag);
		$("#heatmap_container_0").on('mouseup', _this.end_dragging);
		//d3.select("heatmap_container_0")
		$("#heatmap_svg_0").on('click',_this.update_hist_x_y);



		//$("#heatmap_svg").on('mousedown',update_hist_x_y);
	}


	this.click_stats=function  () {

		var id=$(this).attr('id');
		var f=$(this).attr('data-stats');
		console.log('click_stats:',f);
		var state=_this.opties[f];
		if (state==true)	{
			state=false;
			$(this).removeClass('active_selectie');
		}
		else {
			state=true;
			$(this).addClass('active_selectie');
		}
		_this.opties[f]=state;
		_this.bin_data();
		_this.draw_heatmap();

	}




	this.init_stats=function (widget_id, transform) {

	 	$('.stats').on('click',_this.click_stats);
	 	$('.stats').on('mouseenter ',enter_selectie);
	  	$('.stats').on('mouseout ',leave_selectie);

	  	$('.stats').each(function(i,obj){
	  		var f=$(this).attr('data-stats');
	  		_this.opties[f]=false;
	  	});
	}


	this.update_display=function(displaymode) {


		console.log('update_display',displaymode);
		console.trace();
		if (displaymode=='dotplot') {
    	    $('.colormap-gradient').css("display","none");
        	$('.dotplot-controls').css("display","");
        	$('.text-controls').css("display","none");
        	$('.txt').remove();
        	_this.draw_dotplot();
	  	}
	  	if (displaymode=='heatmap') {
	  		$('.dotplot-controls').css("display","none");
	  		$('.text-controls').css("display","none");
	  		$('.colormap-gradient').css("display","");
	  		$('.txt').remove();
	  		$('.dot').remove();
	  		$('.dot_grid').remove();
	  		_this.draw_heatmap();
	  	}
	  	if (displaymode=='text') {
	  		$('.text-controls').css("display","");
	  		$('.dotplot-controls').css("display","none");
	  		$('.text-controls').css("display","");
	  		$('.colormap-gradient').css("display","");
	  		$('.dot').remove();
	  		$('.dot_grid').remove();
	  		_this.draw_text();
	  	}
	}

	this.click_change_display=function () {

		var id=$(this).attr('id');
		var f=$(this).attr('data-display');
		console.log('click_change_display:',f);
		_this.opties['displaymode']=f;
		_this.update_display(f);
	}


	this.init_display=function (widget_id, transform) {

	 	$('.display').on('click',_this.click_change_display);
	 	$('.display').on('mouseenter ',enter_selectie);
	  $('.display').on('mouseout ',leave_selectie);

		_this.update_display(_this.opties.displaymode);
	}


	this.update_dotplot=function  (e) {

		console.log('update_gradient:');
		if (e.keyCode == '13') {
			boxsize=$('#dotplot_boxsize_val').val();
			dotsize=$('#dotplot_dotsize_val').val();
			console.log('update_dotplot:',boxsize, dotsize);
			opties['dot_boxsize']=boxsize;
			opties['dot_dotsize']=dotsize;
			_this.draw_dotplot ();
			console.log('update_dotplot done');
		}

	}

	this.toggle_dotplot=function ()
	{
		console.log('toggle_dotplot',opties['use_dots'] );
		if(_this.opties['use_dots']){
			$(this).removeClass('active_selectie');
			_this.opties['use_dots']=false;
			$('.dot').remove();
		} else{
			$(this).addClass('active_selectie');
			_this.opties['use_dots']=true;
			_this.draw_dotplot();
		}
	}


	this.show_dot_background=function () {

		if(_this.opties['dot_show_background']){
			$('#dotplot_show_background').addClass('active_selectie');
			$('.heatmap_canvas').show();
			_this.draw_heatmap();
		} else {
			$('#dotplot_show_background').removeClass('active_selectie');
			$('.heatmap_canvas').hide();
		}
	}

	this.show_dot_grid=function () {

		console.log('show_dot_grid',_this.opties['dot_grid']);
		if(_this.opties['dot_grid']){
			$('#dotplot_grid').addClass('active_selectie');
			$('.dot_grid').show();
		} else {
			$('#dotplot_grid').removeClass('active_selectie');
			$('.dot_grid').hide();
		}
	}


	this.toggle_dot_background=function ()
	{
		console.log('toggle_dot_background',opties['dot_show_background'] );
		if(_this.opties['dot_show_background']){
			_this.opties['dot_show_background']=false;
		} else{
			_this.opties['dot_show_background']=true;
		}
		_this.show_dot_background();
	}

	this.toggle_dot_grid=function ()
	{
		console.log('toggle_dot_grid',opties['dot_grid'] );
		if(_this.opties['dot_grid']){
			_this.opties['dot_grid']=false;
		} else{
			_this.opties['dot_grid']=true;
		}
		_this.show_dot_grid();
	}

	this.toggle_dotgradient=function ()
	{
		console.log('toggle_dotgradient',opties['dot_use_gradient'] );

		if(_this.opties['dot_use_gradient']){
			$(this).removeClass('active_selectie');
			_this.opties['dot_use_gradient']=false;
			_this.draw_dotplot();
		} else{
			_this.opties['dot_use_gradient']=true;
			$(this).addClass('active_selectie');
			_this.draw_dotplot();
		}
	}

	this.init_dotplot=function  () {
		$('#dotplot_heatdots').on('click',_this.toggle_dotgradient);
		$('#dotplot_show_dotplot').on('click',_this.toggle_dotplot);
		$('#dotplot_grid').on('click',_this.toggle_dot_grid);
		$('#dotplot_show_heatmap').on('click',_this.toggle_dot_background);
	 	$('.stats').on('mouseenter ',enter_selectie);
	  	$('.stats').on('mouseout ',leave_selectie);
		$("#dotplot_boxsize_val").on('keydown',_this.update_dotplot);
		$("#dotplot_dotsize_val").on('keydown',_this.update_dotplot);

		if (_this.opties['dot_use_gradient']) {
			$('#dot_use_gradient').addClass('active_selectie');
		}
		_this.show_dot_background();
	}



	this.click_annotation=function (e) {

    	e.stopPropagation();

		nr=$(this).attr("data-annotationid");
		console.log('click_annotate, id/edit:',nr,edit_annotations);


		a=_this.opties.annotate[nr];

/*		if (edit_annotations) {
			annotatie=_this.opties.annotate[nr]		
			edit_annotation (annotatie);
		}
*/		
		if (selected_annotation!=undefined) {
			$('#annotation_obj_'+selected_annotation).attr('class','annotation annotation_obj');
			$('#annotation_textc_'+selected_annotation).hide();
		}
		$('#annotation_obj_'+nr).attr('class','annotation annotation_obj annotation_selected');

    	$('.annotation_label').hide();
		$('.annotation_text').hide();		
		$('.annotation_connector').hide();
		$('.hist_x').hide();
		$('.hist_y').hide();


		$('#annotation_textc_'+nr).show();


		$('#atext_'+nr).show();
		$('.connector_'+nr).show();
		selected_annotation=nr;

		console.log('ok');
	}

	this.enter_annotation=function (e) {

		nr=$(this).attr("data-annotationid");
		console.log('enter_annotation:',nr);
		$('#annotation_obj_'+nr).attr('class','annotation annotation_obj annotation_hover');
	}

	this.leave_annotation=function (e) {

		nr=$(this).attr("data-annotationid");
		if (selected_annotation==nr) {
			$('#annotation_obj_'+nr).attr('class','annotation annotation_obj annotation_selected');
		} else {
			$('#annotation_obj_'+nr).attr('class','annotation annotation_obj');
		}
	}




	this.init_annotations=function () {

		init_annotations (_this, _this.opties.annotate);
	}

}
