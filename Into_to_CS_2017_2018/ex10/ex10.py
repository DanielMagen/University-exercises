#############################################################
# FILE : ex10.py
# WRITER : Daniel Magen
# EXERCISE : intro2cs ex10 2017-2018
# DESCRIPTION: this module contains the required classes and methods
# to identify an illness given its symptoms
#############################################################
from itertools import combinations


class Node:
    """
    a class representing a node in a tree
    each node has
    data
    and max 2 children each representing either a positive or a negative
    answer to the data in the node
    """

    def __init__(self, data="", pos=None, neg=None):
        self.data = data
        self.positive_child = pos
        self.negative_child = neg

    def get_data(self):
        """
        :return: the node data
        """
        return self.data

    def get_positive_child(self):
        """
        :return: the node positive child
        """
        return self.positive_child

    def get_negative_child(self):
        """
        :return: the node negative child
        """
        return self.negative_child

    def is_leaf(self):
        """
        :return: True if the node has no children false otherwise
        """
        return self.negative_child is None and self.positive_child is None

    def has_positive_child(self):
        """
        :return: True if the node has a positive child ,False otherwise
        """
        return self.positive_child is not None

    def has_negative_child(self):
        """
        :return: True if the node has a negative child ,False otherwise
        """
        return self.negative_child is not None

    def get_childs_list(self):
        """
        :return: a list of the node children
        """
        child_list = []

        if not self.negative_child is None:
            child_list.append(self.negative_child)

        if not self.positive_child is None:
            child_list.append(self.positive_child)

        return child_list

    def __repr__(self):
        return str(self.data)


class Record:
    """
    a class representing an illness and its symptoms
    """

    def __init__(self, illness, symptoms):
        self.illness = illness
        self.symptoms = symptoms

    def get_illness(self):
        """
        :return: the record illness
        """
        return self.illness

    def get_symptoms(self):
        """
        :return: the record illness symptoms
        """
        return self.symptoms


def parse_data(filepath):
    with open(filepath) as data_file:
        records = []
        for line in data_file:
            words = line.split()
            records.append(Record(words[0], words[1:]))
        return records


class Diagnoser:
    """
    a class representing a Diagnoser for illnesses that are ordered in a
    tree by their symptoms
    """

    def __init__(self, root):
        self.__root = root

    def diagnose(self, symptoms):
        """
        :param symptoms: list of symptoms
        :return: the illness that contains the most symptoms in the given
        symptoms list
        """
        current_node = self.__root
        while not current_node.is_leaf():
            if current_node.get_data() in symptoms:
                current_node = current_node.get_positive_child()
            else:
                current_node = current_node.get_negative_child()

        return current_node.get_data()

    def calculate_error_rate(self, records):
        """
        :param records: a list of records objects
        :return: the error_rate which is calculated by the number
        of wrong diagnosis divided by the total number of diagnosis made
        """
        wrong_diagnosis = 0

        for record in records:
            diagnosis_result = self.diagnose(record.get_symptoms())
            if diagnosis_result != record.get_illness():
                wrong_diagnosis += 1

        return wrong_diagnosis / len(records)

    def all_illnesses(self):
        """
        :return: all illnesses that the Diagnoser contains
        """
        set_of_illnesses = set([])
        self._all_illnesses_helper(self.__root, set_of_illnesses)
        return sorted(list(set_of_illnesses))

    def _all_illnesses_helper(self, node, set_of_illnesses):
        """
        :param node: a node object
        :param set_of_illnesses: a set containing illnesses strings
        :return: None

        it adds all the illnesses in the tree spanned by the given node
        to the set_of_illnesses given
        """
        if node.is_leaf():
            set_of_illnesses.add(node.get_data())
            return
        for child in node.get_childs_list():
            self._all_illnesses_helper(child, set_of_illnesses)

    def most_common_illness(self, records):
        """
        :param records: a list of records objects
        :return: the illness which was diagnosed the most given the
        symptoms in the records objects
        """
        most_common_illness_dict = {}

        for record in records:
            diagnosis_result = self.diagnose(record.get_symptoms())
            if diagnosis_result in most_common_illness_dict:
                most_common_illness_dict[diagnosis_result] += 1
                # add one the the number of times the diagnosis resulted
            else:
                # create a new entry in the dict that will represent the
                # number of times the diagnosis resulted ans set it to 1
                most_common_illness_dict[diagnosis_result] = 1

        # get the diagnosis that resulted the most times
        max_diagnosis_result = None
        max_diagnosis_result_times = 0
        for diagnosis_result in most_common_illness_dict:
            times_it_appeared = most_common_illness_dict[diagnosis_result]
            if times_it_appeared >= max_diagnosis_result_times:
                max_diagnosis_result_times = times_it_appeared
                max_diagnosis_result = diagnosis_result

        return max_diagnosis_result

    def paths_to_illness(self, illness):
        """
        :param illness: an illness string
        :return: a list of lists containing a path of True or False answers
        that would result in the diagnosis of the given illness
        """
        _, illness_paths = self._paths_to_illness_helper(self.__root, illness)
        return illness_paths

    def _paths_to_illness_helper(self, node, illness):
        """
        :param node: a node object
        :param illness: an illness string
        :return: a boolean indicating if the illness was found in a leaf of
        the tree spanned by the given node,
        and a list containing all the paths from the given node to the illness
        as lists of booleans representing answers
        """
        if node.is_leaf():
            # we got to a node containing the illness
            if node.get_data() == illness:
                return True, [[]]

        tree_contain_illness = False
        # a boolean indicating if the illness was found in a leaf of
        # the tree spanned by the given node,

        illness_paths = []
        # a list containing all the paths from the given node to the illness
        # as lists of booleans representing answers

        # calculate the paths to the illness from the positive_child
        # and add True at the start of all the paths that resulted
        if node.has_positive_child():
            has_illness, positive_child_illness_paths = \
                self._paths_to_illness_helper(node.get_positive_child(),
                                              illness)
            if has_illness:
                tree_contain_illness = True
                for path in positive_child_illness_paths:
                    path.insert(0, True)

            # adds the resulting paths to the illness_paths
            illness_paths += positive_child_illness_paths

        # calculate the paths to the illness from the negative_child
        # and add False at the start of all the paths that resulted
        if node.has_negative_child():
            has_illness, negative_child_illness_paths = \
                self._paths_to_illness_helper(node.get_negative_child(),
                                              illness)
            if has_illness:
                tree_contain_illness = True
                for path in negative_child_illness_paths:
                    path.insert(0, False)

            # adds the resulting paths to the illness_paths
            illness_paths += negative_child_illness_paths

        return tree_contain_illness, illness_paths


def build_tree(records, symptoms):
    """
    :param records: a list of records objects
    :param symptoms: a list of symptoms strings
    :return: a decision tree in which each node that is not a leaf will
    ask about a symptom in the symptoms given, such that each symptom will be
    asked about in the order they were given in the symptoms list.
    the leafs of the decision tree will be the diagnosis that is the best match
    for the symptoms given. the best match will be decided
    using the records given
    """
    symptoms_tree = create_symptoms_tree(symptoms, 0, records, records)
    return symptoms_tree


def create_symptoms_tree(symptoms, index_in_symptoms, records,
                         complete_records):
    """
    :param symptoms: a list of symptoms strings
    :param index_in_symptoms: an index in the list of symptoms
    :param records: a list of records objects
    :param complete_records: a non-empty list of records objects
    :return: a decision tree in which each node that is not a leaf will
    ask about a symptom in the symptoms given, such that each symptom will be
    asked about in the order they were given in the symptoms list.
    the leafs of the decision tree will be the diagnosis that is the best match
    for the symptoms given. the best match will be decided
    using the records given
    """
    if index_in_symptoms >= len(symptoms):
        # base case, add first record illness found into a new Node, return it
        data = complete_records[0].get_illness()
        if len(records) > 0:
            data = records[0].get_illness()
        diagnosis_node = Node(data)
        return diagnosis_node

    symptom = symptoms[index_in_symptoms]
    records_with_illnesses_that_contain_symptom = []
    records_with_illnesses_that_do_not_contain_symptom = []

    for record in records:
        if symptom in record.get_symptoms():
            records_with_illnesses_that_contain_symptom.append(record)
        else:
            records_with_illnesses_that_do_not_contain_symptom.append(record)

    return Node(symptoms[index_in_symptoms],
                create_symptoms_tree(symptoms,
                                     index_in_symptoms + 1,
                                     records_with_illnesses_that_contain_symptom,
                                     complete_records),
                create_symptoms_tree(symptoms,
                                     index_in_symptoms + 1,
                                     records_with_illnesses_that_do_not_contain_symptom,
                                     complete_records))


def optimal_tree(records, symptoms, depth):
    """
    :param records: a list of records objects
    :param symptoms: a list of symptoms strings
    :param depth: a number representing the depth of a tree
    :return: a decision tree which asks about a depth number of symptoms
    such that its calculated error rate will be the smallest possible given
    the list of symptoms
    """
    smallest_error_rate = None
    smallest_error_rate_tree = None

    for combo in combinations(symptoms, depth):
        combo_symptoms_tree = build_tree(records, combo)
        # tree built from the the combinations of symptoms
        combo_diagnoser = Diagnoser(combo_symptoms_tree)
        # a Diagnoser object built using the combo_symptoms_tree as its root
        error_rate = combo_diagnoser.calculate_error_rate(records)

        if smallest_error_rate is not None:
            if error_rate <= smallest_error_rate:
                smallest_error_rate = error_rate
                smallest_error_rate_tree = combo_symptoms_tree
        else:
            smallest_error_rate = error_rate
            smallest_error_rate_tree = combo_symptoms_tree

    return smallest_error_rate_tree


if __name__ == "__main__":

    # Manually build a simple tree.
    #                cough
    #          Yes /       \ No
    #        fever           healthy
    #   Yes /     \ No
    # influenza   cold

    flu_leaf = Node("influenza", None, None)
    cold_leaf = Node("cold", None, None)
    inner_vertex = Node("fever", flu_leaf, cold_leaf)
    healthy_leaf = Node("healthy", None, cold_leaf)
    root = Node("cough", inner_vertex, healthy_leaf)

    diagnoser = Diagnoser(root)

    # Simple test
    diagnosis = diagnoser.diagnose(["cough"])
    if diagnosis == "cold":
        print("Test passed")
    else:
        print("Test failed. Should have printed cold, printed: ", diagnosis)

        # Add more tests for sections 2-7 here.
