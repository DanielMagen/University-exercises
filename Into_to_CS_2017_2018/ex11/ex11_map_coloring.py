#############################################################
# FILE : ex11.py
# WRITER : Daniel Magen
# EXERCISE : intro2cs ex11 2017-2018
# DESCRIPTION: this module contains methods used to load and solve
# a map coloring problem
#############################################################
from ex11_backtrack import general_backtracking

# from map_coloring_gui import color_map #uncomment if you installed the required libraries

COLORS = ['red', 'blue', 'green', 'magenta', 'yellow', 'cyan']
SPLIT_NODE_AND_CONNECTION_BY = ":"
SPLIT_CONNECTIONS_BY = ","


def read_adj_file(adjacency_file):
    """
    :param adjacency_file: a file containing nodes and their connections
    :return: a dict representing the nodes and their connections
    """
    nodes_and_connections_dict = {}

    with open(adjacency_file, "r") as adjacency:
        nodes_and_connections = adjacency.read().splitlines()

    for node_and_connect in nodes_and_connections:
        node, connections = node_and_connect.split(
            SPLIT_NODE_AND_CONNECTION_BY)
        connections = connections.split(SPLIT_CONNECTIONS_BY)
        if connections[0] == '':
            connections = []
        nodes_and_connections_dict[node] = connections

    return nodes_and_connections_dict


def run_map_coloring(adjacency_file, num_colors=4, map_type=None):
    """
    :param adjacency_file: a file containing nodes and their connections
    :return: a dict representing the nodes and their connections
    :param num_colors: the number of colors to paint the map in
    :param map_type: not implemented in my code
    :return: True if a solution exists False otherwise
    """
    nodes_and_connections_dict = read_adj_file(adjacency_file)
    list_of_nodes = list(nodes_and_connections_dict.keys())
    nodes_coloring = {}

    solution_exits = general_backtracking(list_of_nodes,
                                          nodes_coloring,
                                          0,
                                          COLORS[:num_colors],
                                          coloring_is_legal,
                                          nodes_and_connections_dict)

    if solution_exits:
        return nodes_coloring

    return None


def coloring_is_legal(nodes_coloring, node_to_check,
                      nodes_and_connections_dict):
    """
    :param nodes_coloring: coloring_dict: a dict of nodes and their
    assigned colors
    :param node_to_check: a node in the nodes_and_connections_dict
    :param nodes_and_connections_dict: a dict representing the nodes
    and their connections
    :return: True if the color of the node is legal
    False otherwise
    """
    current_node_coloring = nodes_coloring[node_to_check]
    for nodes_connected in nodes_and_connections_dict[node_to_check]:
        if nodes_connected in nodes_coloring:
            if nodes_coloring[nodes_connected] == current_node_coloring:
                return False
    return True
