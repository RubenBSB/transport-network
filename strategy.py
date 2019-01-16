import copy
from cost import average_travelling_time, building_cost
from data.data_preprocess import df_stations

def is_neighbour(u, v, G):
    """Returns True if u and v are neighbours in graph G."""
    for [station, _] in G[u]:
        if station == v:
            return True
    return False

def add_edge(edge, G):
    """Returns a copy of G added with 'edge'."""
    u, v, dist = edge
    G_copy = copy.deepcopy(G)
    G_copy[u].append([v,dist])
    G_copy[v].append([u,dist])
    return G_copy

def get_utility(edge, G, alpha, traffic, V):
    """Computes the ratio between time saved by adding 'edge' and additional building cost."""
    att_G = average_travelling_time(G, traffic, V)
    att_G_added = average_travelling_time(add_edge(edge, G),traffic, V)
    additional_cost = alpha * edge[2]
    return ((att_G-att_G_added)/(additional_cost+10**(-8)))

def get_utilities(edge_list, G, alpha, traffic, V):
    """Returns the utilities for each edge of 'G' in 'edge_list'."""
    utilities = [[get_utility(edge, G, alpha, traffic, V), edge] for edge in edge_list]
    return utilities

# def aretesFreq(l):
#     L = [[arete[0], arete[1], freq[arete[0]][1] * freq[arete[1]][1] / (M[arete[0]][arete[1]])] for arete in l]
#     return L

def sort_utilities(edge_list):
    """Recursive quicksort on all edges according to their utility."""
    if edge_list == []:
        return []
    else:
        pivot = edge_list[0][0]
        l1, l2 = [], []
        for k in range(1, len(edge_list)):
            if edge_list[k][0] >= pivot:
                l2.append(edge_list[k])
            else:
                l1.append(edge_list[k])
        return (sort_utilities(l2) + [edge_list[0]] + sort_utilities(l1))

def shortest_edges(sorted_edges, G, rest_edges):
    """Complete 'rest_edges', which is a list of potential edges for G, with the shortest
     edges of 'sorted_edges' in order to have 10 edges candidates."""
    selected_edges = []
    k = 0
    while len(selected_edges + rest_edges) < 10:
        i,j,dist = sorted_edges[k]
        if not is_neighbour(i,j,G):
            selected_edges.append(sorted_edges[k])
        k += 1
    return selected_edges + [rest_edges[i][1] for i in range(len(rest_edges))], k

def max_utility(edge_list):
    """Returns (utility,edge) with maximum utility in 'edge_list'."""
    max_ut = edge_list[0][0]
    max_edge = edge_list[0][1]
    for utility,edge in edge_list:
        if utility > max_ut:
            max_ut = utility
            max_edge = edge
    return (max_ut, max_edge)


def keep_half(edge_list, value):
    """Keep edges from 'edge_list' that have a utility higher than value/2."""
    best_edges = [ [utility,edge] for utility,edge in edge_list if utility > value / 2 and utility != value]
    return best_edges


def heuristic(initial_G, max_cost, sorted_edges,alpha, traffic, V):
    """Starting from the graph 'initial_G', we add the best edges while the global building cost is
    less than 'max_cost'."""
    G = copy.deepcopy(initial_G)
    edge_list = sorted_edges
    rest_edges = []
    added_edges = []
    while building_cost(G,alpha)*0.001 < max_cost:
        edges, k = shortest_edges(edge_list, G, rest_edges)
        utilities = get_utilities(edges, G, alpha, traffic, V)
        max_ut, max_edge = max_utility(utilities)
        i, j, dist = max_edge
        print("A tunnel between "+ df_stations['station'][i] +"and"+ df_stations['station'][j]
              +" was added to the graph.")
        print("The building cost has increased by "+ str(round(dist*alpha,2)) +" million euros and is now "+
              str(round(building_cost(G,alpha)*0.001,2)) +".")
        G[i].append([j,dist])
        G[j].append([i,dist])
        added_edges.append(max_edge)
        rest_edges = keep_half(utilities, max_ut)
        edge_list = edge_list[(k + 1):]
    return G, added_edges





