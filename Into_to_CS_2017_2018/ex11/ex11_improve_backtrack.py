#############################################################
# FILE : ex11.py
# WRITER : Daniel Magen
# EXERCISE : intro2cs ex11 2017-2018
# DESCRIPTION: this module contains the required methods
# to solve the map coloring problem more efficiently
#############################################################
import ex11_map_coloring


# from map_coloring_gui import color_map #uncomment if you installed the required libraries


def back_track_degree_heuristic(adj_dict, colors):
    """
    :param adj_dict: a dict of nodes and connections
    :param colors: available colors
    :return: a solution to the map coloring problem , if it exists,
    using a heuristic degree of node approach
    """
    adj_list_sorted_list = sorted(adj_dict,
                                  key=lambda node: len(adj_dict[node]),
                                  reverse=True)
    coloring_dict = {}
    coloring_exists = map_solve_helper(adj_dict,
                                       coloring_dict,
                                       adj_list_sorted_list,
                                       0,
                                       colors,
                                       ex11_map_coloring.coloring_is_legal)
    if coloring_exists:
        return coloring_dict


def back_track_MRV(adj_dict, colors):
    """
    :param adj_dict: a dict of nodes and connections
    :param colors: available colors
    :return: a solution to the map coloring problem, if it exists,
    using a least remaining colors approach,
    i.e the node with the least remaining colors will be colored first
    """
    adj_list_sorted_list = list(adj_dict.keys())
    coloring_dict = {}
    coloring_exists = map_solve_helper(adj_dict,
                                       coloring_dict,
                                       adj_list_sorted_list,
                                       0,
                                       colors,
                                       ex11_map_coloring.coloring_is_legal,
                                       back_track_MRV_sorter)
    if coloring_exists:
        return coloring_dict


def back_track_MRV_sorter(adj_list_sorted_list, adj_dict, coloring_dict,
                          index):
    """
    :param adj_list_sorted_list: a list of sorted nodes in the dict
    :param adj_dict: a dict of nodes and connections
    :param coloring_dict: a dict of nodes and their assigned colors
    :param index: an index in the adj_list_sorted_list
    :return: goes through the adj_list_sorted_list and sorts it from index+1
    onwards. it sorts it such that the node with the least available colors
    will appear first
    """
    if index >= len(adj_list_sorted_list) - 1:
        return adj_list_sorted_list

    part_not_change = adj_list_sorted_list[:index + 1]
    part_to_sort = adj_list_sorted_list[index + 1:]
    part_to_sort = sorted(part_to_sort,
                          key=lambda node: count_neighbours_colored(node,
                                                                    adj_dict,
                                                                    coloring_dict),
                          reverse=True)
    return part_not_change + part_to_sort


def count_neighbours_colored(node, adj_dict, coloring_dict):
    """
    :param node: a node in the dict
    :param adj_dict: a dict of nodes and connections
    :param coloring_dict: a dict of nodes and their assigned colors
    :return: how many of the nodes neighbours are in the coloring_dict
    """
    return count_how_many_in_dict(adj_dict[node], coloring_dict)


def count_how_many_in_dict(lis, dict_ot_items):
    """
    :param lis: a list of items
    :param dict_ot_items: a dict of items
    :return: how many items in the list are keys in the dict
    """
    counter = 0
    dict_keys = list(dict_ot_items.keys())
    for item in lis:
        if item in dict_keys:
            counter += 1
    return counter


def back_track_FC(adj_dict, colors):
    """
    :param adj_dict: a dict of nodes and connections
    :param colors: available colors
    :return: a solution to the map coloring problem, if it exists,
    such that each choice is also checked for the node neighbours
    """
    adj_list_sorted_list = list(adj_dict.keys())
    coloring_dict = {}
    coloring_exists = map_solve_helper(adj_dict,
                                       coloring_dict,
                                       adj_list_sorted_list,
                                       0,
                                       colors,
                                       back_track_FC_legal_assignment,
                                       None,
                                       None,
                                       len(colors))
    if coloring_exists:
        return coloring_dict


def back_track_FC_legal_assignment(nodes_coloring,
                                   node_to_check,
                                   nodes_and_connections_dict,
                                   num_of_colors):
    """
    :param nodes_coloring: coloring_dict: a dict of nodes and their
    assigned colors
    :param node_to_check: a node in the nodes_and_connections_dict
    :param nodes_and_connections_dict: a dict representing the nodes
    and their connections
    :param num_of_colors: number of colors available
    :return: True if the color of the node is legal and all the neighbours
    of the node can still be colored
    False otherwise
    """
    coloring_legal = ex11_map_coloring.coloring_is_legal(nodes_coloring,
                                                         node_to_check,
                                                         nodes_and_connections_dict)

    if not coloring_legal:
        return False

    return check_neighbours_can_still_be_colored(node_to_check,
                                                 nodes_and_connections_dict,
                                                 nodes_coloring,
                                                 num_of_colors)


def check_neighbours_can_still_be_colored(node, adj_dict, coloring_dict,
                                          num_of_colors):
    """
    :param node: a node in the dict
    :param adj_dict: a dict of nodes and connections
    :param coloring_dict: a dict of nodes and their assigned colors
    :param num_of_colors: number of colors available
    :return: True if all the neighbours of the given node can still be colored
    False otherwise
    """
    for neighbour in adj_dict[node]:
        if not node_can_still_be_colored(neighbour,
                                         adj_dict,
                                         coloring_dict,
                                         num_of_colors):
            return False

    return True


def node_can_still_be_colored(node, adj_dict, coloring_dict, num_of_colors):
    """
    :param node: a node in the dict
    :param adj_dict: a dict of nodes and connections
    :param coloring_dict: a dict of nodes and their assigned colors
    :param num_of_colors: number of colors available
    :return: True if the given node can still be colored
    False otherwise
    """
    nodes_connected_to_colors = get_neighbors_colors(node,
                                                     adj_dict,
                                                     coloring_dict)

    if len(nodes_connected_to_colors) > num_of_colors:
        return False

    return True


def back_track_LCV(adj_dict, colors):
    """
    :param adj_dict: a dict of nodes and connections
    :param colors: available colors
    :return: a solution to the map coloring problem, if it exists, using the
    least constraining value approach, i.e.  only the color that will constrain
    the next coloring the least is chosen each time
    """
    adj_list_sorted_list = list(adj_dict.keys())
    coloring_dict = {}
    coloring_exists = map_solve_helper(adj_dict,
                                       coloring_dict,
                                       adj_list_sorted_list,
                                       0,
                                       colors,
                                       ex11_map_coloring.coloring_is_legal,
                                       None,
                                       colors_sorting_func_for_LCV)
    if coloring_exists:
        return coloring_dict


def colors_sorting_func_for_LCV(node, adj_dict, coloring_dict, colors):
    """
    :param node: a node in the dict
    :param adj_dict: a dict of nodes and connections
    :param coloring_dict: a dict of nodes and their assigned colors
    :param colors: colors that are available
    :return: a new list of colors
    sorted by the color that will give the least constrains
    """
    colors_copy = list(tuple(colors))
    colors_copy = sorted(colors_copy,
                         key=lambda color: get_coloring_options_left(node,
                                                                     adj_dict,
                                                                     coloring_dict,
                                                                     len(colors),
                                                                     color),
                         reverse=True)
    return colors_copy


def get_coloring_options_left(node, adj_dict, coloring_dict, num_of_colors,
                              suggested_color):
    """
    :param node: a node in the dict
    :param adj_dict: a dict of nodes and connections
    :param coloring_dict: a dict of nodes and their assigned colors
    :param num_of_colors: how many colors that are available
    :param suggested_color: a color that the given node will be colored with
    :return: how many total coloring options the node neighbors will have left
    if the node will be colored by the suggested color
    """
    total_options_left = 0
    for neighbor in adj_dict[node]:
        if neighbor in coloring_dict:
            neighbor_neighbors_colors = get_neighbors_colors(neighbor,
                                                             adj_dict,
                                                             coloring_dict)
            neighbor_neighbors_colors.add(suggested_color)
            total_options_left += num_of_colors - len(
                neighbor_neighbors_colors)
        else:
            total_options_left += num_of_colors - 1

    return total_options_left


def get_neighbors_colors(node, adj_dict, coloring_dict):
    """
    :param node: a node in the dict
    :param adj_dict: a dict of nodes and connections
    :param coloring_dict: a dict of nodes and their assigned colors
    :return: a set containing all the colors of the neighbors of the given node
    """
    nodes_connected_to = adj_dict[node]
    nodes_connected_to_colors = set([])

    for node in nodes_connected_to:
        if node in coloring_dict:
            nodes_connected_to_colors.add(coloring_dict[node])

    return nodes_connected_to_colors


def map_solve_helper(adj_dict,
                     coloring_dict,
                     adj_list_sorted_list,
                     index,
                     colors,
                     legal_assignment_func,
                     adj_list_sorting_function=None,
                     colors_sorting_func=None,
                     *args):
    """
    :param adj_dict: dict that contains the values given for each item
    :param coloring_dict: a dict that will give each node a coloring
    :param adj_list_sorted_list: a list of nodes
    :param index: an index in adj_list_sorted_list
    :param colors: possible colors for the nodes
    :param legal_assignment_func: check that the assignment made is legal
    :param adj_list_sorting_function: will sort the adj_list_sorted_list
    after each assignment, defaults to None
    :param colors_sorting_func: will sort the colors given each time the
    function is called, defaults to None
    :param args: possible args given to the legal_assignment_func
    :return: if a solution to the given problem is possible it returns True
    otherwise it returns True
    it changes the dict_items_to_vals given
    """

    # base case, got to the end without illegal moves
    if index >= len(adj_list_sorted_list):
        return True

    # the given dict_items_to_vals should not be changed if there are no
    # legal moves, this will help restore dict_items_to_vals to the way
    # it was if there were no legal moves
    dict_has_value = adj_list_sorted_list[index] in coloring_dict
    if dict_has_value:
        dict_at_value = coloring_dict[adj_list_sorted_list[index]]

    # sorts the colors using colors_sorting_func
    if colors_sorting_func is not None:
        colors = colors_sorting_func(adj_list_sorted_list[index],
                                     adj_dict,
                                     coloring_dict,
                                     colors)

    for color in colors:
        coloring_dict[adj_list_sorted_list[index]] = color
        if legal_assignment_func(coloring_dict,
                                 adj_list_sorted_list[index],
                                 adj_dict,
                                 *args):

            if adj_list_sorting_function is not None:
                # sorts adj_list_sorted_list using adj_list_sorting_function
                adj_list_sorted_list = adj_list_sorting_function(
                    adj_list_sorted_list,
                    adj_dict,
                    coloring_dict,
                    index)

            if map_solve_helper(adj_dict,
                                coloring_dict,
                                adj_list_sorted_list,
                                index + 1,
                                colors,
                                legal_assignment_func,
                                adj_list_sorting_function,
                                colors_sorting_func,
                                *args):
                return True

    # restore dict_items_to_vals to the way it was
    if not dict_has_value:
        del coloring_dict[adj_list_sorted_list[index]]
    else:
        coloring_dict[adj_list_sorted_list[index]] = dict_at_value

    return False


def fast_back_track(adj_dict, colors):
    """
    bonus - not implemented
    :param adj_dict:
    :param colors:
    :return:
    """
    pass
