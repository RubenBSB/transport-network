from math import radians, cos, sin, asin, sqrt
import matplotlib.pyplot as plt
import numpy as np
from data.data_preprocess import df_stations

x = [long for long in df_stations['longitude'].values]
y = [lat for lat in df_stations['latitude'].values]

m = len(df_stations)        # Here m = 302 subway stations

'''=================== Implementation of distances between stations =================='''

def euc_distance(A,B):
    """Simply returns the euclidean distance between points A and B."""
    return(np.sqrt(((B[0]-A[0])**2)+((B[1]-A[1])**2)))

def sph_distance_station(station1, station2):
    global df_stations
    """More elaborated distance that takes into account Earth spherical nature, given two subway stations."""
    lon1, lat1 = df_stations.loc[df_stations['station']==station1][['longitude','latitude']].values[0].tolist()
    lon2, lat2 = df_stations.loc[df_stations['station']==station2][['longitude','latitude']].values[0].tolist()
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r

def sph_distance_coordinate(lon1, lat1, lon2, lat2):
    global df_stations
    """Same function than before except that longitude and latitude are already known."""
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r

'''=================== Construction of the real parisian network ======================'''

import ast

with open('data/real_network.txt', encoding="utf-8") as file:
    real_network_structure = ast.literal_eval(file.read())

def station_index(station,df):
    """Returns the index of 'station' in the DataFrame 'df'."""
    for index, row in df.iterrows():
        if row['station'] == station:
            return index

def build_real_network(structure_list):
    """Creates the adjacency matrix of Paris subway network."""
    global m, dist_matrix, df_stations
    adj_matrix = np.zeros((m, m))
    for k in range(len(structure_list) - 1):
        if structure_list[k] == 'END_OF_LINE':
            pass
        elif structure_list[k + 1] == 'END_OF_LINE':
            pass
        else:
            i = station_index(structure_list[k],df_stations)
            j = station_index(structure_list[k + 1],df_stations)
            adj_matrix[i][j] = sph_distance_station(structure_list[k], structure_list[k+1])
            adj_matrix[j][i] = adj_matrix[i][j]
    for i in range(m):
        for j in range(m):
            if adj_matrix[i][j] == 0.0:
                adj_matrix[i][j], adj_matrix[j][i] = -1.0, -1.0
    return adj_matrix

def matrix_to_dic(adj_matrix):
    """Transforms the adjacency matrix of a graph into its adjacency dictionary."""
    m = len(adj_matrix)
    adj_dic = {}
    for i in range(m):
        adj_dic[i] = [[j,adj_matrix[i][j]] for j in range(m) if adj_matrix[i][j] != -1]
    return(adj_dic)

def display_graph(adj_dic, plot_title=''):
    """Plot a graph described by its adjacency dictionary 'adj_dic'."""
    global x,y
    plt.figure()
    plt.xlim(2.2, 2.5)
    plt.ylim(48.75, 49.0)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.scatter(x,y,marker='.',c='g')
    for station_id in adj_dic:
        for connected_station in adj_dic[station_id]:
            j = connected_station[0]
            plt.plot([x[station_id],x[j]],[y[station_id],y[j]],'g-',linewidth=0.5)
    plt.title(plot_title)
    plt.show()

