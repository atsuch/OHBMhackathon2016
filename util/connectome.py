# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 12:35:34 2016

@author: taken from https://www.continuum.io/blog/developer-blog/drawing-brain-bokeh
modified by Ami
"""

from math import pi, cos, sin
 
def draw_circle_points(points, radius=1, centerX=0, centerY=0):
    part = 2 * pi / points
    final_points = []
 
    for point in range(points):
        angle = part * point;
        newX = centerX + radius * cos(angle)
        newY = centerY + radius * sin(angle)
        final_points.append((newX, newY))
 
    return final_points
    

def connectomme_lines(connectome, hardness=0.3):
    number_of_areas = connectome.shape[0]
    positions = draw_circle_points(number_of_areas)
 
    final_positions = []
    area_name = []
 
    for index, area1 in enumerate(connectome):
        commonXY = positions[index]
        for index2, area2 in enumerate(area1):
            newXY = positions[index2]
            if abs(area2) > hardness:
                final_positions.append([[commonXY[0], newXY[0]], [commonXY[1], newXY[1]]])
 
    return final_positions


def width_of_lines(c, hardness=0.3):
    f = c.flatten()
    flat = f[(abs(f) > hardness)]
    
    return flat/flat.sum()