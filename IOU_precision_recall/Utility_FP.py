#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import cv2
from sklearn.neighbors import NearestNeighbors

class Utility_FP(object):
    
    @staticmethod
    def compute_bnd_red_cv(img, low_th, high_th, connectivity):
        ret, thresh = cv2.threshold(img,low_th,high_th,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
        reduction = cv2.connectedComponents(thresh, connectivity, cv2.CV_32S)
        return contours, hierarchy, reduction
    
    @staticmethod
    def cvt_geometry2list(g):
        '''
        Convert outputs from extract_geometry_fromGDB to x1 y1 x2 y2 list.
        This function only works when fields2read is: ['Random', 'START_X', 'START_Y', 'END_X', 'END_Y', 'Random', ...]
        @g: input geometry, output from extract_geometry_fromGDB
        '''
        lyr_num = len(g)
        x1 = [[0.0]] * lyr_num
        y1 = [[0.0]] * lyr_num
        x2 = [[0.0]] * lyr_num
        y2 = [[0.0]] * lyr_num
        for lyr in range(lyr_num):
            x1_ = [0.0] * len(g[lyr])
            y1_ = [0.0] * len(g[lyr])
            x2_ = [0.0] * len(g[lyr])
            y2_ = [0.0] * len(g[lyr])
            for i in range(len(g[lyr])):
                x1_[i] = g[lyr][i][1]
                y1_[i] = g[lyr][i][2]
                x2_[i] = g[lyr][i][3]
                y2_[i] = g[lyr][i][4]
            x1[lyr] = x1_
            y1[lyr] = y1_
            x2[lyr] = x2_
            y2[lyr] = y2_
        return x1, y1, x2, y2
    
    @staticmethod
    def extract_patch(x, y, patch_size, img):
        '''
        Extract patch from image.
        @x: x coordinate of the center pixel
        @y: y coordinate of the center pixel
        @patch_size: size of the extracted patch, has to be odd number
        @img: input image
        '''
        assert(patch_size % 2 == 1)
        [h, w] = img.shape
        radius = int(np.floor(patch_size / 2))
        l = max(0, x - radius)
        r = min(w - 1, x + radius)
        t = max(0, y - radius)
        b = min(h - 1, y + radius)
        return img[t:b+1, l:r+1]
    
    @staticmethod
    def extract_patch_topleft(x, y, patch_size, img):
        '''
        Extract patch from image.
        @x: x coordinate of the top left pixel
        @y: y coordinate of the top left pixel
        @patch_size: size of the extracted patch, has to be odd number
        @img: input image
        '''
        assert(patch_size % 2 == 1)
        [h, w] = img.shape
        r = min(w - 1, x + patch_size-1)
        b = min(h - 1, y + patch_size-1)
        ph = b - y + 1
        pw = r - x + 1
        if ph <= 1 or pw <= 1:
            return None
        else:
            return img[y:b+1, x:r+1]
        
    @staticmethod    
    def pairwise_distance(x1, y1, x2, y2, radius):
        num1 = len(x1)
        num2 = len(x2)
        set1 = [None] * num1
        set2 = [None] * num2
        for i in range(num1):
            set1[i] = [x1[i], y1[i]]
        for i in range(num2):
            set2[i] = [x2[i], y2[i]]
        set1 = np.array(set1)
        set2 = np.array(set2)

        cost_matrix = np.ones((num1, num2), dtype=np.float32) * sys.float_info.max
        nbrs = NearestNeighbors(radius=radius).fit(set2)
        rng = nbrs.radius_neighbors(set1)
        for i in range(num1):
            cost_matrix[i, rng[1][i]] = rng[0][i]
        return cost_matrix

