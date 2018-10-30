import numpy as np
import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt
from data_preprocess import df_stations

x=[long for long in df_stations['longitude'].values]
y=[lat for lat in df_stations['latitude'].values]


plt.xlim(2.2, 2.5)
plt.ylim(48.75, 49.0)
plt.gca().set_aspect('equal', adjustable='box')
plt.scatter(x,y,marker='.')
plt.title('Subway stations in Paris')
plt.show()

m = len(df_stations)        # Here m = 302 subway stations

'''=================== Construction of the adjacency matrix =================='''

def eucDistance(A,B):
    """Simply returns the euclidean distance between points A and B."""
    return(np.sqrt(((B[0]-A[0])**2)+((B[1]-A[1])**2)))

def sphDistance(lon1, lat1, lon2, lat2):
    """More elaborated distance that takes into account Earth spherical nature, given the longitude and latitude of
    two points.
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r

adj_matrix = np.zeros((m,m))

for j in range(m):
    for i in range(j):
        adj_matrix[i][j] = sphDistance(y[i],x[i],y[j],x[j])
        adj_matrix[j][i] = adj_matrix[i][j]