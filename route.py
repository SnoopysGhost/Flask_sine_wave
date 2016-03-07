# -*- coding: utf-8 -*-
"""
Created on Sun Mar 06 19:05:28 2016

@author: Ruan
"""

import numpy as np

from flask import Flask, render_template

from bokeh.plotting import figure, show, gridplot, output_file
from bokeh.models import ColumnDataSource, HBox, VBoxForm, CustomJS
from bokeh.models.widgets import Slider
from bokeh.embed import components

#Static Amplitude 
amp = 5

#Set up data
N = 200
x = np.linspace(0,4*np.pi,N)
y = amp*np.sin(x)

source = ColumnDataSource(data=dict(x=x,y=y))

#Interaction tools
TOOLS = 'box_select, crosshair, help, reset, resize'

# Figure plotting function
def make_figure():
    #set up plot
    plot = figure(plot_height=400, plot_width=400, title="Sine Wave",
                  tools=TOOLS, x_range=[0,4*np.pi], y_range=[-5,5])
                  
    plot.line('x','y', source=source, line_width=3)
    plot.scatter('x','y', source=source,size=5)
    
    #call back CustomJS
    callback = CustomJS(args=dict(source=source), code="""
                var data = source.get('data')
                var f = cb_obj.get('value')
                x = data['x']
                y = data['y']
                for (i = 0; i < x.length; i++) {
                    y[i] = f*Math.sin(x[i])            
                    }
                    source.trigger('change');
                    """)

    #add slider
    amplitude = Slider(title="Amplitude",value=amp, start=0, end=5, callback=callback)

    #plot
    layout = VBoxForm(amplitude,plot)
    show(layout)
    return plot #need to return the layout
        
# Calling plotting Function
p = make_figure()
      
# Extracting HTML elements
script, div = components(p)

#Set up Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')
    
@app.route('/plot')
def plot():
   return render_template('plot.html', script=script, div=div)
    
if __name__ == '__main__':
    app.run(debug=True)