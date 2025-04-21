import matplotlib.pyplot as plt
import  numpy as np
from scipy.spatial import Delaunay

points = np.array([[3.0, 0.0], [2.0, 0.0], [2.0, 0.75], 
                   [2.5, 0.75]]) 
  
tri = Delaunay(points) 
  
# Visualize the triangulation 
plt.triplot(points[:,0], points[:,1], tri.simplices.copy()) 
plt.plot(points[:,0], points[:,1], 'o') 
plt.show() 