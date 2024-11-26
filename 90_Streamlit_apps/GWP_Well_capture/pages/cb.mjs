// js function equivalent to np.linspace
function makeArr(startValue, stopValue, cardinality) {
  var arr = [];
  var step = (stopValue - startValue) / (cardinality - 1);
  for (var i = 0; i < cardinality; i++) {
	arr.push(startValue + (step * i));
  }
  return arr;
}

import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7.9/+esm"

export default function({src,sl_dict,f,w_src,w_lbl,c_src,c_lbl}){
	//collect slider values
	var q = sl_dict['Pumping'].value/10**9 //cubic km/s 
	var k = 10**sl_dict['Conductivity'].value/1000 //km/s
	var i = 10**sl_dict['Gradient'].value
	var b = sl_dict['Thickness'].value/1000 //km

	//get ymax and x0_conf
	var ymax = q/(2*k*i*b)
	var x0 = q/(2*Math.PI*k*i*b)

	//calculate array for y based on ymax
	var ya = makeArr(-ymax*0.999,ymax*0.999, 1000)
	//calculate array for x based on ya
	var xa = ya.map(y=>y/(Math.tan(2*Math.PI*k*i*b*y/q))) //convert m to km

	//update src
	src.data = {'x':xa, 'y':ya}
	src.change.emit()

	//calculate figure bounds
	f.x_range.end = x0*1.1
	f.x_range.start = x0*-25
	var yr = (f.x_range.end - f.x_range.start)/2
	f.y_range.start = -yr
	f.y_range.end = yr
	
	//calculate max width
	var w = q/(k*i*b)
	
	//update max width annotation
	w_src.data={'x0':[x0*-22],'x1':[x0*-22],'y0':[-w/2], 'y1':[w/2]}
    w_lbl.visible = true
    w_lbl.text = 'Max Width = '+w.toFixed(2).toString()+' km'
    w_lbl.x = x0*-21.25
    
    //update culm pt annotation
    c_src.data={'x0':[0],'x1':[x0],'y0':[0], 'y1':[0]}
    c_lbl.visible = true
    c_lbl.text = 'X₀ =\n'+x0.toFixed(2).toString()+' km'
    c_lbl.x = -x0*1.7
    c_lbl.y = w*0.05
          	
}