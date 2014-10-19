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


    heatmapnode=document.getElementById('canvasdiv');
    heatmapnode.innerHTML =template(heatmapdata);

}

function init_page() {
  
    
    var imgwidth=opties[0].imgwidth;
    var imgheight=opties[0].imgheight;

    console.log("init_page", imgwidth, imgheight);

    var nr_heatmaps=1;
    var heatmapdata={heatmaps:[0]};
    init_all_heatmaps(heatmapdata);
    


    for (i=0; i<nr_heatmaps; i++){
        h=new heatmap(data[i],opties[i]);
        h.init_databuffers('heatmap_svg_'+i,'heatmap_canvas_'+i);
        h.draw_axes();    
    }
    set_gradient(opties[0]);
    console.log(h);
    topnode.preAttributeChangedCallback=h.calc_minmax;    
    topnode.postAttributeChangedCallback=h.draw_heatmap;        
    init_gradients(); 


  //  init_manipulation();
    
    h.init_print();    
    h.init_stats();
    h.init_hist_xy();
    h.init_dotplot();
    if (opties.use_dots) {
        console.log('kill gradient');
        $('.colormap-gradient').css("display","none");   
        $('.dotplot-controls').css("display","");     
    } else {
        $('.dotplot-controls').css("display","none");
    }
 //   Pixastic.debug=true;
    document.title =opties[0].title;
    console.log('print=',print);
    if (print==true) {
        $('.leftbox').hide();
        $('.gradient_vars').hide();
        $('.hist_2d').hide();
    }
}

$( document ).ready(init_page);