# -*- coding: utf-8 -*-
"""
Created on Sun Mar 06 19:05:28 2016

@author: Ruan
"""

import numpy as np

from flask import Flask, render_template

from bokeh.plotting import Figure
from bokeh.models import ColumDataSource, HBox, VBoxFrom
from bokeh.models.widget import Slider, TextInput
from bokeh.io import curdoc


#Set up data
N = 200
x = np.linspace(0,4*np.pi,N)
y = np.sin(x)
source = ColumDataSource(data = dict(x=x,y=y))

#set up plot
plot = Figure(plot_height=400, plot_width=400, title="Sine Wave",
              tools="crosshair,reset,pan", x_rane=[0,4*np.pi], y_range=[-5,-5])
              
plot.line('x','y', source=source, line_width=3, line_alpha=0.6)

#set up widgets

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')
    
@app.route('/plot')
def plot():
    return render_template('plot.html')
    
if __name__ == '__main__':
    app.run(debug=True)