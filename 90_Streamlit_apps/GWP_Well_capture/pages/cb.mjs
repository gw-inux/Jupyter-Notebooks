// js function equivalent to np.linspace
function makeArr(startValue, stopValue, cardinality) {
  var arr = [];
  var step = (stopValue - startValue) / (cardinality - 1);
  for (var i = 0; i < cardinality; i++) {
	arr.push(startValue + (step * i));
  }
  return arr;
}

// import * as d3 from "https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js"
import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7.9/+esm"


export default function({src,sl_dict,f}){
	//collect slider values
	var q = sl_dict['Pumping'].value
	var k = 10**sl_dict['Conductivity'].value
	var i = 10**sl_dict['Gradient'].value
	var b = sl_dict['Thickness'].value

	//get ymax_conf and x0_conf
	var ymax = q/(2*k*i*b)
	var x0 = q/(2*Math.PI*k*i*b)

	//calculate array for y based on ymax
	var ya = makeArr(-ymax*0.999,ymax*0.999, 1000)
	//calculate array for x based on ya
	var xa = ya.map(y=>y/(Math.tan(2*Math.PI*k*i*b*y/q)))

	//update src
	src.data = {'x':xa, 'y':ya}
	src.change.emit()

	//calculate figure bounds
	f.x_range.end = x0*1.1
	f.x_range.start = x0*-25
	var yr = (f.x_range.end - f.x_range.start)/2
	f.y_range.start = -yr
	f.y_range.end = yr
}