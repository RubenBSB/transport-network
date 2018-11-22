from heapq import *
import numpy as np


def dist_inf(dist1, dist2):
    """Returns True if 'dist1' is less than 'dist2' knowing that -1.0 denotes infinity."""
    if dist1 == -1.0 and dist2 != -1.0:
        return False
    elif dist1 != -1.0 and dist2 == -1.0:
        return True
    elif dist1 == -1.0 and dist2 == -1.0:
        return False
    else:
        return (dist1 < dist2)


def dist_sum(dist1, dist2):
    """Returns the sum of 'dist1' and 'dist2' knowing that -1.0 denotes infinity."""
    if dist1 == -1.0 or dist2 == -1.0:
        return -1.
    else:
        return dist1 + dist2


def dist_min(dist1, dist2):
    """Returns the minimal value between 'dist1' and 'dist2' knowing that -1.0 denotes infinity."""
    if dist1 == -1:
        return dist2
    elif dist2 == -1:
        return dist1
    else:
        return min(dist1, dist2)


def get_distances(source, graph):
    """Dijkstra's algorithm to compute the length of the shortest path between station 'source'
    and any other station of 'graph'."""
    m = len(graph)
    distances_to_source = np.array(m * [-1.0])
    distances_to_source[source] = 0
    queue = [[0, source]]
    already_seen = np.zeros(n, bool)
    while queue != []:
        [dist_source_i, station_i] = heappop(f)
        if not already_seen[station_i]:
            already_seen[station_i] = True
            for [dist_ij, station_j] in graph[station_i]:
                c = som(dist_source_i, dist_ij)
                if inf(c, distances_to_source[station_j]):
                    distances_to_source[station_j] = c
                    heappush(f, [c, station_j])
    return distances_to_source


def distance_matrix(graph):
    """Returns the distance matrix of the graph which stores every distance between two stations."""
    m = len(graph)
    matrix = []
    for i in range(m):
        matrix.append(get_distances(i, graph))
    return np.array(matrix)


def average_travelling_time(graph, traffic, V):
    """Computes the average travelling time of 'graph' (in minutes) knowing its traffic distribution and the average velocity of a
    subway wagon 'V'."""
    F = sum(traffic[i] for i in range(len(traffic)))  # Total number of travellers over a year.
    dist_matrix = distance_matrix(graph)
    m = len(dist_matrix)
    S = []
    for i in range(m):
        for j in range(m):
            if dist_matrix[i][j] != -1:
                S.append((dist_matrix[i][j] / V) * traffic[i] * traffic[j] / F ** 2)
    return sum(L)*60

def building_cost(graph, alpha):
    """Computes the building cost of a graph by summing the lengths of every tunnels and multiplying it by
    the cost of one kilometer 'alpha'."""
    m = len(graph)
    distance_total = 0
    for station in graph:
        for [neighbour, dist] in G[station]:
            distance_total += dist
    distance_total = distance_total / 2     # We counted twice each tunnel.
    return distance_total * alpha

