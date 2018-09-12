#!/usr/bin/env python3
"""
    Simple shapes in cartesian coordinates
"""

from PIL import Image
import numpy as np

def black2white_plus(size):
    length = size
    width = size
    # white background
    xy = np.ones((width, length, 3)) * 255

    for x in range(length):
        for y in range(width):
            xy[x,y,:] = (x*y)*255/(length*width)
    Image.fromarray(np.uint8(xy)).show()

def black2white_multi(size):
    length = size
    width = size
    # white background
    xy = np.ones((width, length, 3)) * 255

    for x in range(length):
        for y in range(width):
            xy[x,y,:] = (x*y)*255/(length*width)
    Image.fromarray(np.uint8(xy)).show()

def circle(size):
    length = size
    width = size
    # white background
    xy = np.ones((width, length, 3)) * 255

    # x axis (blue)
    xy[width//2,:,:] = [0,0,255]
    # y axis (blue)
    xy[:,length//2,:] = [0,0,255]

    for x in range(width):
        for y in range(length):
            axis_x = float(x-length/2)/(length/2)
            axis_y = float(y-width/2)/(width/2)
            r = 1
            if abs((axis_x**2 + axis_y**2) - r) < 1/(float(size)/2):
                xy[x,y,:] = [0,0,255]

    Image.fromarray(np.uint8(xy)).show()

def ellipse(size):
    length = size
    width = size
    # white background
    xy = np.ones((width, length, 3)) * 255

    # x axis (blue)
    xy[width//2,:,:] = [0,0,255]
    # y axis (blue)
    xy[:,length//2,:] = [0,0,255]

    for x in range(length):
        for y in range(width):
            axis_x = float(x-length/2)/(length/2)
            axis_y = float(y-width/2)/(width/2)
            a = 0.5
            b = 1
            if abs((axis_x**2/a**2 + axis_y**2/b**2) - 1) < 2/(float(size)/2):
                xy[x,y,:] = [0,0,255]

    Image.fromarray(np.uint8(xy)).show()

def circle_estimate(x, y, u):
    r = 1
    if abs((x**2 + y**2) - r) < 1/(u/2):
        return True
    else:
        return False

def ellipse_estimate(x, y, u):
    a = 0.5
    b = 1
    if abs((x**2/a**2 + y**2/b**2) - 1) < 2/(u/2):
        return True
    else:
        return False

def hyperbola_estimate(x, y, u):
    a = 0.5
    b = 0.5
#    if abs((x**2/a**2 - y**2/b**2) - 1) < 2/(u/2):
    if abs((x**2/a**2 - y**2/b**2) + 1) < 2/(u/2):
        return True
    else:
        return False

def general_shapes(width=600,length=800,background=[255,255,255],frontground=[0,0,255],func=circle_estimate):

    xy=np.ones((width, length, 3))
    xy[:,:,:]=background

    #x axis
    xy[width//2,:,:]=frontground
    #y axis
    xy[:,length//2,:]=frontground

    axis_unit=float(min(width, length))
    for x in range(width):
        for y in range(length):
            axis_x=float(x-width/2)/(axis_unit/2)
            axis_y=float(y-length/2)/(axis_unit/2)
#            r = 1
#            if abs((axis_x**2 + axis_y**2) - r) < 1/(float(axis_unit)/2):
            if func(axis_x, axis_y, axis_unit):
                xy[x,y,:]=frontground

    Image.fromarray(np.uint8(xy)).show()


if __name__ == '__main__':
    imagesize = 75*9
#    black2white_multi(imagesize)
#    black2white_plus(imagesize)
#    circle(imagesize)
#    ellipse(imagesize)
#    general_shapes(79*9,79*16,[204,232,207],[0,0,255],circle_estimate)
#    general_shapes(79*9,79*16,[204,232,207],[0,0,255],ellipse_estimate)
    general_shapes(79*9,79*16,[204,232,207],[0,0,255],hyperbola_estimate)
