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
    
if __name__ == '__main__':
    imagesize = 75*9
#    black2white_multi(imagesize)
#    black2white_plus(imagesize)
    circle(imagesize)
#    ellipse(imagesize)

