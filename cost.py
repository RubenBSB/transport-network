from heapq import *
import numpy as np

def get_distances(start, graph):
    """Dijkstra's algorithm to compute the length of the shortest path between station 'start'
    and any other station of 'graph'."""
    m = len(graph)
    dist = [None] * m
    queue = [(0, start)]
    while queue:
        path_len, v = heappop(queue)
        if dist[v] is None: # v is unvisited
            dist[v] = path_len
            for w, edge_len in graph[v]:
                if dist[w] is None:
                    heappush(queue, (path_len + edge_len, w))
    return [0 if x is None else x for x in dist]

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
    F = sum(traffic)  # Total number of travellers over a year.
    dist_matrix = distance_matrix(graph)
    m = len(dist_matrix)
    S = []
    for i in range(m):
        for j in range(m):
            if dist_matrix[i][j] != -1:
                S.append((dist_matrix[i][j] / V) * traffic[i] * traffic[j] / F ** 2)
    return sum(S)*60

def building_cost(graph, alpha):
    """Computes the building cost of a graph by summing the lengths of every tunnels and multiplying it by
    the cost of one kilometer 'alpha'."""
    m = len(graph)
    distance_total = 0
    for station in graph:
        for [_, dist] in graph[station]:
            distance_total += dist
    distance_total = distance_total / 2     # We counted twice each tunnel.
    return distance_total * alpha

