#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().run_line_magic('run', 'Topo_FP.ipynb')
get_ipython().run_line_magic('run', 'FileIO_FP.ipynb')
get_ipython().run_line_magic('run', 'Viewer_FP.ipynb')
get_ipython().run_line_magic('run', 'Utility_FP.ipynb')
get_ipython().run_line_magic('run', 'Conversion_DWG_FP.ipynb')
import numpy as np
from scipy.optimize import linear_sum_assignment

def compute_precision_recall_helper(path1, path2, units, threshold):
    '''
    @path1: path to ground truth jason file
    @path2: path to generated jason file
    @units: length of each pixel, has to be "1cm"
    @threshold: threshold to match the points, in cm, 
     pass in 2, 5, 10 as thresholds corresponding to 2, 5, 10 cm
    '''
    geo1 = FileIO_FP.read_geometry_JSON(path1, "1cm")
    geo2 = FileIO_FP.read_geometry_JSON(path2, "1cm")
    x1, y1 = Conversion_DWG_FP.extract_all_points(geo1)
    x2, y2 = Conversion_DWG_FP.extract_all_points(geo2)

    cost_matrix = Utility_FP.pairwise_distance(x1, y1, x2, y2, threshold)
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    matched_pts = 0
    for i in range(len(row_ind)):
        if cost_matrix[row_ind[i]][col_ind[i]] <= threshold:
            matched_pts = matched_pts + 1
    precision = matched_pts / cost_matrix.shape[1] if cost_matrix.shape[1] else 0
    recall = matched_pts / cost_matrix.shape[0] if cost_matrix.shape[0] else 0
    return precision, recall

def compute_precision_recall(path1, path2, units):
    '''
    @path1: path to ground truth jason file
    @path2: path to generated jason file
    @units: length of each pixel, has to be "1cm"
    '''
    if units != "1cm":
        print("Invalid pixel length, has to be 1cm")
        sys.exit()
    p1, r1 = compute_precision_recall_helper(path1, path2, units, 2)
    p2, r2 = compute_precision_recall_helper(path1, path2, units, 5)
    p3, r3 = compute_precision_recall_helper(path1, path2, units, 10)
    return [p1, p2, p3], [r1, r2, r3]

def compute_room_IOU(path1, path2, units, area_threshold):
    '''
    @path1: path to ground truth jason file
    @path2: path to generated jason file
    @units: length of each pixel
    @area_threshold: the threshold to determine a room
    '''
    geo1 = FileIO_FP.read_geometry_JSON(path1, units)
    geo2 = FileIO_FP.read_geometry_JSON(path2, units)
    geo1 = Conversion_DWG_FP.cvt_geometry_format_obj2drw(geo1)
    geo2 = Conversion_DWG_FP.cvt_geometry_format_obj2drw(geo2)
    x1_1, y1_1, x2_1, y2_1 = Utility_FP.cvt_geometry2list(geo1)
    x1_2, y1_2, x2_2, y2_2 = Utility_FP.cvt_geometry2list(geo2)
    shape = Viewer_FP.determine_curtain_size_sync(x1_1, y1_1, x2_1, y2_1, x1_2, y1_2, x2_2, y2_2)
    img1  = Viewer_FP.plot_layers(x1_1, y1_1, x2_1, y2_1, [-1], shape, 1)
    img2  = Viewer_FP.plot_layers(x1_2, y1_2, x2_2, y2_2, [-1], shape, 1)
    iou = Topo_FP.compute_room_matching(img1, img2, units, area_threshold)
    return iou

def compute_Betti_error(path1, path2, patch_size, N):
    '''
    @path1: path to ground truth jason file
    @path2: path to generated jason file
    @patch_size: integer, size of the sample patch
    @N: integer, number of samples
    '''
    geo1 = FileIO_FP.read_geometry_JSON(path1, "20cm")
    geo2 = FileIO_FP.read_geometry_JSON(path2, "20cm")
    geo1 = Conversion_DWG_FP.cvt_geometry_format_obj2drw(geo1)
    geo2 = Conversion_DWG_FP.cvt_geometry_format_obj2drw(geo2)
    x1_1, y1_1, x2_1, y2_1 = Utility_FP.cvt_geometry2list(geo1)
    x1_2, y1_2, x2_2, y2_2 = Utility_FP.cvt_geometry2list(geo2)
    shape = Viewer_FP.determine_curtain_size_sync(x1_1, y1_1, x2_1, y2_1, x1_2, y1_2, x2_2, y2_2)
    img1 = Viewer_FP.plot_layers(x1_1, y1_1, x2_1, y2_1, [-1], shape, 1)
    img2 = Viewer_FP.plot_layers(x1_2, y1_2, x2_2, y2_2, [-1], shape, 1)
    betti_error = Topo_FP.compute_betti_error_patch(img1, img2, 8, patch_size, N)
    return betti_error

json_path1 = "E:/Data2/ArcGIS/Floor_CAD/Wenxuan/gt_json/01_OfficeLab_01_F1_floorplan.txt"
json_path2 = "E:/Data2/ArcGIS/Floor_CAD/Wenxuan/user_json/01_OfficeLab_01_F1_floorplan.txt"
precision, recall = compute_precision_recall(json_path1, json_path2, "1cm")
iou = compute_room_IOU(json_path1, json_path2, "20cm", 100)
betti_error = compute_Betti_error(json_path1, json_path2, 25, 500)
print(precision, recall)
print(iou)
print(betti_error)

