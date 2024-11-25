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
from bokeh.models import VeeHead, Arrow, Label
from bokeh.themes import Theme
from bokeh.layouts import column

wdir = r'C:\Repo\Jupyter-Notebooks\90_Streamlit_apps\GWP_Well_capture\pages' #when using in IDE locally
# wdir = os.path.dirname(os.path.realpath(__file__)) #when deploying

#style/theming loading
thm = Theme(filename=wdir+r'\\Bokeh_Styles.yaml') #read yaml file for some styling already hooked up
with open(wdir+'\\Bokeh_Styles.css','r') as f:
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

    ,'Conductivity':Slider(title='Hydraulic Conductivity (m/s)',value = -3, start = -3, end = 0, step = 0.01
                        ,format=CustomJSTickFormatter(code="return (10**tick).toExponential(2).toString()") #handling log scale slider)
                        )
    }

#create figure
f = figure(height=800,width=800
           ,title='Well capture zone of a pumping well'
           # ,sizing_mode='stretch_both'
           ,match_aspect=True
           ,x_range = [-10,1]
           ,y_range= [-5,5]
           )

f.xaxis[0].axis_label = 'y (m)'
f.yaxis[0].axis_label = 'x (m)'

vh = VeeHead(size=15, fill_color='black')
arrw = Arrow(end=vh
              , x_start=100, y_start=400, x_end=200
              , y_end=400,
              end_units='screen',start_units='screen'
             )
f.add_layout(arrw,'center')
lbl = Label(x=100,y=400,y_offset=-50,text='Regional Gradient\nDirection',x_units='screen',y_units='screen')
f.add_layout(lbl)

#well glyph, using highest level API because it's static (no need to access/manipulate for now)
pw = f.scatter(x=[0],y=[0],marker='circle_x',size=12,legend_label='Pumping well',fill_color='red')

#capture zone datasource
src = ColumnDataSource(data={'y': []
                             ,'x': []
                             }) #initialize completely empty, to be filled on first user action


#patch renderer for capture zone
cz_pr = f.patch(x='x',y='y',source=src, fill_alpha=0.1,legend_label='Well capture zone')

cb = CustomJS.from_file(path=wdir+r'\\cb.mjs', src=src,sl_dict=slider_dict, f= f)

#execute this callback when slider value changes
for sl in slider_dict.values():
    sl.js_on_change('value',cb)
    sl.stylesheets = [sl_style]
    sl.width=f.width
    
#layout
lo = column([sl for sl in slider_dict.values()]+[f]
            # ,sizing_mode = 'stretch_both'
            )


curdoc().theme = thm #assigns theme

save(lo,wdir+r'\\Testing.html',title='Well Capture')

