# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 10:12:43 2016

@author: ami
"""

import numpy as np

from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

# prepare sample data from txt file
raw_data = []
with open("denoised_func.txt") as f:
    for line in f.readlines():
        data = line.strip("\n").split(" ")
        data = [float(i) for i in data]
        raw_data.append(data) 
        
fc = np.asarray(raw_data).reshape((179,179))

names = ["roi%s" % (i+1) for i in range(len(fc))]

def interactive_fc(nodes, fc_arr):
    """ 
    function to display interactive correlation matrix
    nodes: a list of lendth N specifying node names
    fc_arr: a numpy array of NxN 
    """
    
    xname = []
    yname = []
    color = []
    alpha = []
    for i, node1 in enumerate(names):
        for j, node2 in enumerate(names):
            xname.append(node1)
            yname.append(node2)
            alpha.append(min(abs(fc[i,j]), 0.9) + 0.1)

            if fc[i,j] < -0.2:
                color.append("#e31a1c")
            elif fc[i,j] > 0.2:
                color.append("#1f78b4")
            else:
                color.append('lightgrey')

    source = ColumnDataSource(data=dict(
        xname=xname,
        yname=yname,
        colors=color,
        alphas=alpha,
        count=fc.flatten(),
    ))
    
    p = figure(title="Functional Connectivity Matrix",
           x_axis_location="above", tools="resize,box_zoom,hover,save,reset",
           x_range=list(reversed(names)), y_range=names)

    p.plot_width = 800
    p.plot_height = 800
    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_text_font_size = "5pt"
    p.axis.major_label_standoff = 0
    p.xaxis.major_label_orientation = np.pi/3

    p.rect('xname', 'yname', 0.9, 0.9, source=source,
           color='colors', alpha='alphas', line_color=None, 
           hover_line_color="black", hover_color='colors', hover_alpha=1.0)

    p.select_one(HoverTool).tooltips = [
        ('names', '@yname, @xname'),
        ('FC strength', '@count'),
    ]

    output_file("fc_test.html", title="FC Matrix example")

    show(p) # show the plot