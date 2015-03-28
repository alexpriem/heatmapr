// https://developer.mozilla.org/en-US/docs/Web/API/FileReader#readAsDataURL%28%29

var c,s,ctx;
var print=false;
var datasets=null;
// printinfo hier


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
    heatmapnode.innerHTML =template(heatmapdata);

    var opt=opties[0];    
    var multi_cols=opt.multi_cols;
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
        xpos+=width;
        if (j==multi_cols) {
            for (k=multi_cols; k>0; k--) {
                opties[i-k+1].xlabel='';                
            }
            ypos+=height;
            xpos=0;
            j=0;
        }

     //   $('#heatmap_container_'+i).css('left',xpos);       
    }
    xpos=multi_cols*width;
    $('.colormap-gradient').css('margin-left',xpos+'px')
}


var bin_alldata=function () {

	for (var i=0; i<nr_heatmaps; i++) {
        	heatmaps[i].bin_data();
	    }
}

var draw_heatmaps=function() {

    for (var i=0; i<nr_heatmaps; i++) {
        console.log('draw_heatmaps:',data.length,i);
        heatmaps[i].draw_heatmap();
        console.log('draw_heatmaps:',data.length,i);
    }

}

function init_page() {
  
    console.log('init_page, # heatmaps:',data.length);    
    console.log('multimap',multimap);    

    if (multimap) {
        var heatmapinfo=[0];        
    } else {
        var heatmapinfo=[];    
        nr_heatmaps=data.length;        
        for (i=0; i<nr_heatmaps; i++) {heatmapinfo.push(i);}
    }

	datasets=data;
    var heatmapdata={heatmaps:heatmapinfo};
    init_all_heatmaps(heatmapdata);
    
    heatmaps=[];
    for (i=0; i<nr_heatmaps; i++) {
        h=new heatmap(data[i],opties[i]);
        h.init_databuffers('heatmap_svg_'+i,'heatmap_canvas_'+i);
        h.mean_x=mean_x[i];
        h.median_x=median_x[i];
        h.xmean=xmean[i];
        h.ymean=ymean[i];
        h.sum_x=sum_x[i];
        h.sum_y=sum_y[i];
        h.draw_axes(); 
        heatmaps.push(h);
    }

    var window_opties=opties[0];
    set_gradient(window_opties);
    //console.log(h);
    topnode.preAttributeChangedCallback=bin_alldata;    
    topnode.postAttributeChangedCallback=draw_heatmaps;        
    init_gradients(); 


  //  init_manipulation();
    
    h.init_print();    
    h.init_stats();
    h.init_hist_xy();
    h.init_dotplot();
    h.init_display();

    
 //   Pixastic.debug=true;
    document.title =window_opties.title;
    console.log('print=',print);
    if (print==true) {
        $('.leftbox').hide();
        $('.gradient_vars').hide();
        $('.hist_2d').hide();
        $('#IE9_hack').hide();
    } else {
        $('#sel_print').hide();
    }
}

$( document ).ready(init_page);