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

def circumcircle(p1, p2, p3, p4):
    ax, ay = p1
    bx, by = p2
    cx, cy = p3
    dx, dy = p4

    det = np.linalg.det([
        [ax, ay, ax**2 + ay**2, 1],
        [bx, by, bx**2 + by**2, 1],
        [cx, cy, cx**2 + cy**2, 1],
        [dx, dy, dx**2 + dy**2, 1]
    ])
    return det >= 0

def plot_initial_and_delaunay(points, initial_edges, delaunay_edges):
    """Plot the initial triangulation and Delaunay triangulation side by side."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # Plot initial triangulation
    axes[0].set_title("Initial Triangulation")
    for edge in initial_edges:
        x_coords = [points[edge[0]][0], points[edge[1]][0]]
        y_coords = [points[edge[0]][1], points[edge[1]][1]]
        axes[0].plot(x_coords, y_coords, 'b-')
    axes[0].scatter([p[0] for p in points], [p[1] for p in points], color='red')
    axes[0].set_xlabel("X")
    axes[0].set_ylabel("Y")

    # Plot Delaunay triangulation
    axes[1].set_title("Delaunay Triangulation")
    for edge in delaunay_edges:
        x_coords = [points[edge[0]][0], points[edge[1]][0]]
        y_coords = [points[edge[0]][1], points[edge[1]][1]]
        axes[1].plot(x_coords, y_coords, 'b-')
    axes[1].scatter([p[0] for p in points], [p[1] for p in points], color='red')
    axes[1].set_xlabel("X")
    axes[1].set_ylabel("Y")

    plt.tight_layout()
    plt.show()

def generateRandomArray(num_points, num_range):
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
    i = 0

    for point in points:
        bad_triangles = []
        for triangle in triangulation:
            if circumcircle(triangle.p1, triangle.p2, triangle.p3, point):
                bad_triangles.append(triangle)
                #print(f"Point {i} in circle")
                i = i+1
                #print(f"bad triangle added")

        polygon = Project.polygon()
        for triangle in bad_triangles:
            edges = [(triangle.p1,triangle.p2), (triangle.p2, triangle.p3), (triangle.p3, triangle.p1)]
            #print(edges)
            for comp_triangle in bad_triangles:
                comp_edges = [(comp_triangle.p1, comp_triangle.p2), (comp_triangle.p2, comp_triangle.p3), (comp_triangle.p3, comp_triangle.p1)]
                #print(comp_edges)
                flag = False
                for edge in edges:
                    for comp_edge in comp_edges:
                        if edge == comp_edge and triangle != comp_triangle:
                            flag = True
                    if flag == False:
                        polygon.edges.add(edge)
        for triangle in bad_triangles:
            triangulation.remove(triangle)
        for edge in polygon.edges:
            new_tri = Project.triangle(edge[0], edge[1], point)
            triangulation.append(new_tri)
    for triangle in triangulation:
        if triangle.p1 == (-15, -5) or triangle.p2 == (-15, -5) or triangle.p3 == (-15, -5) or triangle.p1 == (35,-5) or triangle.p2 == (35,-5) or triangle.p3 == (35,-5) or triangle.p1 == (15,50) or triangle.p2 == (15,50) or triangle.p3 == (15,50):
            triangulation.remove(triangle)
            print(f"Removed: {triangle}")
            print(f"points: {triangle.p1} {triangle.p2} {triangle.p3}")
    return triangulation

            

def main():
    num_points = int(input("Enter the number of points: "))
    points = generateRandomArray(num_points, 20)
    print(points)
    trii = bowyer_waston(points)
    i = 1
    for tir in trii:
        print(f"Triangle {i}: {tir.p1} {tir.p2} {tir.p3} {tir}")
        i = i+1

if __name__ == "__main__":
    main()