
// http://rosettacode.org/wiki/Matrix_Transpose#JavaScript
function Matrix(ary) {
    this.mtx = ary
    this.height = ary.length;
    this.width = ary[0].length;
}

 
Matrix.prototype.toString = function() {
    var s = []
    for (var i = 0; i < this.mtx.length; i++) 
        s.push( this.mtx[i].join(",") );
    return s.join("\n");
}
 
// returns a new matrix
Matrix.prototype.transpose = function() {
    var transposed = [];
    for (var i = 0; i < this.width; i++) {
        transposed[i] = [];
        for (var j = 0; j < this.height; j++) {
            transposed[i][j] = this.mtx[j][i];
        }
    }
    return new Matrix(transposed);
}

// http://rosettacode.org/wiki/Matrix_multiplication#JavaScript
// returns a new matrix
Matrix.prototype.mult = function(other) {
    if (this.width != other.height) {
        throw "error: incompatible sizes";
    }
 
    var result = [];
    for (var i = 0; i < this.height; i++) {
        result[i] = [];
        for (var j = 0; j < other.width; j++) {
            var sum = 0;
            for (var k = 0; k < this.width; k++) {
                sum += this.mtx[i][k] * other.mtx[k][j];
            }
            result[i][j] = sum;
        }
    }
    return new Matrix(result); 
}



 
var a = new Matrix([[1,2],[3,4]])
var b = new Matrix([[-3,-8,3],[-2,1,4]]);
print(a.mult(b));


Xn= 95.047;
Yn= 100.0;
Zn= 108.883;

transM = [[0.4124564, 0.2126729, 0.0193339], 
        [0.3575761, 0.7151522, 0.1191920],
        [0.1804375, 0.0721750, 0.9503041]];


 function rgblinear (rgb) {

 	rgblinear=[0,0,0];

    for (i=0; i<3; i++) {
    	value=rgb[i];
    	if (value> 0.04045) {
    		  value = Math.power( value + 0.055 ) / 1.055 , 2.4);
    	} else {
    		value= value/12.92;
    	}
    	rgblinear[i]=value*100;
    }
   return rgblinear; 	
 }


function sRGB (rgblinear) {

 	rgb=[0,0,0];

    for (i=0; i<3; i++) {
    	value=value/100;
    	if (value > 0.00313080495356037152) {
    		value = (1.055 * Math.power(value,1./2.4) ) - 0.055	
    	} else {
    		value= value*12.92;
    	}
    	rgb[i]=parseInt(value*255);
    }
   return rgb; 	
 }



  function generateColorMap(RGB1, RGB2, divide) {
        /*
        Generate the complete diverging color map using the Moreland-technique
        from RGB1 to RGB2, placing "white" in the middle. The number of points
        given by "numPoints" controls the resolution of the colormap. The 
        optional parameter "divide" gives the possibility to scale the whole
        colormap, for example to have float values from 0 to 1.
        */
        
        // calculate
        scalars = np.linspace(0., 1., self.numColors);
        RGBs = np.zeros((self.numColors, 3));
        for (i=0; i<numColors; i++) {
        	s=scalars[i];
            RGBs[i] = interpolateColor(RGB1, RGB2, s)
        return RGBs/divide;

 }


  var RGB1 = [59, 76, 192];
  var RGB2 = [180, 4, 38];
  var numColors=33;
  var divide=255;

  colormap = generateColorMap(RGB1, RGB2, numColors, divide);