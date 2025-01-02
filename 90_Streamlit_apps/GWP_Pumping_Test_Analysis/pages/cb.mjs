import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7.9/+esm"
import cephes from 'https://cdn.jsdelivr.net/npm/cephes@2.0.0/+esm'
await cephes.compiled

// js function equivalent to np.linspace
function makeArr(startValue, stopValue, cardinality) {
  var arr = [];
  var step = (stopValue - startValue) / (cardinality - 1);
  for (var i = 0; i < cardinality; i++) {
	arr.push(startValue + (step * i));
  }
  return arr;
}

function well_function(u){
    return cephes.expn(1,u)
    }

function theis_u(T,S,r,t){
    return r**2*S/4/T/t
    }
    
function theis_s(Q,T,u){
    return Q/4/Math.PI/T*well_function(u)
    }
	
export default function({hr_src,ddr_src,obs_src,ddt_src,sl_dict}){
	//collect slider values
	var q = sl_dict['Q'].value
	var tr = 10**sl_dict['T'].value
	var s = 10**sl_dict['S'].value
	var t = 10**sl_dict['Time'].value
	
	//if statement resetting everything if q = 0
	if (q==0){
    	hr_src.data = {'r':[],'dd':[],'ir':[]}
    	ddr_src.data = {'x':[],'dd':[]}
    	ddt_src.data = {'t':[],'dd':[]}
    	return
    	}
	//compile dd(r) function for bisection method
	function ddr(r){
    	var u = theis_u(tr,s,r,t)
        var dd = theis_s(q,tr,u)
        return dd
    	}
    	
	//get dd @0.1 m
    var mdd = ddr(0.1)
    function bisection(tgt,a,b,f,epsilon){
        //tgt is goal
        //a is initial small guess that f(a) = tgt
        //b i initial big guess that f(b) = tgt
        //f is function
        //episilon is termination criteria (b-a < epsilon)
        while ((b-a)>epsilon){
            //find middle
            var m = (a+b)/2
            var res = f(m)
            if (res == tgt){
                break
                }
            else if (res<tgt){
                //under target, big guess becomes m 
                b = m
                }
            else {
                //over target, small guess becomes makeArr
                a = m
                }
            }
        return m
        }
    var r2 = 10**10 // big guess guess radius
    var r1 = 0 //small guess radius
    
    var tgts = makeArr(mdd/25,mdd,15)
    var rs = tgts.map(x=>bisection(x,r1,r2,ddr,0.01))
    
    hr_src.data = {'r':rs,'dd':tgts, ir:[...rs.slice(1),0]}
    
    //build drawdown vs distance plot
    var rs = makeArr(-rs[0],rs[0],1000)
    var dd = rs.map(x=>ddr(x))
    ddr_src.data = {'x':rs,'dd':dd}
    
    //drawdown vs time plot
    if (obs_src.data['x'].length>0){
        var xo = obs_src.data['x'][0]
        var yo = obs_src.data['y'][0]
        var r = (xo**2+yo**2)**0.5
        //drawdown at that radius
        var ddob = ddr(r)
        //add fields to obs_src
        obs_src.data['r'] = [r]
        obs_src.data['dd'] = [ddob]
        obs_src.change.emit()
    	//compile dd(t) function
    	function ddt(t){
        	var u = theis_u(tr,s,r,t)
            var dd = theis_s(q,tr,u)
            return dd
        	}
        
        var ts = makeArr(1,t,1000)
        var dda = ts.map(x=>ddt(x))
        ddt_src.data = {'t':ts,'dd':dda}
        }
    
     
}