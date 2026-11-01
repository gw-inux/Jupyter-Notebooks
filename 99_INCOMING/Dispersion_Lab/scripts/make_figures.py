"""Original teaching illustrations. Run from any cwd: python scripts/make_figures.py.

CODE MAP — refresh with python scripts/update_code_index.py
  L0023  clean
  L0028  save
  L0034  figures
  L0035  figures.t
END CODE MAP
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
from matplotlib.figure import Figure
from matplotlib.patches import Circle
from matplotlib.collections import LineCollection,PatchCollection
from dispersion_lab.model import Config,simulate,pin_reference
from dispersion_lab.experiment import prepare_board
OUT=Path(__file__).resolve().parents[1]/"assets"/"figures"
BLUE="#256c9b";ORANGE="#b56b26"


def clean(ax):
    ax.spines[["top","right"]].set_visible(False)
    ax.tick_params(labelsize=10)


def save(fig,name,lang):
    name=name+("_de" if lang=="de" else "")
    for fmt in ('png','svg'):
        fig.savefig(OUT/(name+'.'+fmt),dpi=180,bbox_inches="tight",facecolor="white")


def figures(lang):
    def t(en,de):return de if lang=="de" else en
    f=Figure(figsize=(8,3.3),layout="constrained");axes=f.subplots(1,2)
    run=simulate(Config(rows=6,particles=3,mode="variable",seed=42))
    axes[0].add_collection(LineCollection(run.xy[run.edges]*1e3,colors="#ccd0d2",lw=.7,zorder=0))
    axes[0].scatter(*(run.xy*1e3).T,s=7,color="#c5c8ca",zorder=1)
    axes[0].set_xlim(-6.6,6.6)
    for i,col in enumerate([ORANGE,"#793f84","#2c7550"]):
        xy=run.xy[run.paths[i]]*1e3
        axes[0].plot(xy[:,0],xy[:,1],"o-",color=col,lw=2,ms=4,label=str(i+1))
        axes[1].vlines(run.arrival[i],0,1,color=col,lw=3)
        axes[1].text(run.arrival[i],1.04,str(i+1),ha="center",color=col)
    axes[0].invert_yaxis();axes[0].set(xlabel=t("Transverse position (mm)","Querposition (mm)"),ylabel=t("Flowwise distance (mm)","Strecke in Fließrichtung (mm)"),title=t("Different pathways","Unterschiedliche Wege"))
    axes[0].legend(title=t("Particle","Teilchen"),frameon=False,fontsize=9)
    axes[1].set(xlim=(0,max(run.arrival)*1.25),ylim=(0,1.35),xlabel=t("Arrival time (s)","Ankunftszeit (s)"),title=t("Different arrival times","Unterschiedliche Ankunftszeiten"),yticks=[])
    for ax in axes:clean(ax)
    save(f,"space_time",lang)
    f=Figure(figsize=(8,3.4),layout="constrained");axes=f.subplots(1,2)
    for ax,n in zip(axes,[4,12]):
        ref=pin_reference(Config(rows=n));x=2*np.arange(n+1)-n
        ax.bar(x,ref['outlet_probability'],width=1.4,color=BLUE)
        ax.set(xlabel=t("Outlet position (mm)","Auslassposition (mm)"),ylabel=t("Probability (–)","Wahrscheinlichkeit (–)"),title=f"n = {n} · a = 1 mm")
        ax.text(.97,.94,t("Exact binomial","Exakt binomial"),transform=ax.transAxes,ha="right",va="top",fontsize=10)
        clean(ax)
    save(f,"binomial",lang)
    f=Figure(figsize=(8,4.8),layout="constrained");axes=f.subplots(2,2)
    cases=[("regular",0.,t("Fixed times · pulse","Feste Zeiten · Impuls")),("regular",6.,t("Fixed times · 6 s injection","Feste Zeiten · 6 s Zugabe")),("variable",0.,t("Variable times · pulse","Variable Zeiten · Impuls")),("variable",6.,t("Variable times · 6 s injection","Variable Zeiten · 6 s Zugabe"))]
    bins=np.arange(0,31,.5)
    for ax,(mode,d,title) in zip(axes.flat,cases):
        run=simulate(Config(mode=mode,injection_s=d,particles=10000))
        heights=np.histogram(run.arrival,bins)[0]/10000/np.diff(bins)
        ax.bar(bins[:-1],heights,width=.5,align="edge",color=BLUE)
        ax.set(title=title,xlabel=t("Arrival time (s)","Ankunftszeit (s)"),ylabel=t("Mass rate (s⁻¹)","Massenrate (s⁻¹)"),xlim=(0,30))
        ax.text(.96,.92,t("Variance:","Varianz:")+f" {run.reference['variance_arrival']:.2f} s²",transform=ax.transAxes,ha="right",va="top",fontsize=9)
        clean(ax)
    save(f,"arrival",lang)
    f=Figure(figsize=(8,3.6),layout="constrained");ax1,ax2=f.subplots(1,2)
    board=prepare_board(Config(mode="grains",rows=4))
    ax1.add_collection(PatchCollection([Circle((x*1e3,y*1e3),r*1e3) for x,y,r in board.network.grains],facecolors="#c7c7c4",edgecolors="#969995",lw=.5))
    ax1.add_collection(LineCollection(board.xy[board.edges]*1e3,colors=BLUE,lw=1))
    ax1.set(xlim=(-6,6),ylim=(5,-1),aspect="equal",xlabel="x (mm)",ylabel="z (mm)",title=t("Lattice and grey grains","Gitter und graue Körner"))
    for y,r in [(1.1,.75),(-1.1,.6)]:ax2.add_patch(Circle((0,y),r,fc="#c7c7c4",ec="#969995"))
    ax2.plot([-1.7,1.7],[0,0],color=BLUE,lw=2)
    ax2.annotate("",xy=(0,.35),xytext=(0,-.5),arrowprops={"arrowstyle":"<->","color":ORANGE,"lw":2})
    ax2.text(.2,-.3,t("Gap = 2r","Öffnung = 2r"),color=ORANGE,fontsize=11,bbox={"facecolor":"white","edgecolor":"none","pad":1})
    ax2.set(xlim=(-2,2),ylim=(-2,2),aspect="equal",title=t("Equivalent throat (schematic)","Ersatzverbindung (Schema)"));ax2.axis("off");clean(ax1)
    save(f,"grain",lang)


if __name__=="__main__":
    OUT.mkdir(exist_ok=True)
    for language in ("en","de"):figures(language)
    print("8 original figures generated in PNG and SVG.")
