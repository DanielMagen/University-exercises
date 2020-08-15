#############################################################
# FILE : ex11.py
# WRITER : Daniel Magen
# EXERCISE : intro2cs ex11 2017-2018
# DESCRIPTION: this module contains a single method called general_backtracking
# which is used to solve general backtracking problems
#############################################################

def general_backtracking(list_of_items, dict_items_to_vals, index,
                         set_of_assignments, legal_assignment_func,
                         *args):
    """
    :param list_of_items: list of items
    :param dict_items_to_vals: dict that contains the values given for each item
    :param index: an index in the item list
    :param set_of_assignments: set of possible assignments as values
    :param legal_assignment_func: check that the assignment made is legal
    :param args: possible args given to the legal_assignment_func
    :return: if a solution to the given problem is possible it returns True
    otherwise it returns True
    it changes the dict_items_to_vals given
    """

    # base case, got to the end without illegal moves
    if index >= len(list_of_items):
        return True

    # the given dict_items_to_vals should not be changed if there are no
    # legal moves, this will help restore dict_items_to_vals to the way
    # it was if there were no legal moves
    dict_has_value = list_of_items[index] in dict_items_to_vals
    if dict_has_value:
        dict_at_value = dict_items_to_vals[list_of_items[index]]

    for assignment in set_of_assignments:
        dict_items_to_vals[list_of_items[index]] = assignment
        if legal_assignment_func(dict_items_to_vals,
                                 list_of_items[index],
                                 *args):
            if general_backtracking(list_of_items,
                                    dict_items_to_vals,
                                    index + 1,
                                    set_of_assignments,
                                    legal_assignment_func,
                                    *args):
                return True

    # restore dict_items_to_vals to the way it was
    if not dict_has_value:
        del dict_items_to_vals[list_of_items[index]]
    else:
        dict_items_to_vals[list_of_items[index]] = dict_at_value

    return False
