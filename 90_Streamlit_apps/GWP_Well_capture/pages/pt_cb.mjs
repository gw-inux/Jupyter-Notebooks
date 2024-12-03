
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

export default function({sl_dict,pt_src, f, pt_d, ptl_src
                        }){
    if (pt_d.active == true){
    	//collect slider values
    	var q = sl_dict['Pumping'].value/10**9 //cubic km/s 
    	var k = 10**sl_dict['Conductivity'].value/1000 //km/s
    	var i = 10**sl_dict['Gradient'].value
    	var b = sl_dict['Thickness'].value/1000 //km
    	var por = sl_dict['Porosity'].value //porosity
    	

        function calcVx(x,y,i,q,b,k,n){
            var gr = i-(q*x)/(2*Math.PI*b*k*(x**2+y**2))
            return gr*k/n
            }
        function calcVy(x,y,q,b,k,n){
            var gr = -(q*y)/(2*Math.PI*b*k*(x**2+y**2))
            return gr*k/n
            }
        function calcH(x,y,i,q,b,k){
            var rgt = -i*(x-1000) 
            var wt = q/(2*Math.PI*b*k)*Math.log((x**2+y**2)**0.5/1000)
            return {'rgt':rgt,'wt':wt, 'h':rgt+wt}
            }
        
        var xi = pt_src.data['x'][0]
        var yi = pt_src.data['y'][0]

        var vx = calcVx(xi,yi,i,q,b,k,por)
        var vy = calcVy(xi,yi,q,b,k,por)
        var v = (vx**2+vy**2)**0.5
        var xr = f.x_range.end-f.x_range.start
        var yr = f.y_range.end-f.y_range.start
        var fr = d3.max([xr,yr])
        var td = fr/1000/v //initial time step
        
        //initialize results arrays
        var vxa = [vx]
        var vya = [vy]
        var ta = [0]
        var xa = [xi]
        var ya = [yi]
        var ha = [calcH(xi,yi,i,q,b,k)['h']*1000]
        var xn = xi+vx*td
        var yn = yi+vy*td
        do {
            var hn = calcH(xn,yn,i,q,b,k)['h']*1000
            
            //termination criteria one, next head is higher than current
            if (hn>ha[ha.length-1]){
                break
                }
                
            xa.push(xn)
            ya.push(yn)
            ta.push(td)
            vx = calcVx(xn,yn,i,q,b,k,por)
            vy = calcVy(xn,yn,q,b,k,por)
            vxa.push(vx)
            vya.push(vy)
            
            

            
            ha.push(hn)
            v = (vx**2+vy**2)**0.5
            td = fr/1000/v

            xn = xn+vx*td
            yn = yn+vy*td
            //termination criteria two --> reaches the far field
            if (xn > 1000){
                break
                }
               // }
            } while (xa.length<1001)
       ptl_src.data = {'x':xa,'y':ya,'t':d3.cumsum(ta).map(x=>x/60/60/24/365)}
        }
	    	
}