
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



function heatmap (data, opties) {
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

	var _this = this;

	var xpix2img=parseInt(opties.imgwidth/opties.x_steps);
	var ypix2img=parseInt(opties.imgheight/opties.y_steps);



	this.init_databuffers =function (svg_el, canvas_el) {

		var opties=_this.opties;
		var imgwidth=opties.imgwidth;
		var imgheight=opties.imgheight;
		var c,s;

		console.log('init_databuffers:', svg_el, canvas_el, imgwidth, imgheight);

		var c=document.getElementById(canvas_el);
	    c.setAttribute("width", imgwidth);
    	c.setAttribute("height", imgwidth);
    	_this.ctx = c.getContext('2d');
    	var s=document.getElementById(svg_el);
    	s.setAttribute("width", imgwidth*2+100);
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

		var imgsize=imgwidth*imgheight
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

		console.log('update_minmax:min/max:',minval,maxval );

		var opties=_this.opties;
		var gradient_node=document.getElementById("cg_a");
		var gradmax=gradient_node.getAttribute('gradient_max');
		var gradmin=gradient_node.getAttribute('gradient_min');
		var gradsteps=gradient_node.getAttribute('gradient_steps');

		if (gradmax=='max') {
			gradient_node.setAttribute('gradient_max_data', maxval);
		} else {
			if (gradient_node.hasAttribute('gradient_max_data')) {
				gradient_node.removeAttribute ('gradient_max_data');
			}
		}
		if (gradmin=='min') {
			gradient_node.setAttribute('gradient_min_data', minval);
		} else {
			if (gradient_node.hasAttribute('gradient_min_data')) {
				gradient_node.removeAttribute ('gradient_min_data');
			}
		}

		if (opties.missing_color=='min'){
			_this.missing_color=gradient_node.colormap[0];
		} else {
			_this.missing_color=opties.missing_color;
		}
		console.log('missing_color:',_this.missing_color);
	}




	this.bin_data=function  () {

		console.log("bin_data");
		var gradient_node=document.getElementById("cg_a");
		if (gradient_node.need_data_recalc==false) return;

		if (multimap) {
			_this.bin_data_multi();
			return;
		}

		var size=gradient_node.size;
		if (size==1) {
			_this.bin_data_1 ();
			return;
		}
		if (size<1) {
			console.error ('illegal size:',size);
			return;
		}

		var opties=_this.opties;
		var log_min=gradient_node.getAttribute('log_min');

		var weighx=opties.weighx;
		var weighy=opties.weighy;
		var x_steps=opties.x_steps;
		var y_steps=opties.y_steps;
		var transform=gradient_node.getAttribute('transform');

		console.log('bin_data:',x_steps, y_steps, size);
		console.log('weighx/y:', weighx, weighy);
		var data=_this.data;

		var ptr2=0;
		var maxval=data[0];
		var minval=data[0];
		var xmean=_this.xmean;
		var ymean=_this.ymean;
		var sum_x=_this.sum_x;
		var sum_y=_this.sum_y;
		var transposebuffer=_this.transposebuffer;

		console.log('xmean,ymean:\n', xmean, ymean, size, typeof(size))


		for (var i=0; i<y_steps; i+=size) {
			for (var j=0; j<x_steps;  j+=size) {
				val=0;
				ptr=j*y_steps+i;
				for (cx=0; cx<size; cx++) {
					for (cy=0; cy<size; cy++) {
						val+=data[ptr+cx+cy*x_steps];
					}
				}				//cy

				val=val/(size*size);
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
			} //j
	//		console.log("i:",i);
		}	//i

		_this.update_minmax(minval,maxval);
	}


	this.bin_data_multi=function () {

		console.log("bin_data_multi", datasets.length);
		var gradient_node=document.getElementById("cg_a");
		var log_min=gradient_node.getAttribute('log_min');

		var maxval=multimap_vals[0][0];
		var minval=multimap_vals[0][0];

		var x_steps=opties.x_steps;
		var y_steps=opties.y_steps;
		var transform=gradient_node.getAttribute('transform');
		var transposebuffer=_this.transposebuffer;
		var transposebuffer_cats=_this.transposebuffer_cats;
		var weighx=opties.weighx;
		var weighy=opties.weighy;
		var xmean=_this.xmean;
		var ymean=_this.ymean;
		var sum_x=_this.sum_x;
		var sum_y=_this.sum_y;


		var values=multimap_vals[0];
		var colors=multimap_colors[0];
		var datalength=data.length;
		console.log("bin_data_multi", data.length, x_steps, y_steps);
		console.log("bin_data_multi", maxval,minval);

		var ptr2=0;
		var nr=0;
		for (var i=0; i<y_steps; i++) {
			for (var j=0; j<x_steps;  j++) {
				val=0;
				ptr=j*y_steps+i;
				val=values[ptr];
				if (val>maxval) maxval=val;
				if (val<minval) minval=val;
				//val=transform_value(val,transform, log_min);

				transposebuffer[ptr2]=val;
				transposebuffer_cats[ptr2]=colors[ptr];
				ptr2++;
			} //j
	//		console.log("i:",i);
		}	//i

		_this.transposebuffer=transposebuffer;
		_this.transposebuffer_cats=transposebuffer_cats;
		//		console.log("i:",i);
		console.log('bin_data_multi:', minval, maxval);
		_this.update_minmax(minval,maxval);
	}



	this.bin_data_1=function  () {

		console.log("bin_data_1");
		var gradient_node=document.getElementById("cg_a");

		var opties=_this.opties;
		var log_min=gradient_node.getAttribute('log_min');

		var weighx=opties.weighx;
		var weighy=opties.weighy;
		var x_steps=opties.x_steps;
		var y_steps=opties.y_steps;
		var transform=gradient_node.getAttribute('transform');

		console.log('bin_data:',x_steps, y_steps, size);
		console.log('weighx/y:', weighx, weighy);
		var data=_this.data;

		var ptr2=0;
		var maxval=data[0];
		var minval=data[0];
		var xmean=_this.xmean;
		var ymean=_this.ymean;
		var sum_x=_this.sum_x;
		var sum_y=_this.sum_y;
		var transposebuffer=_this.transposebuffer;

		console.log('xmean,ymean:\n', xmean, ymean, size, typeof(size))

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

		_this.update_minmax(minval,maxval);
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
		var size=gradient_node.size;

		var histmax=_this.histmax;
		var transposebuffer=_this.transposebuffer;
		var transposebuffer_cats=_this.transposebuffer_cats;
		var backbuffer=_this.backbuffer;
		var backbuffer_cats=_this.backbuffer_cats;


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

		console.log('spread_bins: transform, gradmin/gradmax',transform, gradmin,gradmax);
		var gradmax=transform_value(gradmax,transform, log_min);
		var gradmin=transform_value(gradmin,transform, log_min);

		var delta=gradmax-gradmin;
		console.log('spread_bins, gradmin/gradmax, multimap',gradmin,gradmax,multimap);


		var line=0;
		for (i=0; i<opties.imgwidth*opties.imgheight; i++) {
			backbuffer[i]=0;
		}
		xstep=xpix2img*size;
		ystep=ypix2img*size;
		console.log('xstep, ystep',xstep,ystep);

		u=0;
		v=1;
		//console.log('xstep/ystep:',xstep,ystep, xpix2img, ypix2img, size);
		_this.hist=new Array(gradsteps);
		var hist=_this.hist;
		for (i=0; i<gradsteps; i++) {
			hist[i]=0;
		}
		console.log('totalpixels,ptr:',totalpixels, opties.imgheight, opties.imgwidth);

		console.log('val2index:',gradmin, delta,gradsteps);

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
			console.log('multimap');
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
	console.log(hist);

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
		console.log('draw_heatmap, size:',size);
		var xstep=xpix2img*size;
		var ystep=ypix2img*size;

		var colormap=gradient_node.colormap;
		var imgwidth=opties.imgwidth;
		var imgheight=opties.imgheight;
		var mean_x=_this.mean_x;
		var median_x=_this.median_x;
		var extradata=_this.extradata;
		var cat=null;

	//	console.log('draw_heatmap, colormap:', colormap);

		console.log("draw_heatmap:",backbuffer.length);
		for (i=0,j=0; i<backbuffer.length; i++,j+=4) {
				indexval=backbuffer[i];
				/*
				if ((indexval>0) && (nr<50)) {
							console.log(nr, i,j,indexval);
							nr+=1;
						}
				*/

				if ((indexval!=0) || (!_this.skipzero)) {	  // waardes die 0 zijn niet plotten
					if (multimap){

						cat=backbuffer_cats[i];
						color=colormap[cat];

						if ((indexval>0) && (nr<550)) {
							//console.log(nr, i,j,cat, color);
							nr+=1;
						}

			    			mapdata[j] =  color[0];
			    			mapdata[j+1] = color[1];
		    				mapdata[j+2] = color[2];
		    				mapdata[j+3] = 0xff;

					} else {
						color=colormap[indexval];
		    				mapdata[j] =  color[0];
			    			mapdata[j+1] = color[1];
			    			mapdata[j+2] = color[2];
			    			mapdata[j+3] = 0xff;
		    		}
				} else {
					color=_this.missing_color;
					mapdata[j] =  color[0]; ;
		    		mapdata[j+1] = color[1]; ;
		    		mapdata[j+2] = color[2]; ;
		    		mapdata[j+3] = 0xff;
		    	}

			}
		if (opties['plot_mean']==true){
			console.log('plot_mean:',xstep,xpix2img, ystep, ypix2img);
			color=opties['plot_mean_color'];
			for (i=0; i<mean_x.length; i++) {
				avgval=mean_x[i];
				ptr=(i*xpix2img+imgwidth*(imgheight-ypix2img*avgval))*4;
				mapdata[ptr]=color[0];
				mapdata[ptr+1]=color[1];
				mapdata[ptr+2]=color[2];
				mapdata[ptr+3]=color[3];
			}
		}
		if (opties['plot_median']==true){
			color=opties['plot_median_color'];
			for (i=0; i<median_x.length; i++) {
				medval=median_x[i];
				ptr=(i*xstep+ystep*imgwidth*(imgheight-medval))*4;
				mapdata[ptr]=color[0];
				mapdata[ptr+1]=color[1];
				mapdata[ptr+2]=color[2];
				mapdata[ptr+3]=color[3];
			}
		}

		if (opties['info_datafile']!=null){
			color=opties['info_color'];
			for (i=0; i<extradata.length; i++) {
				i=extradata[i][0];
				j=i=extradata[i][1];
				ptr=(i*size+size*imgwidth*(imgheight-j))*4;
				mapdata[ptr]=color[0];
				mapdata[ptr+1]=color[1];
				mapdata[ptr+2]=color[2];
				mapdata[ptr+3]=color[3];
			}
		}
		console.log('putdata');
		_this.ctx.putImageData(_this.imgData, 0, 0);
	}






	this.init_print=function () {
	   $('.print').on('click',_this.click_print);
	   $('.sidelist').on('mouseenter ',enter_selectie);
	   $('.sidelist').on('mouseout ',leave_selectie);
	}


	this.print_ok=function  () {
		console.log("print ok");
	}

	this.print_fail=function  () {

		var opties=_this.opties;

		console.log('print failed');
		s='\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'
		s+="Printen niet gelukt. Opties voor command-line-reproductie:\n\n";
		s+='import contour\n\n'
		s+='args=dict(\n\t'
		var firstkey=true;


		opties['default_colormap']=colormapname;
		opties['default_size']=size;
		opties['default_transform']=transform;
		opties['gradmin']=gradmin;
		opties['gradmax']=gradmax;
		opties['gradsteps']=gradsteps;

		console.log('transform=',transform);

		var optiekeys=[];
		for (key in opties) {
	    	if (opties.hasOwnProperty(key)) {
	    		optiekeys.push(key);
	    	}
	    }
	    optiekeys.sort();

	    delete opties['datamin'];
	    delete opties['datamax'];
	    delete opties.x_max;
	    delete opties.x_min;
	    delete opties.y_max;
	    delete opties.y_min;


	    for (var i=0; i<optiekeys.length; i++) {
	    		key=optiekeys[i];
	    		if (!(firstkey)) {
	    			s+=',\n\t';
	    		}
				val=opties[key];
				console.log(key,val, typeof(val));
				if (typeof(val)=='number')  {
	    			s+=key+'='+val;
	    		}
	    		if (typeof(val)=='boolean') {
	    			if (val==true) {
	    				s+=key+'=True'
	    			}
		   			if (val==false) {
	    				s+=key+'=False'
	    			}

	    		}
				if (typeof(val)=='string') {
					s+=key+'="'+val+'"';
				}
	    		firstkey=false;
	    }
	    s+=')\nc=contour.contour()\nc.run_contour(args)\n';

	    $('#printcode').html(s);
	}

	this.click_print=function  () {


		var printtype=$(this).attr('data-print');
		//$.get('#',{'cmd':printtype})
	 	$.ajax({
	            cache: false,
	            url: "/"+printtype,
	            type: "GET"

	        })
	 		.done(print_ok)
	 		.fail(print_fail);

	}











	  this.draw_axes=function  () {

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
	  				console.log(opties.x_mindate,opties.x_maxdate);
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
	  				console.log(opties.y_mindate,opties.y_maxdate);
	  				var y_data_type_simple='date';
	  			}
	  	    }


	  xScale.range([0,imgwidth]);
	  yScale.range([0,imgheight]);

	  var xAxis=d3.svg.axis();
	  var yAxis=d3.svg.axis();	
	  xAxis.scale(xScale)
	  		.ticks(numticks)	  		
	        .orient("bottom");
	  if ((x_data_type=='nominal') && (!x_log)) {
	  	xAxis.tickFormat(d3.format("s"));
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
	  		.ticks(numticks)
	        .orient("left");
	  if ((y_data_type=='nominal') && (!y_log)) {
	  	yAxis.tickFormat(d3.format("s"));
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


	  fontsize=opties['fontsize'];

	  //console.log(chart);
	  var chart=_this.chart;

		chart.append("rect")
			.attr("id",'dragrect')
			.attr("x",0)
			.attr("y",0)
			.attr("height",0)
			.attr("width",0)
			.attr("stroke",'black')
			.attr("stroke-width",1)
			.attr("fill","none")

	  chart.append("rect")
	  		.attr("id",'IE9_hack')
	  		.attr("x",0)
	  		.attr("y",0)
	  		.attr("height",imgheight)
	  		.attr("width",imgwidth)
	  		.attr("stroke",'black')
	  		.attr("stroke-width",0)
	  		.attr("fill","none")

	  chart.append("g")
	        .attr("class","xaxis mainx")
	        .attr("transform","translate(75,"+(imgheight+25)+")")
	        .attr('font-size','32px')
	        .call(xAxis);
	  chart.append("g")
	        .attr("class","yaxis")

	        .attr("transform","translate(75,25)")
	        .call(yAxis);
	  chart.selectAll(".tick >text")
	  		.attr("font-family", "Corbel")
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



	  chart.append("text")      // text label for the x axis
	  		.attr("class","xaxis")
	        .attr("x", imgwidth/2+70 )
	        .attr("y",  imgheight+70 )
	        .style("text-anchor", "middle")
	        .attr("font-family", "Corbel")
	  		.attr("font-size", fontsize+"px")
	  		 .attr("transform","translate(0,"+(fontsize-15)+xlabeloffset+")")
	  		.attr("font-weight", "bold")
	        .text(opties.x_label);
	  chart.append("text")      // text label for the x axis
	    	.attr("class","yaxis")
	        .attr("x", 0 )
	        .attr("y", 0)
	        .attr("font-family", "Corbel")
	  		.attr("font-size", fontsize+"px")
	  		.attr("font-weight", "bold")
	        .attr("transform","translate(20,"+(imgheight/2)+")rotate(270)")
	        .style("text-anchor", "middle")
	        .text(opties.y_label);
	  chart.append("text")      // text label for the x axis
	    	.attr("class","yaxis")
	        .attr("x", imgwidth/2+70 )
	        .attr("y", 15)
	        .attr("font-family", "Corbel")
	  		.attr("font-size", fontsize+"px")
	  		.attr("font-weight", "bold")
	        .style("text-anchor", "middle")
	        .text(opties.title);
	        /*
	  if (y_data_type_simple=='date') {
	  	chart.selectAll(".mainy")
	  			.selectAll(".tick >text")
	  			.attr("transform", "translate(-10,0)rotate(-45)")
	  			.style("text-anchor", "end");
		ylabeloffset=8;
	  	}
	  	*/


	}





	this.draw_text=function  () {

		console.log('draw text');
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


		console.log('start text, size', size);
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
        .attr("font-family", "Corbel")
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



			console.log('draw_dotplot',xmin, xmax, x_steps, dx,dy);

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
					console.log('bimodal:',delta,delta2,colormap,colormap2)
				} else {
					var delta=gradmax-gradmin;
					var colormap=gradient_node.colormap;
				}
				var color='';
			}


			var size=gradient_node.size
			console.log('start dotplot, size', size);
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
		var xmax=opties.x_max+1;
		var xmin=opties.x_min;
		var delta=(xmax-xmin);
		//var val=((x-75)/imgwidth)*delta+xmin;

		var val=((x-xmin)/delta)*imgwidth+75

		return val;
	}

	this.world_to_y=function (y) {
		var opties=_this.opties;
		var imgheight=opties.imgheight;
		var ymax=opties.y_max+1;   // off by one, again.
		var ymin=opties.y_min;
		var delta=(ymax-ymin);
		//var val=(((imgheight-y)+25)/imgheight)*delta+ymin;

		var val=imgheight-((y-ymin)/delta*imgheight)+15;
		console.log('y,val:',y,val);
		return val;
	}


	this.x_to_world=function (x) {
		var opties=_this.opties;
		var imgwidth=opties.imgwidth;
		var xmax=opties.x_max+1;
		var xmin=opties.x_min;
		var delta=(xmax-xmin);
		var val=((x-75)/imgwidth)*delta+xmin;

		return val;
	}

	this.y_to_world=function (y) {
		var opties=_this.opties;
		var imgheight=opties.imgheight;
		var ymax=opties.y_max+1;   // off by one, again.
		var ymin=opties.y_min;
		var delta=(ymax-ymin);
		var val=(((imgheight-y)+25)/imgheight)*delta+ymin;

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


		x=parseInt(evt.pageX-$(this).position().left);
		y=parseInt(evt.pageY-$(this).position().top);
		console.log(x, y);

		if ((x<0) || (y<0) || (x>imgwidth) || (y>imgheight)) {
			if ((x>imgwidth) && (x<imgwidth+100) && (y<150)) {
				//toggle_gradcontrols();
			}
			return false;
		}

		$('.hist_x').remove();
		$('.hist_y').remove();
		$('.pointinfotext').remove();

		var offsetx_hist=125;  //distance between heatmap and side-histograms
		var offsety_hist=25;   // distance between bottom of screen & side-histograms
		var offsetspace_hist=-40;   // distance between side-histograms
		var graphheight=0.25*imgheight;

		var val=_this.x_to_world(x);
		console.log(val, typeof(val));
		if (val>1000){
			xval=Math.round(val);
		} else {
			xval=Math.round(val*100)/100;
		}


		/* text upper right corner */
	 	chart.append("text")
	    	.attr("class","pointinfotext")
	        .attr("x", 1.5*imgwidth+100 )
	        .attr("y", 50 )
	        .attr("font-family", "Corbel")
	        .attr("font-size", "15px")
	        .attr("font-weight", "bold")
	        .text(opties.x_label+':'+xval);

	    var val=_this.y_to_world(y);
		yval=val.toFixed(0);
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
	        .text('#count:'+val);



	/* histogram y */

	

		histy_max=0;
		for (i=0; i<imgwidth; i++) {
			val=backbuffer[y*imgheight+i];
			if (val>histy_max) histy_max=val;
		}


		//console.log(histy_max);


		for (i=0; i<imgwidth; i++) {
		 	val=backbuffer[y*imgheight+i];
		//	console.log('x,y:', imgwidth+offsetx_hist+i, parseInt(imgheight-(val/histy_max)*graphheight)+offsety_hist );
		 	color=colormap[val];
			chart.append("rect")
				.attr("class","hist_y")
				.attr("x",imgwidth+offsetx_hist+i)
				.attr("y",parseInt(imgheight-(val/histy_max)*graphheight)+offsety_hist)
				.attr("width",1)
				.attr("height",(val/histy_max)*graphheight)
				.style("fill","rgb(8,8,0)")
				.style("stroke","rgb(8,8,0)")
				//.style("fill","rgb("+color[0]+","+color[1]+","+color[2]+")")
				//.style("stroke","rgb("+color[0]+","+color[1]+","+color[2]+")")
				.style("stroke-width","1px");
			 }


	histx_max=0;
	for (i=0; i<imgheight; i++) {
		 	val=backbuffer[i*imgwidth+x];
		 	if (val>histx_max) histx_max=val;
		 }

	for (i=0; i<imgheight; i++) {
		 	val=backbuffer[i*imgwidth+x];
		 	color=colormap[val];
			chart.append("rect")
				.attr("class","hist_y")
				.attr("x",2*imgwidth+offsetx_hist-i)
				.attr("y",imgheight-(val/histx_max)*graphheight-graphheight+offsety_hist+offsetspace_hist)
				.attr("width",1)
				.attr("height",(val/histx_max)*graphheight)
				.style("fill","rgb(130,8,8)")
				.style("stroke","rgb(130,8,8)")

				//.style("fill","rgb("+color[0]+","+color[1]+","+color[2]+")")
				//.style("stroke","rgb("+color[0]+","+color[1]+","+color[2]+")")
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
	        .attr("y",  imgheight+offsety_hist+35 )
	        .style("text-anchor", "middle")
	        .attr("font-family", "Corbel")
	  		.attr("font-size", "16px")
	  		.attr("font-weight", "bold")
	        .text(opties.x_label+ '(voor '+opties.y_label+'='+yval+')');
	  chart.append("text")      // text label for the x axis
	    	.attr("class","yaxis hist_y")
	        .attr("x", 1.5*imgwidth+offsetx_hist )
	        .attr("y", imgheight-graphheight+offsety_hist-offsetspace_hist-45 )
	        .attr("font-family", "Corbel")
	  		.attr("font-size", "16px")
	  		.attr("font-weight", "bold")
	        .style("text-anchor", "middle")
	        .text(opties.y_label+ '(voor '+opties.x_label+'='+xval+')');


	  chart.append("svg:line")
	 	.attr("class","hist_x")
	    .attr("x1", 75)
	    .attr("y1", y)
	    .attr("x2",imgwidth+75)
	    .attr("y2", y)
	    .style("stroke", "rgb(8,8,130)");


	  chart.append("svg:line")
	 	.attr("class","hist_y")
	    .attr("x1", x)
	    .attr("y1", 25)
	    .attr("x2", x)
	    .attr("y2", imgwidth+25)
	    .style("stroke", "rgb(130,8,8)");
	}


	this.handle_drag=function(evt) {
		if (_this.dragging==true) {

			var svgEl= document.getElementById("dragrect");			
			
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
		_this.dragging=true;
		console.clear();
		console.log('init_drag');
		
		_this.x0=parseInt(evt.pageX-$(this).position().left);
		_this.y0=parseInt(evt.pageY-$(this).position().top);
	}

	this.end_dragging=function (evt) {
		_this.dragging=false;
		var opties=_this.opties;

		console.log('end_drag');		
		var svgEl= document.getElementById("dragrect");
		svgEl.style.stroke = "#0000ff";

		var x=parseInt(evt.pageX-$(this).position().left);
		var y=parseInt(evt.pageY-$(this).position().top);

		console.log('x0, y0, x1,y1',_this.x0,_this.y0,x,y);
		$('#selectbox').remove();
		if ((_this.x0==x) && (_this.y0==y))  		
		{
			var svgEl= document.getElementById("dragrect");	
			svgEl.setAttribute("height",  0);
			svgEl.setAttribute("width",  0);			
			return;
		}
		


		var s='python select.py ';
		s+=opties.x_var + ' ' + _this.x_to_world(_this.x0).toFixed(2) + ' ' + _this.x_to_world(x).toFixed(2)+' ';
		s+=opties.y_var + ' ' + _this.y_to_world(_this.y0).toFixed(2) + ' ' + _this.y_to_world(y).toFixed(2);
		console.log(s);

		
		_this.chart.append("text")
	    	.attr("id","selectbox")
	        .attr("x", 75 )
	        .attr("y", 50)
	        .attr("font-family", "Corbel")
	        .attr("font-size", "15px")
	        .attr("font-weight", "bold")
	        .text(s);
		
	}

	this.init_hist_xy=function  () {

		console.log('init_hist');
		this.dragging=false;
		$("#heatmap_container_0").on('mousedown', _this.init_dragging);
		$("#heatmap_container_0").on('mousemove', _this.handle_drag);
		$("#heatmap_container_0").on('mouseup', _this.end_dragging);
		$("#heatmap_container_0").on('click',_this.update_hist_x_y);



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

		_this.update_display(_this.optiesdisplaymode);
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


	this.click_annotation=function () {

		console.log('click_annotation:', this.id);
		a=_this.opties.annotate[this.id];
		console.log('click_annotate, text:',a.text);


		if (a.position=='top'){
			y=50;
		} else {
			y=a.text_y_pos;
		}

		console.log('ypos:', y);
		txt="<div class='annotation'>"+a.text+"</div>"; 
		_this.chart.append('foreignObject')
		    .attr("width", _this.opties.imgwidth)
		    .attr("height", _this.opties.imgheight)
		    .attr('x',_this.opties.imgwidth+100)
		    .attr('y',y)
		    .attr("class",'annotation')
		    .attr("id",'annotation')
   	        .append("xhtml:body")		       	        
    		.html(txt);



	}


	this.init_annotations=function () {
		init_annotations (_this, _this.opties.annotate);
	}

}
