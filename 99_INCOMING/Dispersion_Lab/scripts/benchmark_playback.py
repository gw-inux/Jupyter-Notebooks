"""Estimate current-renderer video costs from a small frame sample.

Run: python scripts/benchmark_playback.py OUTPUT_JSON
Estimates exclude encoding, Streamlit delivery and optimized artist reuse.

CODE MAP — refresh with python scripts/update_code_index.py
  L0013  Module configuration / entry point
END CODE MAP
"""
import sys,time,io,json
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
if len(sys.argv)!=2:raise SystemExit("Specify the output JSON path.")
from dispersion_lab.model import Config,simulate
from dispersion_lab.plots import board_figure,distribution_figure
reports=[]
for rows in (20,40):
 run=simulate(Config(mode='grains',rows=rows,particles=10010))
 durations=[];sizes=[]
 for fraction in (.02,.08,.16,.35,.65,.95):
  begin=time.perf_counter();size=0
  for fig in [board_figure(run,fraction*run.end_time,highlighted=10),distribution_figure(run,fraction*run.end_time,bins=60)]:
   buf=io.BytesIO();fig.savefig(buf,format='png',dpi=130);size+=buf.tell();fig.clear()
  durations.append(time.perf_counter()-begin);sizes.append(size)
 reports.append({'rows':rows,'particles':10010,'frames_measured':len(durations),'frame_pair_seconds':durations,'median_seconds':float(np.median(durations)), 'mean_seconds':float(np.mean(durations)), 'mean_png_bytes':float(np.mean(sizes)), 'estimated_render_seconds_for_60s_at_24fps':float(1440*np.mean(durations))})
 print(rows,'rows benchmark finished',flush=True)
Path(sys.argv[1]).write_text(json.dumps(reports,indent=2))
print(json.dumps(reports,indent=2))
