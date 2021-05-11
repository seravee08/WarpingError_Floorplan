import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from random import randrange

class Viewer_FP(object):
    
    @staticmethod
    def imshow_(img, cmap='gray', gray=True):
        plt.figure(figsize=(14,14))
        img = np.squeeze(img)
        if gray == True:
            imgplot = plt.imshow(img, cmap=cmap)
        else:
            imgplot = plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.show()
    
    @staticmethod
    def draw_red_on_single_dim_cv(red, cmap='jet', component_to_plot=-1):
        '''
        red: [0] is the number of labels (connected component), [1] is the matrix
        '''
        plt.figure(figsize=(12,12))
        assert(component_to_plot < red[0])
        if component_to_plot == -1:
            imgplot = plt.imshow(red[1], cmap=cmap)
        else:
            curtain = red[1]
            curtain[curtain!=component_to_plot] = red[0]
            imgplot = plt.imshow(curtain, cmap=cmap)
        return red[0]
    
    @staticmethod
    def draw_simple_points(img, simple_points):
        '''
        Draw computed simple points on the image plane for visualization.
        @img: input image, assuming in 3-channel RGB format
        @simple points: output from compute_simple_points
        '''
        assert(img.shape[2] == 3)
        for i in range(len(simple_points)):
            img = cv2.circle(img, (simple_points[i][1], simple_points[i][0]), 1, (0,0,255), 1)
        return img
    
    @staticmethod
    def plot_layers(x1, y1, x2, y2, index):
        '''
        @x1, y1, x2, y2: x y coordinates for two endpoints
        @index: list of integers indicating the layers to draw. If [-1] is given, draw all layers
        '''
        if len(index) == 1 and index[0] == -1:
            index = np.arange(len(x1))
        assert(len(x1) >= 1)
        assert(len(index) >= 1)
        assert(np.amax(index) < len(x1))
        colors = [None] * len(index)
        colors[0] = (0,0,0)
        for i in range(1, len(index)):
            colors[i] = (randrange(256), randrange(256), randrange(256))
        img = Viewer_FP.draw_coord(x1, y1, x2, y2, index[0], 5, colors[0])
        for i in range(1, len(index)):
            img = Viewer_FP.draw_coord(x1, y1, x2, y2, index[i], 5, colors[i], img)
        return img
    
    @staticmethod
    def draw_coord(x1, y1, x2, y2, index, thickness, color, img = None):
        '''
        Draw the coordinates output from cvt_geometry2list on an image
        @x1: x coordinate of the left endpoint
        @y1: y coordinate of the left endpoint
        @x2: x coordinate of the right endpoint
        @y2: y coordinate of the right endpoint
        @index: the layer to draw
        @thickness: line thickness
        @color: line color
        @img: if provided, the lines will be drawn on it. If not provided, it will be created
        '''
        if index >= len(x1):
            print("Requested index exceeds the size of the layers")
        if img is None:
            print("Determining the size of the image...")
            x_min = [0.0] * len(x1) * 2
            y_min = [0.0] * len(x1) * 2
            x_max = [0.0] * len(x1) * 2
            y_max = [0.0] * len(x1) * 2
            for i in range(len(x1)):
                x_min[i*2+0] = np.amin(x1[i])
                x_min[i*2+1] = np.amin(x2[i])
                y_min[i*2+0] = np.amin(y1[i])
                y_min[i*2+1] = np.amin(y2[i])
            x_shift = 100 - np.amin(x_min)
            y_shift = 100 - np.amin(y_min)
            for i in range(len(x1)):
                x1[i] = x1[i] + x_shift
                x2[i] = x2[i] + x_shift
                y1[i] = y1[i] + y_shift
                y2[i] = y2[i] + y_shift
            for i in range(len(x1)):
                x_max[i*2+0] = np.amax(x1[i])
                x_max[i*2+1] = np.amax(x2[i])
                y_max[i*2+0] = np.amax(y1[i])
                y_max[i*2+1] = np.amax(y2[i])
            x_bound = int(np.ceil(np.amax(x_max))) + 100
            y_bound = int(np.ceil(np.amax(y_max))) + 100
            img = np.ones((y_bound, x_bound), np.uint8) * 255
            img = cv2.merge((img, img, img))

        rows = img.shape[0]
        cols = img.shape[1]
        for i in range(len(x1[index])):
            x1_ = int(np.floor(x1[index][i]))
            y1_ = int(np.floor(y1[index][i]))
            x2_ = int(np.ceil(x2[index][i]))
            y2_ = int(np.ceil(y2[index][i]))
            if (x1_<0 or x1_>=cols or x2_<0 or x2_>=cols or y1_<0 or y1_>=rows or y2_<0 or y2_>=rows):
                print("Invalid coordinates")
            img = cv2.line(img, (x1_, y1_), (x2_, y2_), color, thickness)
        return img