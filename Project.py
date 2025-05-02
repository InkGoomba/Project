import matplotlib.pyplot as plt
import numpy as np
from plotsLib import plots
import random
import Project

# Triangle structure to hold data for triangles
class triangle():
    def __init__(self, p1, p2, p3):
        self.p1 = (p1[0], p1[1])
        self.p2 = (p2[0], p2[1])
        self.p3 = (p3[0], p3[1])

# Polygon structure to hold the star shaped polyon made up of edges
class polygon():
    def __init__(self):
        self.edges = set()

# Method to determine whether or not the triangle needs to be swapped from clowise to counter clockwise
def findDeterminant(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p3[0] - p1[0]) * (p2[1] - p1[1])

# Method to find out if a point lies inside of the circumcirlce of a triangle(p1, p2 ,p3)
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

# Method to plot points visually
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
    
# Method to sort triangles so that they are uniformally read essentially (Triangle ABC = BAC etc.)
def sort_triangle(triangle):
    p1 = triangle.p1
    p2 = triangle.p2
    p3 = triangle.p3
    temp = tuple(sorted([tuple(p1), tuple(p2), tuple(p3)]))
    triangle.p1 = temp[0]
    triangle.p2 = temp[1]
    triangle.p3 = temp[2]

# Method to generate the starting random points inside our super triangle
def generateRandomPoints(num_points, num_range):
    points = []
    for i in range(num_points):
        x = random.randint(0,num_range)
        y = random.randint(0,num_range)
        points.append((x,y))
    return points
    
# Main method for running the alorithim
def bowyer_waston(points):
    # Create empty triangulation used for returning later
    triangulation = []
    # Create and add the super triangle to the triangulaion
    super_triangle = Project.triangle((-15, -5), (35,-5), (15,50))
    triangulation.append(super_triangle)

    # Itterate over every point that is generated
    for point in points:

        # Create a set of triangles who's circumcirlce contains our point
        bad_triangles = set()
        for triangle in triangulation:
            sort_triangle(triangle)
            if circumcircle(triangle.p1, triangle.p2, triangle.p3, point):
                bad_triangles.add(triangle)

        # Create a arbitrary polygon to cotain an outline of edges that makes a star shapped hole around the inserted points
        # This set of instructions is our current problem in our code and thus far have been able to figure out why not too many edges are being added
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
        
        # Remove all triangles affected by our points to make space for the new trinagles that connect to the inserted point
        # This set is also a problem as for some reason not all the bad triangles are being removed as some end up in the final
        # triangulation making some edges overlap or crossover each other
        for triangle in bad_triangles:
            sort_triangle(triangle)
            triangulation.remove(triangle)

        # Fill in the hole by creating triangles from each edge that surrounds our new points and add them to the triangulation
        for edge in polygon.edges:
            new_tri = Project.triangle(edge[0], edge[1], point)
            sort_triangle(new_tri)
            triangulation.append(new_tri)
    
    # After every point is inserted remove all triangles that either are the super triangle or that connect to it
    flagged_triangles = []
    for triangle in triangulation:
        sort_triangle(triangle)
        if triangle.p1 == (-15, -5) or triangle.p2 == (-15, -5) or triangle.p3 == (-15, -5) or triangle.p1 == (35,-5) or triangle.p2 == (35,-5) or triangle.p3 == (35,-5) or triangle.p1 == (15,50) or triangle.p2 == (15,50) or triangle.p3 == (15,50):
            flagged_triangles.append(triangle)
    for triangle in flagged_triangles:
        sort_triangle(triangle)
        triangulation.remove(triangle)
    return triangulation

# Entry Method
# Notes: This algorithim is close to working properly however just becuase of some weired list/tuple/ or object issues not all edges that
# should be removed are being removed. However all points are indeed triangulated and on a small scale the triangulations actually turn
# out good and are indeed Delaunay. Even some larger sets of points the triangulation is Delaunay too.
def main():
    num_points = int(input("Enter the number of points: "))
    points = generateRandomPoints(num_points, 20)
    print(points)
    delaunay_triangulation = bowyer_waston(points)
    plot_initial_and_delaunay(delaunay_triangulation, points)
   

if __name__ == "__main__":
    main()