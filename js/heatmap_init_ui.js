// https://developer.mozilla.org/en-US/docs/Web/API/FileReader#readAsDataURL%28%29

var c,s,ctx;
var print=false;
var datasets=null;
// printinfo hier
var interactive=true;

var smallsize=false;
var share_colormap=false;

function set_gradient (opties) {
 
    var defaultsettings={
        colormapname: opties.colormap,
        gradient_min: opties.gradmin,
        gradient_center: opties.gradcenter,
        gradient_max: opties.gradmax,                
        gradient_steps: opties.gradsteps,
        gradient_bimodal: opties.gradient_bimodal,
        log_min: opties.log_min,
        transform: opties.transform,
        gradient_invert: opties.gradient_invert,
        show_size: 'true',
        xpixels: opties.x_steps,
        ypixels: opties.y_steps,
        controltype: opties.controltype
    };
 
    topnode=document.getElementById('cg_a');
     for (var keyword in defaultsettings) {
      if (defaultsettings.hasOwnProperty(keyword)) {                      
            topnode.setAttribute(keyword, defaultsettings[keyword]);                      
      }
  }
}


function init_all_heatmaps(heatmapdata) {

    var source   = $("#heatmap-template").html();        
    var template = Handlebars.compile(source); 

    heatmapnode=document.getElementById('heatmap_div');
    //console.log(heatmapdata);
    heatmapnode.innerHTML =template(heatmapdata);
    var opt=opties[0];      


    var extrawidth=0;
    if (opt.imgwidth>300) {
        extrawidth=50;    
    } 
      
    var num_cols=opt.multimap_numcols;
    if (opt.imgwidth>300) {
        num_cols=2;
    }
    var width=opt.imgwidth+50;
    var height=opt.imgheight+75;
    var xpos=0;
    var ypos=50;
    var i=0;
    var j=0;
    for (i=0,j=1; i<data.length; i++,j++) {
        console.log('container:',i,j);
        $('#heatmap_container_'+i).css('margin-left',xpos);        
        $('#heatmap_container_'+i).css('top',ypos); 
        if (j!=1) opties[i].ylabel='';
        xpos+=width+extrawidth;
        if (j==num_cols) {
            for (k=num_cols; k>0; k--) {
                opties[i-k+1].xlabel='';                
            }
            ypos+=height;
            xpos=0;
            j=0;
        }

     //   $('#heatmap_container_'+i).css('left',xpos);       
    }    

    xpos=num_cols*width;
    $('.colormap-gradient').css('margin-left',xpos+'px')
}


var bin_alldata=function () {

	for (var i=0; i<nr_heatmaps; i++) {
        	heatmaps[i].bin_data();
	    }
}

var draw_heatmaps=function() {
    
    for (var i=0; i<nr_heatmaps; i++) {
       // console.log('draw_heatmaps:',data.length,i);
        heatmaps[i].draw_heatmap();
    }

}


function generate_colormap (endpoint, N) {
    
    var scale=chroma.scale(['white', endpoint]).correctLightness(true);

    var cmap=[];
    var frac=1.0/N;
    for (i=0; i<N; i++){
         var rgb=scale(i*frac).rgb();
         cmap.push([parseInt(rgb[0]),parseInt(rgb[1]),parseInt(rgb[2])]);
    }
  //  console.log(cmap);
    return cmap;  
}


function toggle_colormap_sharing () {

    console.log('toggle_colormap_sharing');
    if (share_colormap) {
        var quali_colormap=chroma.scale('Dark2');

        for (var i=0; i<nr_heatmaps; i++) {     
            var colormap_endpoint=quali_colormap(i/nr_heatmaps);   
            heatmaps[i].colormap=generate_colormap(colormap_endpoint, 20);
        }
        share_colormap=false;
    } else {
        for (var i=0; i<nr_heatmaps; i++) {        
            if ('colormap'  in  heatmaps[i]) {
                   delete heatmaps[i].colormap;
                }
        }
        share_colormap=true;
    }
    draw_heatmaps(); 
    return false;   
}


function resize_cats () {
    
    console.log('resize_cats:', smallsize);
    if (smallsize) {
        // opschalen naar grotere size: 500x500 oid
        smallsize=false;                            
        var new_imgwidth=opties[0].imgwidth*4;
        var new_imgheight=opties[0].imgheight*4;                
    } else {        
        smallsize=true;
        var new_imgwidth=opties[0].imgwidth/4;
        var new_imgheight=opties[0].imgheight/4;                
    }

    for (var i=0; i<nr_heatmaps; i++) { 
            heatmaps[i].opties.imgwidth=new_imgwidth; 
            heatmaps[i].opties.imgheight=new_imgheight;        
        }

    console.log('new imgwidth/height',new_imgwidth, new_imgheight)

    init_resized_page();         

    if (smallsize) {
        colpos=0;
        lastrow=parseInt(nr_heatmaps/4)*4;
        var num_cols=heatmaps[0].opties.multimap_numcols;
        for (i=0; i<nr_heatmaps; i++,colpos++) {            
            if (colpos==num_cols) {
                colpos=0;
            }
            if (colpos!=0) {
                $('.yticks_'+i).hide();
                $('.ylabel_'+i).hide();                
            }
            if (i<lastrow) {                
                $('.xlabel_'+i).hide();
                $('.xticks_'+i).hide();
            }         
        }
        draw_legend();
    } 

    if (!smallsize) {
        for (var i=0; i<nr_heatmaps; i++) { 
            $('.yticks_'+i).show();
            $('.ylabel_'+i).show(); 
            $('.xticks_'+i).show();
            $('.xlabel_'+i).show();                 
            }
    }

   return false; 
}



function init_resized_page() {
  
    console.log('init_page, # heatmaps:',data.length);    
    console.log('multimap',multimap);    
    
    var heatmapinfo=[];    
    nr_heatmaps=data.length;        
    for (i=0; i<nr_heatmaps; i++) {heatmapinfo.push(i);}

    datasets=data;
    var heatmapdata={heatmaps:heatmapinfo};
    init_all_heatmaps(heatmapdata);
    
    heatmaps=[];
    cat_colormap=[]; // globaal
    var quali_colormap=chroma.scale('Dark2');
    for (var i=0; i<nr_heatmaps; i++) {
        console.log('heatmap:',i,nr_heatmaps);
        h=new heatmap(data[i],opties[i],i);
        h.init_databuffers('heatmap_svg_'+i,'heatmap_canvas_'+i);
        h.mean_x=mean_x[i];
        h.median_x=median_x[i];
        h.xmean=xmean[i];
        h.ymean=ymean[i];
        h.sum_x=sum_x[i];
        h.sum_y=sum_y[i];
        var colormap_endpoint=quali_colormap(i/nr_heatmaps);
        var rgb=colormap_endpoint._rgb;
        var colortxt='rgb('+parseInt(rgb[0])+','+parseInt(rgb[1])+','+parseInt(rgb[2])+')';
        cat_colormap.push(colortxt);
        h.colormap=generate_colormap(colormap_endpoint, 20);
        h.draw_axes();                 
        heatmaps.push(h);    
    }


    set_gradient(opties[0]);    
    topnode.preAttributeChangedCallback=bin_alldata;    
    topnode.postAttributeChangedCallback=draw_heatmaps;        
    init_gradients();
    $('#cg_a').append('<svg id="legend" height="400" width="150"> <svg>');

    
    h=heatmaps[0];
    h.init_print();    
    h.init_stats();
    h.init_hist_xy();
    h.init_dotplot();
  //  h.init_display();     
    h.init_annotations();
}




function init_page() {
  
    console.log('init_page, # heatmaps:',data.length);    
    console.log('multimap',multimap);    
    
    var heatmapinfo=[];    
    nr_heatmaps=data.length;        
    for (i=0; i<nr_heatmaps; i++) {heatmapinfo.push(i);}

	datasets=data;
    var heatmapdata={heatmaps:heatmapinfo};
    init_all_heatmaps(heatmapdata);
    
    heatmaps=[];
    cat_colormap=[]; // globaal
    var quali_colormap=chroma.scale('Dark2');
    for (var i=0; i<nr_heatmaps; i++) {
        console.log('heatmap:',i,nr_heatmaps);
        h=new heatmap(data[i],opties[i],i);
        h.init_databuffers('heatmap_svg_'+i,'heatmap_canvas_'+i);
        h.mean_x=mean_x[i];
        h.median_x=median_x[i];
        h.xmean=xmean[i];
        h.ymean=ymean[i];
        h.sum_x=sum_x[i];
        h.sum_y=sum_y[i];
        var colormap_endpoint=quali_colormap(i/nr_heatmaps);
        var rgb=colormap_endpoint._rgb;
        var colortxt='rgb('+parseInt(rgb[0])+','+parseInt(rgb[1])+','+parseInt(rgb[2])+')';
        cat_colormap.push(colortxt);
        h.colormap=generate_colormap(colormap_endpoint, 20);
        h.draw_axes();                 
        heatmaps.push(h);    
    }


    set_gradient(opties[0]);    
    topnode.preAttributeChangedCallback=bin_alldata;    
    topnode.postAttributeChangedCallback=draw_heatmaps;        
    init_gradients();
    $('#cg_a').append('<svg id="legend" height="400" width="150"> <svg>');

    
    h=heatmaps[0];
    h.init_print();    
    h.init_stats();
    h.init_hist_xy();
    h.init_dotplot();
  //  h.init_display();     
    h.init_annotations();
    
    

    $('#cat_multiples').on('click',resize_cats);
    $('#cat_sharecolormap').on('click',toggle_colormap_sharing);
 //   Pixastic.debug=true;
    document.title =h.opties.title;
   // console.log('print=',print);
    if (print==true) {
        $('.leftbox').hide();
        $('.gradient_vars').hide();
        $('.hist_2d').hide();        
    } else {
        $('#sel_print').hide();
    }


    if (typeof (init_interactive) == 'function') { 
        init_interactive(); 
    }


 
}

$( document ).ready(init_page);