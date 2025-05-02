import matplotlib.pyplot as plt
import numpy as np
from plotsLib import plots
import random
import Project

class triangle():
    def __init__(self, p1, p2, p3):
        self.p1 = (p1[0], p1[1])
        self.p2 = (p2[0], p2[1])
        self.p3 = (p3[0], p3[1])

class polygon():
    def __init__(self):
        self.edges = set()

class edge():
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

def findDeterminant(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p3[0] - p1[0]) * (p2[1] - p1[1])

def circumcircle(p1, p2, p3, p4):
    if findDeterminant(p1, p2, p3) < 0:
        p2, p3 = p3, p2  # swap points to make counter-clockwise

    ax, ay = p1[0] - p4[0], p1[1] - p4[1]
    bx, by = p2[0] - p4[0], p2[1] - p4[1]
    cx, cy = p3[0] - p4[0], p3[1] - p4[1]

    det = np.linalg.det([
        [ax, ay, ax**2 + ay**2],
        [bx, by, bx**2 + by**2],
        [cx, cy, cx**2 + cy**2],
    ])
    return det >= 0

def plot_initial_and_delaunay(triangles, points):
    edges = []
    for triangle in triangles:
        edge1 = (triangle.p1, triangle.p2)
        edge2 = (triangle.p2, triangle.p3)
        edge3 = (triangle.p3, triangle.p1)
        edges.extend([edge1, edge2, edge3])

    fig, ax = plt.subplots()
    x_cords = [p[0] for p in points]
    y_cords = [p[1] for p in points]
    ax.scatter(x_cords, y_cords, color='blue', label='Points')

    for edge in edges:
        p1, p2 = edge
        x_values = [p1[0], p2[0]]
        y_values = [p1[1], p2[1]]
        ax.plot(x_values, y_values, color='red', label='Edges')

    plt.grid(True)
    plt.show()
    
def sort_triangle(triangle):
    p1 = triangle.p1
    p2 = triangle.p2
    p3 = triangle.p3
    temp = tuple(sorted([tuple(p1), tuple(p2), tuple(p3)]))
    triangle.p1 = temp[0]
    triangle.p2 = temp[1]
    triangle.p3 = temp[2]

def generateRandomPoints(num_points, num_range):
    points = []
    for i in range(num_points):
        x = random.randint(0,num_range)
        y = random.randint(0,num_range)
        points.append((x,y))
    return points
    
def bowyer_waston(points):
    triangulation = []
    super_triangle = Project.triangle((-15, -5), (35,-5), (15,50))
    triangulation.append(super_triangle)

    for point in points:
        bad_triangles = set()
        for triangle in triangulation:
            sort_triangle(triangle)
            if circumcircle(triangle.p1, triangle.p2, triangle.p3, point):
                bad_triangles.add(triangle)

        polygon = Project.polygon()
        for triangle in bad_triangles:
            sort_triangle(triangle)
            edges = [(triangle.p1,triangle.p2), (triangle.p2, triangle.p3), (triangle.p3, triangle.p1)]
            for comp_triangle in bad_triangles:
                sort_triangle(comp_triangle)
                comp_edges = [(comp_triangle.p1, comp_triangle.p2), (comp_triangle.p2, comp_triangle.p3), (comp_triangle.p3, comp_triangle.p1)]
                comp_edges_reversed = [(comp_triangle.p2, comp_triangle.p1), (comp_triangle.p3, comp_triangle.p2), (comp_triangle.p1, comp_triangle.p3)]
                flag = False
                for edge in edges:
                    for comp_edge in comp_edges:
                        if edge == comp_edge and triangle != comp_triangle:
                            flag = True
                    for comp_edge_rev in comp_edges_reversed:
                        if edge == comp_edge_rev and triangle != comp_triangle:
                            flag = True
                    if flag == False:
                        polygon.edges.add(edge)
        for triangle in bad_triangles:
            sort_triangle(triangle)
            triangulation.remove(triangle)
        for edge in polygon.edges:
            new_tri = Project.triangle(edge[0], edge[1], point)
            sort_triangle(new_tri)
            triangulation.append(new_tri)
    flagged_triangles = []
    for triangle in triangulation:
        sort_triangle(triangle)
        if triangle.p1 == (-15, -5) or triangle.p2 == (-15, -5) or triangle.p3 == (-15, -5) or triangle.p1 == (35,-5) or triangle.p2 == (35,-5) or triangle.p3 == (35,-5) or triangle.p1 == (15,50) or triangle.p2 == (15,50) or triangle.p3 == (15,50):
            flagged_triangles.append(triangle)
    for triangle in flagged_triangles:
        sort_triangle(triangle)
        triangulation.remove(triangle)
    return triangulation

def main():
    num_points = int(input("Enter the number of points: "))
    points = generateRandomPoints(num_points, 20)
    print(points)
    delaunay_triangulation = bowyer_waston(points)
    plot_initial_and_delaunay(delaunay_triangulation, points)
   

if __name__ == "__main__":
    main()