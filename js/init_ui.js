// https://developer.mozilla.org/en-US/docs/Web/API/FileReader#readAsDataURL%28%29

var c,s,ctx;
var print=false;

// printinfo hier


function init_page() {
  
    console.log("init:",imgwidth,imgheight);

    defaultsettings={
        colormapname: opties.colormap,
        gradient_min: opties.gradmin,
        gradient_max: opties.gradmax,
        gradient_steps: opties.gradsteps,
        transform: opties.transform,
        show_size: 'true',
        xpixels: xpixels,
        ypixels: ypixels
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
    init_gradients(); 
    

  //  init_manipulation();
    
    init_print();
    draw_axes ();        
    init_stats();
    init_hist_xy();
    if (opties['use_dots']) {
        console.log('kill gradient');
        $('.colormap-gradient').css("display","none");
    }
 //   Pixastic.debug=true;
    document.title =title;
    console.log('print=',print);
    if (print==true) {
        $('.leftbox').hide();
        $('.gradient_vars').hide();
        $('.hist_2d').hide();
    }
}

$( document ).ready(init_page);