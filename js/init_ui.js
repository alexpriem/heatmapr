// https://developer.mozilla.org/en-US/docs/Web/API/FileReader#readAsDataURL%28%29

var c,s,ctx;
var print=false;

// printinfo hier


function init_page() {
  

    var imgwidth=opties.imgwidth;
    var imgheight=opties.imgheight;
    console.log("init:",imgwidth,imgheight);

    defaultsettings={
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
    //console.log(defaultsettings);

    topnode=document.getElementById('cg_a');
     for (var keyword in defaultsettings) {
      if (defaultsettings.hasOwnProperty(keyword)) {                      
            topnode.setAttribute(keyword, defaultsettings[keyword]);                      
      }
  }
  

    c=document.getElementById("heatmap_canvas");
    c.setAttribute("width", imgwidth);
    c.setAttribute("height", imgwidth);
    s=document.getElementById("heatmap_svg");
    s.setAttribute("width", imgwidth*2+100);
    s.setAttribute("height", imgheight+100);
    
    ctx = c.getContext('2d');  
    topnode.postAttributeChangedCallback=draw_heatmap;  
    topnode.preAttributeChangedCallback=calc_minmax;
    init_databuffers();
    draw_axes();    
    init_gradients(); 


  //  init_manipulation();
    
    init_print();    
    init_stats();
    init_hist_xy();
    init_dotplot();
    if (opties['use_dots']) {
        console.log('kill gradient');
        $('.colormap-gradient').css("display","none");   
        $('.dotplot-controls').css("display","");     
    } else {
        $('.dotplot-controls').css("display","none");
    }
 //   Pixastic.debug=true;
    document.title =opties.title;
    console.log('print=',print);
    if (print==true) {
        $('.leftbox').hide();
        $('.gradient_vars').hide();
        $('.hist_2d').hide();
    }
}

$( document ).ready(init_page);