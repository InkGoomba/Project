import matplotlib.pyplot as plt
import  numpy as np
from scipy.spatial import Delaunay

points = np.array([[0.0, 0.0], [2.0, 0.0], [1.0, 2.0]])

def centroid(points : np.array):
    total_center_x = 0
    total_center_y = 0
    center_y = 0
    center_x = 0

    for point in points:
        total_center_x += point[0]
        total_center_y += point[1]

    center_x = total_center_x/len(points)
    center_y = total_center_y/len(points)
    print(center_x)
    print(center_y)

    