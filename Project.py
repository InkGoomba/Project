import matplotlib.pyplot as plt
import numpy as np
from plotsLib import plots

def is_delaunay(p1, p2, p3, p4):
    """Check if the edge flip is needed to satisfy the Delaunay condition."""
    ax, ay = p1
    bx, by = p2
    cx, cy = p3
    dx, dy = p4

    # Matrix determinant to check if point p4 lies inside the circumcircle of triangle (p1, p2, p3)
    det = np.linalg.det([
        [ax, ay, ax**2 + ay**2, 1],
        [bx, by, bx**2 + by**2, 1],
        [cx, cy, cx**2 + cy**2, 1],
        [dx, dy, dx**2 + dy**2, 1]
    ])
    print(f"Checking Delaunay condition for points {p1}, {p2}, {p3}, {p4}: Determinant = {det}")  # Debugging
    return det <= 0

def edge_flipping(points, edges):
    """Perform edge flipping to convert the triangulation into a Delaunay triangulation."""
    edges = edges[:]
    flipped = True

    while flipped:
        flipped = False
        for i, (a, b) in enumerate(edges):
            # Find triangles sharing the edge (a, b)
            triangles = []
            for c in range(len(points)):
                if c != a and c != b and {a, b, c}.issubset(set(sum(edges, []))):
                    triangles.append((a, b, c))

            if len(triangles) == 2:
                (a, b, c1), (a, b, c2) = triangles

                print(f"Checking edge ({a}, {b}) with triangles ({a}, {b}, {c1}) and ({a}, {b}, {c2})")  # Debugging

                if not is_delaunay(points[a], points[b], points[c1], points[c2]):
                    print(f"Flipping edge ({a}, {b}) to ({c1}, {c2})")  # Debugging
                    # Flip the edge
                    edges[i] = (c1, c2)
                    edges.append((a, c1))
                    edges.append((b, c2))
                    flipped = True

        # Debugging: Print the current state of edges after each iteration
        print(f"Current edges after iteration: {edges}")

        # Remove duplicate edges after flipping
        edges = list(set(tuple(sorted(edge)) for edge in edges))  # Ensure consistent ordering of edges

    # Debugging: Final state of edges
    print(f"Final edges: {edges}")

    return edges

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

def verify_delaunay(points, edges):
    """Verify if the given triangulation satisfies the Delaunay condition."""
    for i, (a, b) in enumerate(edges):
        for c in range(len(points)):
            if c != a and c != b:
                for d in range(len(points)):
                    if d != a and d != b and d != c:
                        if not is_delaunay(points[a], points[b], points[c], points[d]):
                            return False
    return True

# Update main function to include verification
def main():
    case_num = int(input("Enter the case number (0-10): "))
    points, edges = plots.plots_select(case_num)
    delaunay_edges = edge_flipping(points, edges)

    # Verify if the initial triangulation is already Delaunay
    if verify_delaunay(points, edges):
        print("The initial triangulation already satisfies the Delaunay condition.")
    else:
        print("The initial triangulation does not satisfy the Delaunay condition.")

    # Plot initial and Delaunay triangulations side by side
    plot_initial_and_delaunay(points, edges, delaunay_edges)

if __name__ == "__main__":
    main()