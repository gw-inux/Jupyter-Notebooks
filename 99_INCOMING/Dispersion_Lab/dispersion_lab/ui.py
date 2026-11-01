"""Reusable experiment pages. The host owns navigation and page configuration.

Canonical values live in page-specific dictionaries, independently of widgets.
Language changes and navigation can recreate widgets without losing experiments.

CODE MAP — refresh with python scripts/update_code_index.py
  L0054  tr
  L0058  session
  L0067  control
  L0079  number
  L0084  slider
  L0089  reset
  L0096  cached_preview
  L0101  parameter_controls
  L0141  injection_controls
  L0150  start_playback
  L0160  particle_controls
  L0175  run_experiment
  L0198  experiment
  L0261  playback
  L0264  playback.frame
  L0276  playback.frame.reset_display
  L0279  playback.frame.complete_display
  L0284  playback.frame.play
  L0287  playback.frame.pause
  L0290  playback.frame.step
  L0306  playback.frame.seek
  L0348  particle_details
  L0356  particle_details.select_particle
  L0379  result_controls
  L0382  result_controls.save_comparison
  L0384  result_controls.clear_comparison
  L0422  render_page
  L0436  render_pinboard
END CODE MAP
"""
from __future__ import annotations
from dataclasses import asdict
import json
import time

import numpy as np
import pandas as pd
import streamlit as st

from .i18n import content, ui_text
from .model import Config, Run, mass_counts, particle_csv, simulate, summary, pin_reference, network_reference
from .experiment import prepare_board, particle_count, step_fraction, realization_config
from .presentation import apply_styles, section, show_figure, focus_transport
from .plots import board_figure, preview_figure, empty_figure, distribution_figure


# 1. Persistent state and controls ---------------------------------------------
def tr(en, de=None, **translations):
    return ui_text(en, de=de, **translations)


def session(page):
    return st.session_state.setdefault("disp_"+page, {
        "settings":asdict(Config(mode="grains" if page=="explore" else "regular", rows=20)), "highlighted":1, "background_each":0,
        "applied_background":0, "fraction":0., "playing":False,
        "play_seconds":60 if page=="explore" else 8, "traces":True, "paths":True, "bins":60,
        "stacked":False, "selected":1,
    })


def control(kind, data, field, label, page, **kwargs):
    """Persist values outside the lifecycle of any translated widget."""
    key=f"disp_{page}_{field}"
    if kind=="selectbox":
        options=kwargs["options"]
        value=st.selectbox(label,index=options.index(data[field]),key=key,**kwargs)
    else:
        value=getattr(st,kind)(label,value=data[field],key=key,**kwargs)
    data[field]=value
    return value


def number(saved,field,en,de,page,lo,hi,step,**kwargs):
    return control("number_input",saved,field,tr(en,de),page,
                   min_value=lo,max_value=hi,step=step,**kwargs)


def slider(saved,field,en,de,page,lo,hi,step,**kwargs):
    return control("slider",saved,field,tr(en,de),page,
                   min_value=lo,max_value=hi,step=step,**kwargs)


def reset(state):
    state["seek_revision"]=state.get("seek_revision",0)+1
    state["playing"]=False
    state["fraction"]=0.


@st.cache_data(show_spinner=False, max_entries=12)
def cached_preview(config):
    return prepare_board(config)


# 2. Preparation and run staging ----------------------------------------------
def parameter_controls(state,page):
    saved=state["settings"]
    with section(f"{page}_board",tr("Board and transport","Brett und Transport"),expanded=True,tone="blue"):
        labels={"regular":tr("Regular pinboard","Regelmäßiges Galtonbrett"),
                "variable":tr("Pinboard · variable travel times","Galtonbrett · variable Laufzeiten"),
                "grains":tr("Grey grains · pore network","Graue Körner · Porennetzwerk")}
        if page=="pinboard":
            control("selectbox",saved,"mode",tr("Model","Modell"),page,
                    options=["regular","variable"],format_func=labels.get)
        else:
            saved["mode"]="grains"
        left,right=st.columns(2)
        with left:
            slider(saved,"rows","Number of rows","Anzahl der Reihen",page,2,40,1)
        with right:
            number(saved,"spacing_mm","Lattice spacing a (mm)","Gitterabstand a (mm)",page,.2,3.,.1,format="%.1f")
        if saved["mode"]=="grains":
            left,right=st.columns(2)
            with left:
                slider(saved,"packing","Grain-size factor (–)","Korngrößenfaktor (–)",page,.5,.9,.05,
                       help=tr("Higher values narrow the gaps. This is not measured porosity.",
                               "Höhere Werte verengen die Öffnungen. Dies ist keine gemessene Porosität."))
                number(saved,"pressure_pa","Driving pressure difference (Pa)","Antreibende Druckdifferenz (Pa)",page,.05,2.,.05,format="%.2f")
            with right:
                slider(saved,"grain_variation","Grain-size variation (–)","Variation der Korngröße (–)",page,0.,.4,.05,
                       help=tr("Maximum fractional radius reduction. Increasing it also reduces mean grain size.",
                               "Maximale relative Radiusverringerung. Höhere Werte verringern auch die mittlere Korngröße."))
                number(saved,"medium_seed","Grain arrangement seed","Startwert der Kornanordnung",page,0,1_000_000,1)
            st.caption(tr("The grey grains determine equivalent pore openings. Water flow is solved at fixed driving pressure; all outlets have the same pressure.",
                          "Die grauen Körner bestimmen äquivalente Porenöffnungen. Die Strömung wird bei fester Druckdifferenz berechnet; alle Auslässe haben denselben Druck."))
        else:
            number(saved,"mean_step_s","Mean time per row (s)","Mittlere Zeit je Reihe (s)",page,.1,10.,.1,format="%.1f")
            if saved["mode"]=="variable":
                slider(saved,"time_cv","Travel-time coefficient of variation (–)","Variationskoeffizient der Laufzeit (–)",page,0.,1.5,.1,
                       help=tr("Step-time standard deviation / mean; positive lognormal times.",
                               "Standardabweichung / Mittelwert der Schrittzeit; positive lognormale Zeiten."))
            st.caption(tr("Each pin gives an independent 50% left / 50% right choice. Each horizontal and flowwise increment equals a.",
                          "An jedem Stift erfolgt eine unabhängige Entscheidung: 50 % links / 50 % rechts. Quer- und Längsschrittweite entsprechen a."))


def injection_controls(state,page):
    saved=state["settings"]
    with section(f"{page}_injection",tr("Injection and repetition","Zugabe und Wiederholung"),tone="quiet"):
        number(saved,"injection_s","Injection duration (s); 0 = pulse","Zugabedauer (s); 0 = Impuls",page,0.,1000.,1.,format="%.1f")
        number(saved,"seed","Particle realization seed","Startwert der Teilchenrealisierung",page,0,1_000_000,1)
        st.caption(tr("Release times are sampled uniformly within a finite injection interval. The particle seed changes trajectories; the grain seed changes the medium.",
                      "Bei endlicher Zugabedauer sind die Freisetzungszeiten gleichverteilt. Der Teilchenstartwert ändert die Wege; der Kornstartwert ändert das Medium."))


def start_playback(state):
    """Start/resume the display clock; never alter numerical travel times."""
    state["seek_revision"]=state.get("seek_revision",0)+1
    if state["fraction"]>=1:
        state["fraction"]=0.
    state["start_fraction"]=state["fraction"]
    state["wall_start"]=None
    state["playing"]=True


def particle_controls(state,page,guided):
    with section(f"{page}_particles",tr("Particles and injection plan","Teilchen und Zugabeplan"),expanded=True,tone="teal"):
        number(state,"highlighted","Highlighted particles","Hervorgehobene Teilchen",page,1,10,1)
        if guided:
            st.markdown(tr("**Fixed experiment:** 20 rows, a = 1 mm, 1 s per row, instantaneous pulse. Every particle arrives at 20 s. Start with one particle, then compare several paths.",
                           "**Festes Experiment:** 20 Reihen, a = 1 mm, 1 s je Reihe, momentane Impulszugabe. Alle Teilchen kommen bei 20 s an. Beginnen Sie mit einem Teilchen und vergleichen Sie anschließend mehrere Wege."))
        else:
            number(state,"background_each","Background particles per highlighted particle","Hintergrundteilchen je hervorgehobenem Teilchen",page,0,1000,50)
            total=particle_count(state["highlighted"],state["background_each"])
            st.caption(tr(f"Plan: {state['highlighted']} highlighted + {total-state['highlighted']:,} blue background particles = {total:,} in total.",
                          f"Plan: {state['highlighted']} hervorgehobene + {total-state['highlighted']:,} blaue Hintergrundteilchen = insgesamt {total:,}."))
            st.caption(tr("Begin with one, increase to ten, then add background particles. Run starts the full planned cohort. Rerun uses a new particle realization; the particle seed remains available for reproducible comparisons. Total mass stays 1; each marker carries 1/N.",
                          "Beginnen Sie mit einem Teilchen, erhöhen Sie auf zehn und ergänzen Sie dann Hintergrundteilchen. Start setzt die gesamte geplante Gruppe in Bewegung. Erneut starten verwendet eine neue Teilchenrealisierung; der Teilchenstartwert bleibt für reproduzierbare Vergleiche verfügbar. Gesamtmasse: 1; je Teilchen: 1/N."))


def run_experiment(state,page,config,guided=False):
    """Shared Run/Rerun callback; commit the complete result before rendering.

    No intermediate empty page or second full rerun is needed. The numerical
    engine remains deterministic for a given Config. Play uses the stored Run.
    """
    previous=state.get("run")
    config=realization_config(config,previous.config if previous else None)
    run=simulate(config)
    state["settings"]["seed"]=config.seed
    if not guided:
        st.session_state[f"disp_{page}_seed"]=config.seed
    state["run"]=run
    state["run_highlighted"]=state["highlighted"]
    state["selected"]=min(state["selected"],state["highlighted"])
    state["applied_background"]=0 if guided else state["background_each"]
    state["run_number"]=state.get("run_number",0)+1
    state["run_token"]=f"disp-transport-{page}-{time.monotonic_ns()}"
    state.pop("refresh_playback",None)
    reset(state)
    start_playback(state)


def experiment(page="explore",guided=False):
    state=session(page)
    apply_styles()
    if not guided:
        parameter_controls(state,page)
    particle_controls(state,page,guided)
    if not guided:
        injection_controls(state,page)
    config=(Config(rows=20,particles=state["highlighted"],seed=state["settings"]["seed"])
            if guided else Config(**{**state["settings"],
                "particles":particle_count(state["highlighted"],state["background_each"])}))
    old=state.get("run")
    pending=old is None or old.config!=config or state.get("run_highlighted")!=state["highlighted"]
    if pending:
        reset(state)
    with section(f"{page}_preview",tr("Initial board and injection plan","Ausgangszustand und Zugabeplan"),expanded=True,tone="sand"):
        try:
            board=cached_preview(config)
        except (ValueError,RuntimeError) as exc:
            st.error(tr("The board could not be prepared: ","Das Brett konnte nicht vorbereitet werden: ")+str(exc));return
        show_figure(preview_figure(board,state["highlighted"],st.session_state.get("language","en")),
                     tr("Initial board without transport","Ausgangszustand ohne Transport"),preview=True)
        st.caption(tr("The numbered tray shows particles ready for injection at one central inlet. Changing settings updates this preview without moving solute.",
                      "Die nummerierte Ablage zeigt Teilchen für die Zugabe am mittleren Einlass. Änderungen aktualisieren die Vorschau, ohne Stoff zu transportieren."))
        if board.network is None:
            st.caption(tr("The brown pegs sit just below the pale decision nodes. Grey lines show possible routes. The vertical display scale is twice the horizontal scale; coordinate values and travel times are unchanged. This is a schematic, not a collision simulation.",
                          "Die braunen Stifte liegen knapp unter den hellen Entscheidungsknoten. Graue Linien zeigen mögliche Wege. Die vertikale Darstellung ist gegenüber der horizontalen zweifach gestreckt; Koordinatenwerte und Laufzeiten bleiben unverändert. Dies ist eine schematische Darstellung, keine Kollisionssimulation."))
        else:
            st.caption(tr("Surrounding grains complete the picture of the subsurface but are decorative. Only the central triangular network carries calculated flow and solute; injection remains a point source.",
                          "Umgebende Körner vervollständigen das Bild des Untergrunds, sind aber rein illustrativ. Nur das zentrale dreieckige Netz transportiert berechnetes Wasser und gelösten Stoff; die Zugabe bleibt eine Punktquelle."))
            st.caption(tr("Equal horizontal and vertical scales preserve the circular grain shapes. Computed radii, distances and travel times are unchanged.",
                          "Gleiche horizontale und vertikale Maßstäbe erhalten die kreisförmigen Körner. Berechnete Radien, Abstände und Laufzeiten bleiben unverändert."))
            net=board.network
            st.caption(tr(f"Prepared water flow: {net.inlet_flow*1e9:.4g} µL/s · maximum throat Re = {net.max_reynolds:.3g}.",
                          f"Berechneter Wasserzufluss: {net.inlet_flow*1e9:.4g} µL/s · maximale Poren-Re = {net.max_reynolds:.3g}."))
        if not guided:
            reference=network_reference(board.network,config.injection_s) if board.network else pin_reference(config)
            st.caption(tr(f"Injection: 0–{config.injection_s:g} s. Expected mean transit: {reference['mean_transit']:.4g} s; transit standard deviation: {np.sqrt(reference['variance_transit']):.4g} s.",
                          f"Zugabe: 0–{config.injection_s:g} s. Erwartete mittlere Durchlaufzeit: {reference['mean_transit']:.4g} s; Standardabweichung: {np.sqrt(reference['variance_transit']):.4g} s."))
    st.subheader(tr("Observe the transport","Transport beobachten"),divider="blue",anchor=f"disp-observe-{page}")
    label=tr("Rerun highlighted particles","Hervorgehobene Teilchen erneut starten") if old else tr("Run highlighted particles","Hervorgehobene Teilchen starten")
    st.button(label,icon=":material/replay:" if old else ":material/play_arrow:",
              key=f"disp_{page}_run",type="primary",width="stretch",
              on_click=run_experiment,args=(state,page,config,guided))
    if old:
        st.caption(tr("Rerun starts a new particle realization with the settings above. Play replays the current result. Different random samples can still share the same outlet.",
                      "Erneut starten berechnet eine neue Teilchenrealisierung mit den obigen Einstellungen. Abspielen wiederholt das aktuelle Ergebnis. Verschiedene Zufallsstichproben können dennoch denselben Auslass erreichen."))
    if pending:
        st.info(tr("Ready to start. Run begins the animation using the settings above.",
                   "Bereit zum Start. Start beginnt die Animation mit den obigen Einstellungen."))
    if pending:
        show_figure(empty_figure(board,st.session_state.get("language","en")),
                     tr("Transport board ready","Transportbrett bereit"))
        return
    run=state["run"]
    st.caption(tr(f"Particle realization seed: {run.config.seed}",f"Startwert der Teilchenrealisierung: {run.config.seed}"))
    playback(run,state,page,guided)
    if not guided:
        result_controls(run,state,page)
    particle_details(run,state,page)


# 3. Playback and particle inspection -----------------------------------------
def playback(run,state,page,guided=False):
    interval=.8 if state["playing"] else None
    @st.fragment(run_every=interval)
    def frame():
        if state.pop("refresh_playback",False):
            st.rerun()  # Register the timer for the state already changed by a callback.
        if state["playing"]:
            if state["wall_start"] is None:
                state["wall_start"]=time.monotonic()
            fraction=state["start_fraction"]+(time.monotonic()-state["wall_start"])/state["play_seconds"]
            state["fraction"]=min(1.,fraction)
            if fraction>=1:
                state["playing"]=False
                st.rerun()  # Re-register without timer; always render final plots below.
        state["selected"]=min(state["selected"],state["run_highlighted"])
        def reset_display():
            reset(state)
            state["refresh_playback"]=True
        def complete_display():
            state["seek_revision"]=state.get("seek_revision",0)+1
            state["fraction"]=1.
            state["playing"]=False
            state["refresh_playback"]=True
        def play():
            start_playback(state)
            state["refresh_playback"]=True
        def pause():
            state["playing"]=False
            state["refresh_playback"]=True
        def step(direction):
            state["seek_revision"]=state.get("seek_revision",0)+1
            state["fraction"]=step_fraction(run,state["fraction"],state["selected"]-1,direction)
            state["playing"]=False
            state["refresh_playback"]=True
        with section(f"{page}_progress",tr("Progress through the experiment","Fortschritt des Experiments"),tone="blue"):
            left,middle,right=st.columns([1.7,3.6,1.7],vertical_alignment="bottom")
            left.button(tr("Start","Anfang"),icon=":material/first_page:",key=f"disp_{page}_reset",width="stretch",on_click=reset_display,
                        help=tr("Return to the beginning and pause. Play starts playback.","Zum Anfang zurückkehren und pausieren. Abspielen startet die Wiedergabe."))
            if state["playing"]:
                middle.progress(state["fraction"],text=tr("Progress","Fortschritt")+f" · {100*state['fraction']:.1f}%")
            else:
                # A new key after each playback command prevents a delayed browser
                # slider event from undoing a playback command or a new run.
                revision=state.get("seek_revision",0)
                seek_key=f"disp_{page}_seek_{revision}"
                def seek():
                    if state.get("seek_revision",0)==revision:
                        state["fraction"]=st.session_state[seek_key]/100
                        state["refresh_playback"]=True
                middle.slider(tr("Progress (%)","Fortschritt (%)"),0.,100.,
                              value=100*state["fraction"],step=.1,key=seek_key,on_change=seek)
            right.button(tr("Final result","Endergebnis"),key=f"disp_{page}_complete",width="stretch",on_click=complete_display)
            left,right=st.columns(2)
            left.button(tr("Play","Abspielen"),icon=":material/play_arrow:",key=f"disp_{page}_play",width="stretch",on_click=play,disabled=state["playing"],type="primary")
            right.button(tr("Pause","Pause"),icon=":material/pause:",key=f"disp_{page}_pause",width="stretch",on_click=pause,disabled=not state["playing"])
            left,right=st.columns(2)
            left.button(tr("Previous step","Vorheriger Schritt"),icon=":material/skip_previous:",key=f"disp_{page}_previous",width="stretch",on_click=step,args=(-1,),disabled=state["playing"] or state["fraction"]<=0)
            right.button(tr("Next step","Nächster Schritt"),icon=":material/skip_next:",key=f"disp_{page}_step",width="stretch",on_click=step,args=(1,),disabled=state["playing"] or state["fraction"]>=1)
        if not guided:
            with section(f"{page}_display",tr("Optional display settings","Optionale Darstellungseinstellungen"),tone="quiet"):
                slider(state,"play_seconds","Playback duration (screen seconds)","Wiedergabedauer (Bildschirmsekunden)",page,5,60,1,disabled=state["playing"])
                control("checkbox",state,"traces",tr("Show highlighted paths","Hervorgehobene Wege anzeigen"),page)
                control("checkbox",state,"paths",tr("Show possible pathways","Mögliche Wege anzeigen"),page)
                slider(state,"bins","Arrival-time histogram bins","Klassen des Ankunftszeit-Histogramms",page,10,100,1)
                control("checkbox",state,"stacked",tr("Stack result plots (mobile / larger labels)","Ergebnisgrafiken untereinander (mobil / größere Beschriftung)"),page)
                st.caption(tr("Pause to move the progress slider backward or forward. Display settings do not change transport. Next step follows the particle selected in the details below.",
                              "Pausieren Sie, um den Fortschrittsregler vor- oder zurückzubewegen. Darstellungsoptionen ändern den Transport nicht. Nächster Schritt folgt dem unten ausgewählten Teilchen."))
        current=run.end_time*state["fraction"]
        waiting,active,collected=mass_counts(run,current)
        st.caption(tr(f"t = {current:.4g} s · Not yet injected: {waiting:,} · In the board: {active:,} · Collected: {collected:,}",
                      f"t = {current:.4g} s · Noch nicht zugegeben: {waiting:,} · Im Brett: {active:,} · Gesammelt: {collected:,}"))
        language=st.session_state.get("language","en")
        show_figure(board_figure(run,current,language,state["traces"],state["paths"],
                     compact=state["stacked"],highlighted=state["run_highlighted"],selected=state["selected"]-1),
                     tr("Transport board","Transportbrett"),element_id=state["run_token"])
        show_figure(distribution_figure(run,current,language,state.get("baseline"),state["bins"],state["stacked"]),
                     tr("Outlet distributions","Auslassverteilungen"))
        caption=tr("Bars show arrivals so far, divided by the total mass of the full run. The complete temporal histogram has area 1; its height depends on bin width. Simultaneous arrivals occupy one finite bin.",
                   "Balken zeigen bisherige Ankünfte, geteilt durch die Gesamtmasse des vollständigen Laufs. Das vollständige Zeithistogramm hat die Fläche 1; seine Höhe hängt von der Klassenbreite ab. Gleichzeitige Ankünfte liegen in einer endlichen Klasse.")
        if not guided:
            caption+=tr(" A saved comparison always shows its complete run.",
                        " Ein gespeicherter Vergleich zeigt immer den vollständigen Lauf.")
        st.caption(caption)
        focus_transport(state["run_token"],f"disp-observe-{page}")
    frame()


def particle_details(run,state,page):
    """Paused inspection after the comparison tools; never shows stale live status."""
    with section(f"{page}_details",tr("Highlighted particles · position and pathway details","Hervorgehobene Teilchen · Position und Wegdetails"),tone="quiet"):
        if state["playing"]:
            st.caption(tr("Pause the animation to inspect positions and the selected pathway.",
                          "Pausieren Sie die Animation, um Positionen und den ausgewählten Weg zu prüfen."))
            return
        current=run.end_time*state["fraction"]
        def select_particle():
            state["selected"]=st.session_state[f"disp_{page}_selected"]
        control("selectbox",state,"selected",tr("Particle to inspect / step through","Teilchen für Details / Einzelschritte"),page,
                options=list(range(1,state["run_highlighted"]+1)),on_change=select_particle)
        records=[]
        for i in range(state["run_highlighted"]):
            status=tr("Waiting","Wartend") if current<run.release[i] else (tr("Collected","Gesammelt") if current>=run.arrival[i] else tr("Moving","In Bewegung"))
            records.append([i+1,status,run.release[i],run.arrival[i],run.exit_x[i]*1e3])
        st.dataframe(pd.DataFrame(records,columns=[tr("Particle","Teilchen"),tr("State","Zustand"),tr("Release (s)","Zugabe (s)"),tr("Arrival (s)","Ankunft (s)"),tr("Final outlet (mm)","Endauslass (mm)")]),hide_index=True,width="stretch")
        st.caption(tr("The table includes the calculated final arrival and outlet, even before playback reaches them.",
                      "Die Tabelle enthält die berechnete Endankunft und den Auslass, auch bevor die Wiedergabe sie erreicht."))
        i=state["selected"]-1
        valid=np.isfinite(run.times[i]);nodes=run.paths[i,valid]
        table={tr("Node","Knoten"):nodes,
               "x (mm)":run.xy[nodes,0]*1e3,"z (mm)":run.xy[nodes,1]*1e3,
               "t (s)":run.times[i,valid]}
        if run.network is not None:
            table[tr("Pressure potential (Pa)","Druckpotenzial (Pa)")]=run.network.pressure[nodes]
            table[tr("Next connection time (s)","Zeit der nächsten Verbindung (s)")]=np.r_[np.diff(run.times[i,valid]),np.nan]
        st.dataframe(pd.DataFrame(table),hide_index=True,width="stretch")


# 4. Results and exports ------------------------------------------------------
def result_controls(run:Run,state,page):
    with section(f"{page}_repeat",tr("Repeat, compare, and download","Wiederholen, vergleichen und herunterladen"),tone="quiet"):
        left,right=st.columns(2)
        def save_comparison():
            state["baseline"]=run
        def clear_comparison():
            state.pop("baseline",None)
        left.button(tr("Save this run for comparison","Diesen Lauf für Vergleich speichern"),key=f"disp_{page}_save",width="stretch",on_click=save_comparison)
        right.button(tr("Clear comparison","Vergleich entfernen"),key=f"disp_{page}_clear",width="stretch",on_click=clear_comparison)
        st.caption(tr("To compare two realizations, save the current run first, then start a new realization. Both Rerun buttons start a new sample with the current board and transport settings. The saved comparison remains until you replace or clear it.",
                      "Für den Vergleich zweier Realisierungen speichern Sie zuerst den aktuellen Lauf und starten anschließend eine neue Realisierung. Beide Schaltflächen zum erneuten Start beginnen eine neue Stichprobe mit den aktuellen Brett- und Transporteinstellungen. Der gespeicherte Vergleich bleibt bis zum Ersetzen oder Löschen erhalten."))
        st.button(tr("Rerun with new particle realization","Mit neuer Teilchenrealisierung erneut starten"),icon=":material/replay:",key=f"disp_{page}_new",type="primary",on_click=run_experiment,args=(state,page,run.config),width="stretch")
        baseline=state.get("baseline")
        if baseline:
            bc=baseline.config
            st.caption(tr(f"Saved: {bc.mode}; {bc.rows} rows; {bc.particles} markers; seed {bc.seed}.",
                          f"Gespeichert: {bc.mode}; {bc.rows} Reihen; {bc.particles} Teilchen; Startwert {bc.seed}."))
        st.caption(tr("Statistics and downloads describe the complete calculated run, including future arrivals in the animation. All particles have equal mass.",
                      "Statistik und Downloads beschreiben den vollständig berechneten Lauf, einschließlich künftiger Ankünfte in der Animation. Alle Teilchen haben die gleiche Masse."))
        ref=run.reference
        values=[
            [tr("Mean outlet position (mm)","Mittlere Auslassposition (mm)"),np.mean(run.exit_x)*1e3,ref["mean_x"]*1e3],
            [tr("Outlet standard deviation (mm)","Standardabweichung der Auslassposition (mm)"),np.std(run.exit_x)*1e3,np.sqrt(ref["variance_x"])*1e3],
            [tr("Mean transit time (s)","Mittlere Durchlaufzeit (s)"),np.mean(run.arrival-run.release),ref["mean_transit"]],
            [tr("Mean arrival time (s)","Mittlere Ankunftszeit (s)"),np.mean(run.arrival),ref["mean_arrival"]],
            [tr("Arrival-time standard deviation (s)","Standardabweichung der Ankunftszeit (s)"),np.std(run.arrival),np.sqrt(ref["variance_arrival"])],
        ]
        st.dataframe(pd.DataFrame(values,columns=[tr("Quantity","Größe"),tr("Particle sample","Teilchenstichprobe"),tr("Exact model reference","Exakte Modellreferenz")]),hide_index=True,width="stretch")
        if run.network:
            net=run.network
            st.caption(tr(f"Inlet flow: {net.inlet_flow*1e9:.4g} µL/s · relative node residual: {net.residual:.2e} · inlet/outlet imbalance: {net.imbalance:.2e} · maximum throat Re: {net.max_reynolds:.3g}.",
                          f"Zufluss: {net.inlet_flow*1e9:.4g} µL/s · relativer Knotenrest: {net.residual:.2e} · Zu-/Abflussabweichung: {net.imbalance:.2e} · maximale Poren-Re: {net.max_reynolds:.3g}."))
            if net.max_reynolds>=1:
                st.info(tr("Some throat Reynolds numbers reach or exceed 1. Creeping-flow conditions are not assured throughout this teaching network.",
                           "Einige Poren-Reynolds-Zahlen erreichen oder überschreiten 1. Schleichende Strömung ist in diesem Lehrnetz nicht überall gewährleistet."))
        left,right=st.columns(2)
        left.download_button(tr("Particle results · CSV","Teilchenergebnisse · CSV"),particle_csv(run),"dispersion_particles.csv","text/csv",key=f"disp_{page}_csv",width="stretch")
        metadata=summary(run)
        metadata["display"]={"highlighted":state["run_highlighted"],"background_each":state["applied_background"],"page":page}
        right.download_button(tr("Parameters and statistics · JSON","Parameter und Statistik · JSON"),json.dumps(metadata,indent=2),"dispersion_run.json","application/json",key=f"disp_{page}_json",width="stretch")


# 5. Page entry points --------------------------------------------------------
def render_page():
    """Backward-compatible integration entry point for the configurable page."""
    st.title(tr("Grain network · explore and modify","Kornnetzwerk · erkunden und verändern"))
    st.subheader(tr("From individual pathways to a spreading solute pulse","Von einzelnen Fließwegen zur Ausbreitung eines Stoffimpulses"),divider="blue")
    with section("instructions",tr("How to use this experiment","So nutzen Sie dieses Experiment"),expanded=True,tone="teal"):
        st.markdown(content("explore_01",st.session_state.get("language","en")))
    experiment()
    with section("grain_motion",tr("Why can particles move upward or slowly?","Warum können sich Teilchen aufwärts oder langsam bewegen?")):
        from .pages import markdown
        markdown("grain_motion")
    with section("activities",tr("Explore, predict, and explain","Erkunden, vorhersagen und erklären")):
        st.markdown(content("activities",st.session_state.get("language","en")))


def render_pinboard():
    """Intermediate experiment: cohort size, regular/variable times, geometry."""
    st.title(tr("Pinboard · from particles to a plume","Galtonbrett · vom Teilchen zur Stoffwolke"))
    st.subheader(tr("Increase the sample, then change one condition","Stichprobe vergrößern, dann eine Bedingung ändern"),divider="green")
    with section("instructions",tr("How to use this experiment","So nutzen Sie dieses Experiment"),expanded=True,tone="teal"):
        st.markdown(content("pinboard_01",st.session_state.get("language","en")))
    experiment("pinboard")
    with section("arrival_theory",tr("Why do arrival times spread?","Warum streuen die Ankunftszeiten?")):
        from .pages import markdown, illustration
        markdown("theory_03")
        illustration("arrival",tr("Fixed and variable travel times; pulse and finite-duration injection.","Feste und variable Laufzeiten; Impuls und endliche Zugabedauer."))
