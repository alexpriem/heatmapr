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
        transform: opties.transform
    };
    console.log(defaultsettings);

    topnode=document.getElementById('cg_a');
     for (var keyword in defaultsettings) {
      if (defaultsettings.hasOwnProperty(keyword)) {                      
            topnode.setAttribute(keyword, defaultsettings[keyword]);                      
      }
  }
  

    init_gradients(); 
    c=document.getElementById("heatmap_canvas");
    c.setAttribute("width", imgwidth);
    c.setAttribute("height", imgwidth);
    s=document.getElementById("heatmap_svg");
    s.setAttribute("width", imgwidth*2+100);
    s.setAttribute("height", imgheight+100);
    
    ctx = c.getContext('2d');  
    

  //  init_manipulation();
    init_databuffers();
    init_print();
    // copy img byte-per-byte into our ImageData
    draw_heatmap();
    draw_axes ();    
    //console.clear();
    init_hist_xy();
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