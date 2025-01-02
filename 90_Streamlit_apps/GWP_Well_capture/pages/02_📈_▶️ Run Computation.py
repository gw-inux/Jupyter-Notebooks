# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 11:23:09 2024

@author: Gaelen
"""
import os
import sys

import numpy as np
from bokeh.plotting import figure, save, curdoc
from bokeh.models import CustomJS, HoverTool, ColumnDataSource, Slider, CustomJSTickFormatter, InlineStyleSheet, Div, Range1d
from bokeh.models import VeeHead, Arrow, Label, ColorBar, RadioButtonGroup, PointDrawTool
from bokeh.themes import Theme
from bokeh.layouts import column, row
from bokeh.embed import file_html
from bokeh.models import NumericInput
import pandas as pd
# sys.path.append(r'C:\Repo\GWProject_Bokeh')
# import Bokeh_Util as Bokeh_Util

import httpimport
url = r"https://raw.githubusercontent.com/gmerritt123/GWProject_Bokeh/refs/heads/main/Bokeh_Util.py"
with httpimport.github_repo('gmerritt123', 'GWProject_Bokeh', ref='main'):
  import Bokeh_Util as Bokeh_Util


import streamlit as st
st.title('Well capture zone for a confined aquifer')
import streamlit.components.v1 as components

# wdir = r'C:\Repo\Jupyter-Notebooks\90_Streamlit_apps\GWP_Well_capture\pages' #when using in IDE locally
wdir = os.path.dirname(os.path.realpath(__file__)) #when deploying
# wdir = os.getcwd()+r'\\90_Streamlit_apps/GWP_Well_capture/pages'
#style/theming loading
thm = Theme(filename=wdir+r'/Bokeh_Styles.yaml') #read yaml file for some styling already hooked up
with open(wdir+r'/Bokeh_Styles.css','r') as f:
    css = f.read()
sl_style = InlineStyleSheet(css=css)

#slider layout
slider_dict = {
    'Pumping': Slider(title='Pumping rate (m³/s)', value=0, start=0, end=0.2, step = 0.001
                        ,format='0.000'                        
                        )
    ,'Thickness': Slider(title='Aquifer thickness (m)',value=20 ,start=1, end=100, step = 0.01
                        ,format='0.00')
    ,'Gradient': Slider(title='Gradient of regional flow (dimensionless)',value = -5, start = -5, end = 0, step = 0.1
                        ,format=CustomJSTickFormatter(code="return (10**tick).toExponential(2).toString()") #handling log scale slider)
                        )

    ,'Conductivity':Slider(title='Hydraulic Conductivity (m/s)',value = -3, start = -7, end = 0, step = 0.01
                        ,format=CustomJSTickFormatter(code="return (10**tick).toExponential(2).toString()") #handling log scale slider)
                        )
    ,'Porosity':Slider(title='Porosity', value=0.3,start=0.01,end=0.5,step=0.01)
    }

#create figure
f = figure(height=800,width=1200
            # ,title='Well capture zone of a pumping well'
            # ,sizing_mode='scale_both'
            ,match_aspect=True
            ,x_range = [-10,1]
            ,y_range= [-5,5]
            )

f.xaxis[0].axis_label = 'Kilometers'
f.yaxis[0].axis_label = 'Kilometers'

vh = VeeHead(size=15, fill_color='black')
arrw = Arrow(end=vh
              , x_start=100, y_start=600, x_end=200
              , y_end=600,
              end_units='screen',start_units='screen'
              )
f.add_layout(arrw,'center')
lbl = Label(x=100,y=600,y_offset=-50,text='Regional Gradient\nDirection',x_units='screen',y_units='screen'
            # ,render_mode='css'
            )
f.add_layout(lbl)

#well glyph, using highest level API because it's static (no need to access/manipulate for now)
pw = f.scatter(x=[0],y=[0],marker='circle_x',size=12,legend_label='Pumping well',fill_color='red')

#capture zone datasource
src = ColumnDataSource(data={'y': []
                              ,'x': []
                              }) #initialize completely empty, to be filled on first user action

#patch renderer for capture zone
cz_pr = f.patch(x='x',y='y',source=src, fill_alpha=0.1,legend_label='Well capture zone')


#arrow showing width
w_src = ColumnDataSource(data={'x0':[],'y0':[],'x1':[],'y1':[]})
w_arrw = Arrow(start=vh,end=vh,x_start='x0',y_start='y0',x_end='x1',y_end='y1'
                ,source=w_src)
f.add_layout(w_arrw)
w_lbl = Label(x=0,y=0,text='Max Width = '
                ,visible=False
              )
f.add_layout(w_lbl)
#arrow showing culmination
cvh = VeeHead(size=5, fill_color='black')
c_src = ColumnDataSource(data={'x0':[],'y0':[],'x1':[],'y1':[]})
c_arrw = Arrow(start=cvh,end=cvh,x_start='x0',y_start='y0',x_end='x1',y_end='y1'
                ,source=c_src)
f.add_layout(c_arrw)
c_lbl = Label(x=0,y=0,text='Culm. Pt. = '
                ,visible=False
              )
f.add_layout(c_lbl)

#head/drawdown contours

rb = RadioButtonGroup(labels=['Well Drawdown','Hydraulic Head'],active=0)

hr_src = ColumnDataSource(data={'xs':[],'ys':[],'z':[]})
from bokeh.palettes import Turbo256, Inferno
from bokeh.transform import linear_cmap, log_cmap
hr = f.multi_line(xs='xs',ys='ys'
               ,line_color=linear_cmap(field_name='z',palette=Turbo256,low=None,high=None)
               ,line_alpha=1.0
               ,source=hr_src
                )
color_bar = ColorBar(color_mapper=hr.glyph.line_color.transform
                     ,title='Drawdown (m)')

f.add_layout(color_bar, 'right')



pt_rel = f.scatter(x=[],y=[],size=5)
pt_d = PointDrawTool(renderers=[pt_rel], num_objects=1)
f.add_tools(pt_d)

ptl_src = ColumnDataSource(data={'x':[],'y':[]})
# pt_l = f.line(x='x',y='y',source=ptl_src)
pt_sc = f.scatter(x='x',y='y',source=ptl_src,line_alpha=0
                  ,fill_alpha=0.5
                  ,fill_color=linear_cmap(field_name='t',palette=Inferno[11],low=0,high=None)
                  )

tt_bar = ColorBar(color_mapper=pt_sc.glyph.fill_color.transform
                     ,title='Particle Travel Time (years)'
                     ,orientation='horizontal')

f.add_layout(tt_bar, 'below')

pt_cb = CustomJS.from_file(path=wdir+r'/pt_cb.mjs'
                           ,sl_dict=slider_dict,pt_src=pt_rel.data_source, f = f
                           , pt_d = pt_d, ptl_src = ptl_src)

f.js_on_event('tap',pt_cb)
f.toolbar.active_tap = pt_d


cb = CustomJS.from_file(path=wdir+r'/cb.mjs'
                        , src=src,sl_dict=slider_dict, f= f
                        ,w_src=w_src, w_lbl=w_lbl
                        ,c_src=c_src,c_lbl=c_lbl
                        ,hr_src=hr_src, color_bar=color_bar, rb = rb
                        ,pt_cb = pt_cb
                        )

#execute this callback when slider value changes
#link the numeric inputs too
ni_dict = {}
for k,sl in slider_dict.items():
    sl.js_on_change('value',cb)
    sl.stylesheets = [sl_style]
    sl.width=f.width
    sl.sizing_mode='stretch_width'
    if k in ['Gradient','Conductivity']:
        ni_dict[k] = Bokeh_Util.linkNumericInputToSlider(slider=sl,log=True)
    else:
        ni_dict[k] = Bokeh_Util.linkNumericInputToSlider(slider=sl,log=False)
    ni_dict[k].width=100



rb.js_on_change('active',cb)
rb.stylesheets = [sl_style]


slider_layout = [row(list(x),sizing_mode='scale_width') for x in zip(slider_dict.values(),ni_dict.values())]


#layout
lo = column(
    # [sl for sl in slider_dict.values()]
            slider_layout
            +[rb,f]
            ,sizing_mode = 'scale_width'
            )

pv_ins_df = pd.DataFrame(data={'minRange':[0,3],'unitName':['Meters','Kilometers'],'scaleFactor':[.001,1]})
Bokeh_Util.setDynamicUnitScale(fig=f,ins_df=pv_ins_df,ranges='both')

           

# curdoc().theme = thm #assigns theme
# save(lo,wdir+r'/BokehApp.html',title='Well Capture')
Bokeh_Util.save_html_wJSResources(bk_obj=lo
                                  ,fname=wdir+r'/BokehApp.html'
                                  ,resources_list_dict={'sources':['http://d3js.org/d3.v6.js'],'scripts':[]}
                                  ,html_title='Well Capture',theme=thm
    ,icon_url='https://aquainsight.sharepoint.com/sites/AquaInsight/_api/siteiconmanager/getsitelogo?type=%271%27&hash=637675014792340093')

# bk_html = file_html(models=lo,resources='cdn')

with open(wdir+'/BokehApp.html') as f:
    bk_html = f.read()
components.html(bk_html,height=800)



