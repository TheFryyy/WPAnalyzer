import cv2
import numpy as np


def find_homography(pts_src, pts_dist):
    h = cv2.findHomography(pts_src, pts_dist, cv2.RANSAC)
    return h


def real_point(right_side):
    if right_side:
        return np.float32([[0, 0], [2, 0], [0, 9], [2, 9]])
    else:
        return np.float32([[25, 0], [23, 0], [25, 9], [23, 9]])


def src_point(points):
    pts_src = []
    for point in points:
        pts_src.append(point.to_array())
    return np.float32(pts_src)


def warp(point, mat):
    return cv2.perspectiveTransform(point, mat)


def transform_points(points):
    new_points = []
    for point in points:
        new_points.append(point)
    return np.float32([new_points])


