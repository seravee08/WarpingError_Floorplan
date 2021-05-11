import FileIO_FP
import Viewer_FP
import Utility_FP

import numpy as np
from scipy.optimize import linear_sum_assignment

def extract_all_points(geometry):
    '''
    This function extracts all points from geometry for hungarian matching
    @geometry: result from FileIO_FP.read_geometry_OBJ or from Conversion_DWG_FP.extract_geometry_fromGDB
        with flag obj_output set as True
    '''
    x_coord = []
    y_coord = []
    layer_num = len(geometry)
    for i in range(layer_num):
        struct_num = len(geometry[i])
        for j in range(struct_num):
            point_num = geometry[i][j][1]
            for k in range(1, point_num+1):
                x_coord.append(geometry[i][j][k*2])
                y_coord.append(geometry[i][j][k*2+1])
    return x_coord, y_coord


def pairwise_distance_v2(x1, y1, x2, y2):
    num1 = len(x1)
    num2 = len(x2)
    cost_matrix = np.ones((num1, num2), dtype=np.float32) * sys.float_info.max
    for i in range(num1):
        for j in range(num2):
            cost_matrix[i][j] = (x1[i]-x2[j])*(x1[i]-x2[j])+(y1[i]-y2[j])*(y1[i]-y2[j])
    return cost_matrix

def compute_precision_recall_v2(path1, path2, threshold):
    '''
    @path1: path to ground truth jason file
    @path2: path to generated jason file
    @patch_size: patch size to compute hungarian correspondence
    '''
    geo1 = FileIO_FP.read_geometry_JSON(path1, True)
    geo2 = FileIO_FP.read_geometry_JSON(path2, True)
    layer_num = len(geo1)
    assert(layer_num == len(geo2))
    x1, y1 = Conversion_DWG_FP.extract_all_points(geo1)
    x2, y2 = Conversion_DWG_FP.extract_all_points(geo2)
    cost_matrix = pairwise_distance_v2(x1, y1, x2, y2)
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    matched_pts = 0
    for i in range(len(row_ind)):
        if cost_matrix[row_ind[i]][col_ind[i]] < threshold:
            matched_pts = matched_pts + 1
    precision = matched_pts / cost_matrix.shape[1]
    recall = matched_pts / cost_matrix.shape[0]
    return precision, recall

def compute_IOU(path1, path2):
    '''
    @path1: path to ground truth jason file
    @path2: path to generated jason file
    '''
    geo1 = FileIO_FP.read_geometry_JSON(path1, True)
    geo2 = FileIO_FP.read_geometry_JSON(path2, True)
    geo1 = Conversion_DWG_FP.cvt_geometry_format_obj2drw(geo1)
    geo2 = Conversion_DWG_FP.cvt_geometry_format_obj2drw(geo2)
    x1_1, y1_1, x2_1, y2_1 = Utility_FP.cvt_geometry2list(geo1)
    x1_2, y1_2, x2_2, y2_2 = Utility_FP.cvt_geometry2list(geo2)
    img1 = Viewer_FP.plot_layers(x1_1, y1_1, x2_1, y2_1, [-1])
    img2 = Viewer_FP.plot_layers(x1_2, y1_2, x2_2, y2_2, [-1])
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    img1[img1 != 255] = 0
    img2[img2 != 255] = 0
    # Find intersection
    img1 = 255 - img1
    img2 = 255 - img2
    img1[img1 == 255] = 1
    img2[img2 == 255] = 1
    intersection = np.sum(np.multiply(img1, img2))
    union = img1 + img2
    union[union > 1] = 1
    union = np.sum(union)
    return intersection / union

# curtain = np.ones((300, 300), dtype=np.int32)
json_path1 = "E:/Data2/ArcGIS/Floor_CAD/Dataset/json/01_OfficeLab_01_F1_floorplan.txt"
json_path2 = "E:/Data2/ArcGIS/Floor_CAD/Dataset/json/01_OfficeLab_01_F1_floorplan.txt"
precision, recall = compute_precision_recall_v2(json_path1, json_path2, 13)
iou = compute_IOU(json_path1, json_path2)
print(precision, recall)
print(iou)