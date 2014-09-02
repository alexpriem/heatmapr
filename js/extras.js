


function denoise () {
	console.log("denoise");
	var img= document.getElementById("heatmap_canvas");
	var newimg=Pixastic.process(img,"removenoise",{});
	console.log('newimg', newimg);
}


function sharpen () {
	console.log("sharpen");
	var img= document.getElementById("heatmap_canvas");
	var newimg=Pixastic.process(img,"sharpen",{amount:0.5});
}



function pointilize () {
	console.log("pointilize");
	var img= document.getElementById("heatmap_canvas");
	var newimg=Pixastic.process(img, "pointillize", {radius:5, density:1.5, noise:1.0, transparent:false});
}

function edge () {
	console.log("edge");
	var img= document.getElementById("heatmap_canvas");
	var newimg=Pixastic.process(img, "edges", {mono:true,invert:true});
}

function blurfast () {
	console.log("blurfast");
	var img= document.getElementById("heatmap_canvas");
	var newimg=Pixastic.process(img, "blurfast", {amount:0.5});
}


function lighten () {
	console.log("lighten");
	var img= document.getElementById("heatmap_canvas");
	var newimg=Pixastic.process(img, "lighten", {amount:0.5});
}





function init_manipulation () {

	$('#sharpen').on('click',sharpen);
	$('#denoise').on('click',denoise);
	$('#pointilize').on('click',pointilize);	
	$('#edge').on('click',edge);
	$('#blur').on('click',blurfast);
	$('#lighten').on('click',lighten);
	
	$('.man').on('mouseenter ',enter_selectie);
  	$('.man').on('mouseout ',leave_selectie);
}
