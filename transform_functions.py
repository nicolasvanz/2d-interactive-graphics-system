import math
import numpy as np


def generic_transform(coord_obj, matrix):
    new_coords = []
    for coord in coord_obj:
        coord_multi = np.dot(np.array([coord[0], coord[1], 1]), matrix)
        new_coords.append((coord_multi[0], coord_multi[1]))
    return new_coords


def rotation(matrix, angle, ref_point):
    cos = math.cos(math.radians(angle))
    sin = math.sin(math.radians(angle))
    rotation_array = np.array([[cos, sin, 0], [-sin, cos, 0], [0, 0, 1]])
    if ref_point == (0, 0):
        result = np.dot(np.array(matrix), rotation_array)
        return result.tolist()
    else:
        neg_ref_point = (-ref_point[0], -ref_point[1])
        mat_after_trans = translation(matrix, neg_ref_point)
        inter_result = np.dot(np.array(mat_after_trans), rotation_array)
        result = translation(inter_result.tolist(), ref_point)
        return result


def translation(matrix, ref_point):
    dx = ref_point[0]
    dy = ref_point[1]
    translation_array = np.array([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])
    result = np.dot(np.array(matrix), translation_array)
    return result.tolist()


def scale(matrix, scale_coef, center_point):
    sx = scale_coef[0]
    sy = scale_coef[1]
    scale_array = np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])
    neg_cent_point = (-center_point[0], -center_point[1])
    mat_after_trans = translation(matrix, neg_cent_point)
    inter_result = np.dot(np.array(mat_after_trans), scale_array)
    result = translation(inter_result.tolist(), center_point)
    return result

'''
list_array = np.array([2, 3, 4])
matrix_array = np.array([[1, 2, 3], [2, 2, 2], [3, 3, 3]])

coord = [(6, 1)]

identity = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
trans = translation(identity, (50,40))
#print(rot)
print(generic_transform(coord, trans))
'''