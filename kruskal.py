import numpy as np
from data.data_preprocess import df_stations
from network_building import sph_distance_coordinate, display_graph


x=[long for long in df_stations['longitude'].values]
y=[lat for lat in df_stations['latitude'].values]

m = len(x)

edges = []
dist_matrix = np.zeros((m,m))
for i in range(m):
    for j in range(i):
        dist_ij = sph_distance_coordinate(x[i], y[i], x[j], y[j])
        dist_matrix[i][j] = dist_ij
        dist_matrix[j][j] = dist_matrix[i][j]
        edges.append([i,j,dist_ij])

def sort_edges(edge_list):
    """Recursive quicksort on all edges according to their distance."""
    if edge_list == []:
        return []
    else:
        pivot = edge_list[0][2]
        l1, l2 = [], []
        for k in range(1, len(edge_list)):
            if edge_list[k][2] >= pivot:
                l2.append(edge_list[k])
            else:
                l1.append(edge_list[k])
        return (sort_edges(l1) + [edge_list[0]] + sort_edges(l2))

def is_in_graph(node, graph):
    """Tells if a node (i.e a subway station) is in 'graph' which is a network represented by
     an adjency dictionary """
    try:
        if graph[node] != []:
            return True
        else:
            return False
    except:
        return False

def get_component(node, component_list):
    """Returns the connected component (which is a list of nodes) which contains a particular node
     among a list of other components"""
    for component in component_list:
        if node in component:
            return component

def add_component(node1, node2, component_list):
    """Add 'node2' in the component of 'node1'."""
    component1 = get_component(node1, component_list)
    return [component for component in component_list if component != component1] + [component1 + [node2]]


def concat_components(node1, node2, component_list):
    """Concatenate the component of 'node1' with the component of 'node2'."""
    component1 = get_component(node1, component_list)
    component2 = get_component(node2, component_list)
    if component1 == component2:
        return component_list
    else:
        return [component for component in component_list if (component != component1 and component != component2)] + [component1 + component2]


def new_dic(n):
    """Creates a new dictionary with n nodes and no edges."""
    dic = {}
    for k in range(n):
        dic[k] = []
    return dic


def get_MST(edge_list):
    """Kruskal algorithm : we add the smallest edge that doesn't create a cycle in the graph while it is possible to do so."""
    global m, dist_matrix
    tree = new_dic(m)
    component_list = []
    for edge in edge_list:
        i, j = edge[0], edge[1]
        dist_ij = dist_matrix[i][j]
        if not is_in_graph(i, tree)  and not is_in_graph(j, tree):
            tree[i].append([j,dist_ij])
            tree[j].append([i,dist_ij])
            component_list.append([i,j])
        elif is_in_graph(i, tree) and not is_in_graph(j, tree):
            tree[i].append([j,dist_ij])
            tree[j].append([i,dist_ij])
            component_list = add_component(i,j, component_list)
        elif is_in_graph(j, tree) and not is_in_graph(i, tree):
            tree[i].append([j,dist_ij])
            tree[j].append([i,dist_ij])
            component_list = add_component(j, i, component_list)
        else:
            if j in get_component(i, component_list):
                pass
            else:
                tree[i].append([j,dist_ij])
                tree[j].append([i,dist_ij])
                component_list = concat_components(i,j,component_list)
    return tree


