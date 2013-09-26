
var colormapname='';

var click_colormap=function click_colormap (evt) {
	colormapname=$(this).attr('data-colormap');

	colormap=colormaps[colormapname];
	console.log('colormap',colormapname);
	console.log('colormap',colormap);
	resize();
	return false;
}



function init_colormaps()
{

var html='<li class="sel_heading"> colormaps </li>';
for (var key in colormaps) {
  if (colormaps.hasOwnProperty(key)) {
    html+='<li class="colormapname" data-colormap="'+key+'">'+key+'</li>';
  }
}

$('#sel_colormap').html(html);
$('.colormapname').on('click',click_colormap);
$('.colormapname').on('mouseenter ',enter_selectie);
$('.colormapname').on('mouseout ',leave_selectie);
 
 for (colormapname in colormaps)  break;
 colormap=colormaps[colormapname];
}



function resize() {

if (num==1) {
	for (var i = 0,j=0, len = height * width * 4; i < len; i+=4,j+=1) {
    	val=data[j];
    	indexval=~~((val-minval)/(delta)*255);    
    	color=colormap[indexval];

    	mapdata[i] =  color[0];  // imgd[i];
    	mapdata[i+1] = color[1];  // imgd[i];
    	mapdata[i+2] = color[2];  // imgd[i];
    	mapdata[i+3] = 0xff; //i & 0x3f;  // imgd[i];
	}
	ctx.putImageData(imgData, 0, 0);
	return;
}

console.log("resize:",num);
	var val=0;
	var cx=0;
	var cy=0;
	var ptr=0;
	var newdata=[]
	var newdata2=[]

	console.log(height, width, num, typeof(height), typeof(width), typeof(num));
	for (var i=0; i<height; i+=num) {
		for (var j=0; j<width; j+=num) {		
			val=0;

			ptr=i*width+j;			
			for (cx=0; cx<num; cx++) {
				for (cy=0; cy<num; cy++) {
					val+=data[ptr+cx+cy*width];
					}
				}				//cy
			
			val=val/(cx*cy); // XXX weg?
			newdata.push(ptr);

			indexval=~~((val-minval)/(delta)*255);    
    		color=colormap[indexval];			
			for (cx=0; cx<num; cx++) {
				for (cy=0; cy<num; cy++) {
					ptr=((i+cy)*width+j+cx)*4;
					newdata2.push(ptr);
			    	mapdata[ptr] =  color[0]; //color[2];  // imgd[i];
    				mapdata[ptr+1] = color[1];  // imgd[i];
    				mapdata[ptr+2] = color[2];  // imgd[i];
    				mapdata[ptr+3] = 0xff; //i & 0x3f;  // imgd[i];
				} //cx
			}  //cy
		} //j
	}	//i
console.log("done");

	/*
	for (var i = 0,j=0, len = height * width * 4; i < len; i+=4,j+=1) {
    mapdata[i] = 80;
    mapdata[i+1] = 80;
    mapdata[i+2] = 80;
    mapdata[i+3] = 0xff; //i & 0x3f;  // imgd[i];
}*/

//console.log(data);
ctx.putImageData(imgData, 0, 0);

}


var enter_selectie=function enter_selectie (evt) {
	$(this).addClass('hover_selectie');
}
var leave_selectie=function enter_selectie (evt) {
	$(this).removeClass('hover_selectie');
}


var click_size=function click_size (evt) {
	num=parseInt($(this).attr('data-size'));
	resize();
	return false;
}

function init_sizes() {

	var html='<li class="sel_heading"> Sizes:</li>';
		

	html+='<li class="sizename" data-size="1">'+width+"x"+height+'</li>';
	numtable=[2,5,10,20,50,100,200,500,1000,2000,5000];
	j=0;
	num=numtable[0];
	while ((width/num>9) && (height/num)>9) {		
		html+='<li class="sizename" data-size="'+num+'">'+Math.floor(width/num)+"x"+Math.floor(height/num)+'</li>';
		j++;
		num=numtable[j];		
	}
	num=1;
	$('#sel_size').html(html);
	
  $('.sizename').on('click',click_size);
   $('.sizename').on('mouseenter ',enter_selectie);
   $('.sizename').on('mouseout ',leave_selectie);
 // console.log("initsize");
}