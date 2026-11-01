"""Reproduce the v2.4 hydraulic and long-arrival diagnostic.

Run: python scripts/audit_travel_times.py OUTPUT_JSON
No model parameters or equations are changed by this read-only audit.

CODE MAP — refresh with python scripts/update_code_index.py
  L0021  hydraulic_check
  L0063  sample_check
  L0095  main
END CODE MAP
"""
from pathlib import Path
from dataclasses import asdict
import sys,json
import numpy as np
from scipy.linalg import solve
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from dispersion_lab.model import Config,build_network,network_reference,simulate,mass_counts


def hydraulic_check(c):
    net=build_network(c)
    u,v=net.edges.T
    length=np.linalg.norm(net.xy[v]-net.xy[u],axis=1)
    g=np.pi*net.radii**4/(8e-3*length)
    # A separate dense positive-definite solve checks the sparse-solver result.
    matrix=np.zeros((len(net.xy),len(net.xy)))
    for a,b,conductance in zip(u,v,g):
        matrix[a,a]+=conductance;matrix[b,b]+=conductance
        matrix[a,b]-=conductance;matrix[b,a]-=conductance
    free=np.setdiff1d(np.arange(len(net.xy)),np.r_[0,net.outlets])
    pressure=np.zeros(len(net.xy));pressure[0]=c.pressure_pa
    pressure[free]=solve(matrix[np.ix_(free,free)],-matrix[free,0]*c.pressure_pa,assume_a='pos')
    independent_flow=g*(pressure[u]-pressure[v])
    assert np.max(abs(independent_flow-net.flow))/net.inlet_flow<1e-10
    lookup={tuple(sorted((int(a),int(b)))):e for e,(a,b) in enumerate(net.edges)}
    max_time_error=0.
    for a,branches in enumerate(net.outgoing):
        if not branches:continue
        assert abs(sum(p for _,p,_ in branches)-1)<1e-12
        flow_sum=sum(abs(net.flow[lookup[tuple(sorted((a,b)))]]) for b,_,_ in branches)
        for b,p,dt in branches:
            e=lookup[tuple(sorted((a,b)))]
            # Equivalent independent form: L / mean tube velocity.
            delta=net.pressure[a]-net.pressure[b]
            assert delta>0
            speed=net.radii[e]**2*delta/(8e-3*length[e])
            expected=length[e]/speed
            assert np.isclose(p,abs(net.flow[e])/flow_sum,rtol=1e-12)
            assert np.isfinite(dt) and dt>0
            max_time_error=max(max_time_error,abs(dt/expected-1))
    ref=network_reference(net)
    assert abs(ref['outlet_probability'].sum()-1)<1e-10
    assert abs(net.volume/net.inlet_flow/ref['mean_transit']-1)<1e-10
    return {
      'config':asdict(c),'dense_sparse_pressure_difference_over_inlet':float(np.max(abs(pressure-net.pressure))/c.pressure_pa),
      'dense_sparse_flow_difference_over_inlet_flow':float(np.max(abs(independent_flow-net.flow))/net.inlet_flow),
      'max_relative_L_over_velocity_time_error':max_time_error,
      'relative_nodal_residual':net.residual,'relative_flow_imbalance':net.imbalance,
      'exact_mean_transit_s':ref['mean_transit']}


def sample_check(c):
    run=simulate(c);net=run.network
    arrivals=np.quantile(run.arrival,[0,.5,.9,.95,.99,1])
    up=0;repeats=0
    for path,times in zip(run.paths,run.times):
        valid=np.isfinite(times);path=path[valid];times=times[valid]
        repeats+=len(path)-len(set(path))
        assert np.all(np.diff(net.pressure[path])<0)
        assert np.all(np.diff(times)>0)
        assert path[-1] in net.outlets
        up+=np.count_nonzero(np.diff(run.xy[path,1])<0)
    i=int(np.argmax(run.arrival));valid=np.isfinite(run.times[i])
    path=run.paths[i,valid];times=run.times[i,valid];dt=np.diff(times)
    k=int(np.argmax(dt));a,b=path[k:k+2]
    lookup={tuple(sorted((int(a),int(b)))):e for e,(a,b) in enumerate(net.edges)}
    e=lookup[tuple(sorted((int(a),int(b))))]
    dense=hydraulic_check(c)
    assert repeats==0 and mass_counts(run,run.end_time)==(0,0,c.particles)
    return {
     'config':asdict(c),'arrival_quantiles_s':dict(zip(['min','median','p90','p95','p99','max'],map(float,arrivals))),
     'p95_on_8_second_clock_s':float(8*arrivals[3]/run.end_time),
     'p95_on_60_second_clock_s':float(60*arrivals[3]/run.end_time),
     'upward_transitions_in_cohort':int(up),'repeated_nodes':repeats,
     'latest_particle':{'index_zero_based':i,'connections':len(path)-1,'upward_connections':int(np.count_nonzero(np.diff(run.xy[path,1])<0)),
      'arrival_s':float(run.arrival[i]),'slowest_connection':{
       'from_node':int(a),'to_node':int(b),'from_z_mm':float(net.xy[a,1]*1e3),'to_z_mm':float(net.xy[b,1]*1e3),
       'radius_mm':float(net.radii[e]*1e3),'pressure_drop_Pa':float(net.pressure[a]-net.pressure[b]),
       'flow_m3_per_s':float(abs(net.flow[e])),'transit_s':float(dt[k]),
       'fraction_of_particle_transit':float(dt[k]/(run.arrival[i]-run.release[i]))}},
     'hydraulics':dense}


def main():
    if len(sys.argv)!=2:raise SystemExit('Specify the output JSON path.')
    cases=[(2,.5,0.,7,.05),(2,.9,.4,7,2.),(20,.9,.4,19,.05),
           (40,.5,0.,7,2.),(40,.9,0.,7,.05),(40,.9,.4,19,2.)]
    checks=[hydraulic_check(Config(mode='grains',rows=r,packing=p,grain_variation=v,medium_seed=s,pressure_pa=dp)) for r,p,v,s,dp in cases]
    samples=[]
    for rows,packing,variation in [(20,.75,.25),(40,.75,.25),(40,.9,.4)]:
        samples.append(sample_check(Config(mode='grains',rows=rows,particles=10010,packing=packing,grain_variation=variation)))
        print('Checked',rows,'rows, factor',packing,'variation',variation,flush=True)
    result={'hydraulic_edge_cases':checks,'complete_cohorts':samples}
    target=Path(sys.argv[1]);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(target)


if __name__=='__main__':main()
