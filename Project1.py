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

    def verticies(self):
        return (self.p1, self.p2, self.p3)


class edge():
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2


#  to find if the points are clockwise or counterclockwise use the vector cross
#  product https://algs4.cs.princeton.edu/91primitives/
#  if determinant is less than 0, the points are clockwise
#  if determinant is greater than 0, the points are counter-clockwise
def findDeterminant(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p3[0] - p1[0]) * (p2[1] - p1[1])


def circumcircle(p1, p2, p3, p4):
    #  When A, B, C are sorted in a counterclockwise order, this determinant is
    #  positive only if D lies inside the circumcircle (Wiki page)
    if findDeterminant(p1, p2, p3) < 0:
        p2, p3 = p3, p2  # swap points to make counter-clockwise

    ax, ay = p1[0] - p4[0], p1[1] - p4[1]
    bx, by = p2[0] - p4[0], p2[1] - p4[1]
    cx, cy = p3[0] - p4[0], p3[1] - p4[1]

    det = np.linalg.det([
        [ax, ay, ax**2 + ay**2],
        [bx, by, bx**2 + by**2],
        [cx, cy, cx**2 + cy**2]
    ])
    return det > 0


def plot_initial_and_delaunay(points, initial_edges, delaunay_edges):
    """Plot the initial triangulation and Delaunay triangulation side by side."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # Plot initial triangulation
    axes[0].set_title("Initial Triangulation")
    for edge in initial_edges:
        x_coords = [points[edge[0]][0], points[edge[1]][0]]
        y_coords = [points[edge[0]][1], points[edge[1]][1]]
        axes[0].plot(x_coords, y_coords, 'b-')
    axes[0].scatter([p[0] for p in points], [p[1]
                    for p in points], color='red')
    axes[0].set_xlabel("X")
    axes[0].set_ylabel("Y")

    # Plot Delaunay triangulation
    axes[1].set_title("Delaunay Triangulation")
    for edge in delaunay_edges:
        x_coords = [points[edge[0]][0], points[edge[1]][0]]
        y_coords = [points[edge[0]][1], points[edge[1]][1]]
        axes[1].plot(x_coords, y_coords, 'b-')
    axes[1].scatter([p[0] for p in points], [p[1]
                    for p in points], color='red')
    axes[1].set_xlabel("X")
    axes[1].set_ylabel("Y")

    plt.tight_layout()
    plt.show()


def generateRandomArray(num_points, num_range):
    points = []
    for i in range(num_points):
        x = random.randint(0, num_range)
        y = random.randint(0, num_range)
        points.append((x, y))
    return points


def sortEdge(edge):
    return tuple(sorted(edge))


def sortTriangle(p1, p2, p3):
    return tuple(sorted([tuple(p1), tuple(p2), tuple(p3)]))


def bowyer_waston(points):
    triangulation = set()

    min_x, min_y = np.min(points, axis=0)
    max_x, max_y = np.max(points, axis=0)
    dx, dy = max_x - min_x, max_y - min_y
    delta = max(dx, dy) * 10

    p1 = (min_x - delta, min_y - delta)
    p2 = (max_x + delta, min_y - delta)
    p3 = ((min_x + max_x)/2, max_y + delta)

    super_triangle = Project.triangle(p1, p2, p3)
    triangulation.add(super_triangle)

    for point in points:
        bad_triangles = set()
        for triangle in triangulation:
            if circumcircle(triangle.p1, triangle.p2, triangle.p3, point):
                # print(findDeterminant(triangle.p1, triangle.p2, triangle.p3))
                bad_triangles.add(triangle)

        edge_count = {}
        for triangle in bad_triangles:
            edges = [
                tuple(sorted((triangle.p1, triangle.p2))),
                tuple(sorted((triangle.p2, triangle.p3))),
                tuple(sorted((triangle.p3, triangle.p1)))
            ]
            for edge in edges:
                edge_count[edge] = edge_count.get(edge, 0) + 1

        boundary = [e for e, count in edge_count.items() if count == 1]

        triangulation.difference_update(bad_triangles)

        for edge in boundary:
            new_tri = Project.triangle(edge[0], edge[1], point)
            triangulation.add(new_tri)

    final_tri = set()

    for tri in triangulation:  # remove supercircle and its associated triangles
        if p1 in tri.verticies() or p2 in tri.verticies() or p3 in tri.verticies():
            continue
        final_tri.add(tri)

    return final_tri


def main():
    # num_points = int(input("Enter the number of points: "))
    # points = generateRandomArray(num_points, 20)
    points = [[19, 11], [0, 4], [15, 6], [10, 6], [6, 11], [
        5, 17], [2, 16], [1, 17], [2, 6], [0, 12]]
    print(points)
    triangles = bowyer_waston(points)
    for i, tri in enumerate(triangles, 1):
        print(f"triangle {i}: {tri.p1}, {tri.p2}, {tri.p3}")

    for tri in triangles:
        x = [tri.p1[0], tri.p2[0], tri.p3[0], tri.p1[0]]
        y = [tri.p1[1], tri.p2[1], tri.p3[1], tri.p1[1]]
        plt.plot(x, y, 'k-')

    plt.show()


if __name__ == "__main__":
    main()
