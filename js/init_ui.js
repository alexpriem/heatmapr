// https://developer.mozilla.org/en-US/docs/Web/API/FileReader#readAsDataURL%28%29

var c,s,ctx;
var print=false;

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

    
    startpos=200;
    xpos=0;
    ypos=50;
    var i=0;
    var j=0;
    for (i=0,j=0; i<data.length; i++,j++) {
        $('#heatmap_container_'+i).css('margin-left',xpos);        
        $('#heatmap_container_'+i).css('top',ypos);        
        xpos+=200;
        if (j>2) {
            ypos+=200;
            xpos=0;
            j=-1;
        }

     //   $('#heatmap_container_'+i).css('left',xpos);       
    }
}


var calc_minmaxes=function () {

    for (var i=0; i<data.length; i++) {
        heatmaps[i].calc_minmax();
    }
}

var draw_heatmaps=function() {

    for (var i=0; i<data.length; i++) {
        console.log('draw_heatmaps:',data.length,i);
        heatmaps[i].draw_heatmap();
        console.log('draw_heatmaps:',data.length,i);
    }

}

function init_page() {
  
    
    var nr_heatmaps=data.length;
    console.log(data.length);
    var heatmapinfo=[];    
    for (i=0; i<nr_heatmaps; i++) {heatmapinfo.push(i);}

    var heatmapdata={heatmaps:heatmapinfo};
    console.log(heatmapinfo, heatmapdata);
    init_all_heatmaps(heatmapdata);
    
    heatmaps=[];
    for (i=0; i<nr_heatmaps; i++) {
        h=new heatmap(data[i],opties[i]);
        h.init_databuffers('heatmap_svg_'+i,'heatmap_canvas_'+i);
        h.mean_x=mean_x[i];
        h.median_x=median_x[i];
        h.xmean=xmean[i];
        h.ymean=ymean[i];
        
        h.draw_axes(); 
        heatmaps.push(h);
    }

    var window_opties=opties[0];
    set_gradient(window_opties);
    console.log(h);
    topnode.preAttributeChangedCallback=calc_minmaxes;    
    topnode.postAttributeChangedCallback=draw_heatmaps;        
    init_gradients(); 


  //  init_manipulation();
    
    h.init_print();    
    h.init_stats();
    h.init_hist_xy();
    h.init_dotplot();
    if (window_opties.use_dots) {
        console.log('kill gradient');
        $('.colormap-gradient').css("display","none");
        $('.dotplot-controls').css("display","");     
    } else {
        console.log('kill dotplot');
        $('.dotplot-controls').css("display","none");
    }
 //   Pixastic.debug=true;
    document.title =window_opties.title;
    console.log('print=',print);
    if (print==true) {
        $('.leftbox').hide();
        $('.gradient_vars').hide();
        $('.hist_2d').hide();
        $('#IE9_hack').hide();
    }
}

$( document ).ready(init_page);