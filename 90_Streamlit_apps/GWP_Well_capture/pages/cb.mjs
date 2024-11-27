import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7.9/+esm"
import * as d3Contour from 'https://cdn.jsdelivr.net/npm/d3-contour@4.0.2/+esm'

// js function equivalent to np.linspace
function makeArr(startValue, stopValue, cardinality) {
  var arr = [];
  var step = (stopValue - startValue) / (cardinality - 1);
  for (var i = 0; i < cardinality; i++) {
	arr.push(startValue + (step * i));
  }
  return arr;
}

//given bnds {xmin: , xmax: , ymin: , ymax: }, Xdim = number of columns, Ydim number of rows
// returns an array of coordinate objects in a grid  
function genGridPts(bnds,Xdim,Ydim){
  var xa = makeArr(bnds.xmin,bnds.xmax,Xdim)
  var ya = makeArr(bnds.ymin,bnds.ymax,Ydim)
  var cx = d3.cross(ya,xa).map(v=>{return {'x':v[1],'y':v[0]}})
  return cx
    }
    
function euclideanDistance(v,w) {return Math.sqrt(Math.pow(w.x-v.x,2)+Math.pow(w.y-v.y,2))}

//transforms columndatasource data to array of objects
function cds_to_objarray(cds_data){
  var keys = Object.keys(cds_data)
  var z = d3.transpose(Object.values(cds_data))
  var o = z.map(x=>Object.assign(...keys.map((k, i) => ({[k]: x[i]}))))
  return o}
  
//transforms array of objects to columndatasource "dictionary"/object 
function objarray_to_cds(objarray){
  var a = d3.transpose(objarray.map(x=>Object.values(x)))
  if (a.length>0){
    var d = Object.assign(...Object.keys(objarray[0]).map((k, i) => ({[k]: a[i]})))
    }
  return d
  }
  
//translates a d3 contour result into multiline-ready CDS data
function contours_to_cds(d3_contour){
    var cxs = []
    var cys = []
    var cv = []
    for (var vi=0;vi<d3_contour.length;vi++){                       
     		   for (var pi=0; pi<d3_contour[vi].coordinates.length;pi++){
     			  for (var ppi = 0; ppi<d3_contour[vi].coordinates[pi].length;ppi++){                                  
     					  var xy = d3.transpose(d3_contour[vi].coordinates[pi][ppi])
     					  cxs.push(xy[0])
     					  cys.push(xy[1])
     					  cv.push(d3_contour[vi].value)
     					  }
     					  }
     				   }
    return {'z':cv,'xs':cxs,'ys':cys}
    }



export default function({src,sl_dict,f,w_src,w_lbl,c_src,c_lbl
                        ,hr_src,color_bar,rb
                        }){
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
    
    //build and evaluation grid for drawdown
    var xr = f.x_range.end-f.x_range.start
    var yr = f.y_range.end-f.y_range.start
    var bnds = {'xmin':f.x_range.start-xr*0.1,'xmax':f.x_range.end+xr*0.1
        ,'ymin':f.y_range.start-yr*0.1,'ymax':f.y_range.end+yr*0.1}
    var nx  = 200
    var ny = 200
    var grd = genGridPts(bnds,nx,ny)

    var rp = {'x':1000,'y':0, 'h':0} //reference point
    //calc head at well
    var wrft = i*(1000-0) 
    var wt = q/(2*Math.PI*b*k)*Math.log(1000/1e-6) //calc drawdown from well, reference point 1000 km away
    var hwell = wrft-(wt*1000)
    
    for (var gi = 0; gi< grd.length; gi++){
        
        // where b, k and i are aquifer thickness, hyd. cond., and regional gradient respectively
        
        var dw = euclideanDistance(grd[gi],{'x':0,'y':0}) //calc distance of location to well
        var wt = q/(2*Math.PI*b*k)*Math.log(1000/dw) //calc drawdown from well, reference point 1000 km away
        
        var rf = b*k*i //"regional flow Q_0", thickness * k * i, just darcy's law???
        var rft = i*(1000-grd[gi].x) //regional flow component

        grd[gi]['rft'] = rft*1000
        grd[gi]['wt'] = wt*1000
        grd[gi]['h'] = (grd[gi]['rft']-grd[gi]['wt'])-hwell
        
        //deriving velocity field 
        //partial derivate wrt x of h = f(x,y)
        grd[gi]['vx'] = i*(1000-1)+(q*grd[gi]['x'])/(Math.PI*b*k*(grd[gi]['x']**2+grd[gi]['y']**2))
        //partial derivate wrt y of h = f(x,y)
        grd[gi]['vy'] = (q*grd[gi]['y'])/(Math.PI*b*k*(grd[gi]['x']**2+grd[gi]['y']**2))
        grd[gi]['v'] = (grd[gi]['vx']**2+grd[gi]['vy']**2)**0.5*1000 //to m/s
        }
        
    var ctr = d3Contour.contours().thresholds(10).size([nx,ny])
    if (rb.active==0){
        var contours = contours_to_cds(ctr(grd.map(x=>x.wt)))
        color_bar.title = 'Drawdown (m)'
        }
    else {
        var contours = contours_to_cds(ctr(grd.map(x=>x.h)))
        color_bar.title = 'Hydraulic Head (m, relative to well)'
        }
    
    //back to coords
    contours['xs'] = contours['xs'].map(x=>x.map(xx=>xx/nx*(bnds['xmax']-bnds['xmin'])+bnds['xmin']))
    contours['ys'] = contours['ys'].map(y=>y.map(yy=>yy/ny*(bnds['ymax']-bnds['ymin'])+bnds['ymin']))  
    hr_src.data=contours
    console.log(grd)  
          	
}