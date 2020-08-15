#############################################################
# FILE : crossword.py
# WRITER 1 : Daniel Magen
# WRITER 2 : yoav cohn,
# EXERCISE : intro2cs ex5 2017-2018
# DESCRIPTION: this module solves 2d crosswords
#############################################################
import sys
import os.path

NUMBER_OF_ARGUMENTS = 4  # the number of arguments we are expecting to use

DIRECTIONS = {'d': (1, 0),
              'u': (-1, 0),
              'r': (0, 1),
              'l': (0, -1),
              'y': (1, 1),
              'x': (-1, -1),
              'w': (-1, 1),
              'z': (1, -1)}
# the dictionary contains as keys the eight directions we can receive
# and their corresponding (delta x, delta y) values
# relative to the normal axis.

MSG_WORD_LIST_FILE_NOT_FOUND = "ERROR: Word file word_list.txt does not exist."
MSG_MATRIX_FILE_FILE_NOT_FOUND = "ERROR: Matrix file mat.txt does not exist."
MSG_DIRECTIONS_INVALID = "ERROR invalid directions"
MSG_INVALID_NUMBER_OF_PARAMETERS = "ERROR: invalid number of parameters. " \
                                   "Please enter word_file matrix_file " \
                                   "output_file directions."


def write_output_dict_to_file(output_dict, file_path):
    """
    :param output_dict: dictionary containing words:number_of_times_found pairs
    :param file_path: a path to a specific file
    saves the output_dict contents into the file_path given
    if the file_path already exists it overwrites it
    :return: None
    """
    sorted_output = output_dict.items()
    sorted_output = sorted(sorted_output, key=lambda tpl: tpl[0])

    with open(file_path, 'w') as output:
        for i in range(len(sorted_output) - 1):
            word, appearances = sorted_output[i]
            output.write(word + "," + str(appearances))
            output.write("\n")

        if len(sorted_output) > 0:
            word, appearances = sorted_output[-1]
            output.write(word + "," + str(appearances))


def load_words(words_file):
    """
    :param words_file: a file path for a file containing the words
    we should search for
    :return: if the file exists returns a list containing those words
    if not it returns None
    """
    if not os.path.exists(words_file):
        return None

    with open(words_file, 'r') as words_from_list:
        words = words_from_list.read().splitlines()

    for i in range(len(words)):
        words[i] = words[i].lower()

    return words


def load_matrix(matrix_file):
    """
    :param matrix_file: a file path for a file containing the matrix
    we should search in
    :return: if the file exists returns the matrix in a list of lists format
    if not it returns None
    """
    if not os.path.exists(matrix_file):
        return None

    matrix_2D = []
    with open(matrix_file, 'r') as words_from_list:
        matrix_2D = words_from_list.read().splitlines()

    for i in range(len(matrix_2D)):
        matrix_2D[i] = matrix_2D[i].lower().split(",")

    return matrix_2D


def load_directions(directions_input_string):
    """
    :param directions_input_string: a string containing
    letters indicating diretions to search the matrix with
    :return: if a direction is not valid, it returns None
    otherwise it returns those directions without doubles
    """
    directions = directions_input_string
    directions = "".join(set(directions))
    for direction in directions:
        if not direction in DIRECTIONS:
            return None

    return directions


def search_for_word(word, matrix, starting_location, directions):
    """
    :param word: the word we are searching for
    :param matrix: the 2d matrix we are searching in
    :param starting_location: a tuple containing 2 numbers
    representing the location in the matrix we should start searching in
    :param directions: a string containing the directions to search in
    :return: the number of times the word appears in the matrix
    when it starts from starting_location in all the directions given
    """

    number_of_times_found = 0

    for dirc in directions:
        delta_x, delta_y = DIRECTIONS[dirc]

        # if the word won't fit in the given direction we wont search for it
        search_up_to_index = (starting_location[0] + (delta_x * (len(word) - 1)),
                              starting_location[1] + (delta_y * (len(word) - 1)))
        # the first letter of the given word is already included
        # we need to search up to len(word)-1

        if search_up_to_index[0] < 0 or search_up_to_index[0] >= len(matrix):
            continue
        if search_up_to_index[1] < 0 or search_up_to_index[1] >= len(matrix[0]):
            continue

        row = starting_location[0] + delta_x
        col = starting_location[1] + delta_y
        word_is_in_matrix = True

        for i in range(1, len(word)):
            if matrix[row][col] != word[i]:
                word_is_in_matrix = False
                break
            row += delta_x
            col += delta_y

        if word_is_in_matrix:
            number_of_times_found += 1

    return number_of_times_found


def search_2D_matrix(matrix_2d, words_list, directions, output_dict):
    """
    :param matrix_2d: the matrix we are searching in
    :param words_list: the words we are searching for
    :param directions: a string containing the directions to search in
    :param output_dict: a dictionary to write to
    the function writes to the output_dict (words:number_of_times_found) pairs
    for each word it finds in the matrix at least once
    :return:None
    """
    for word in words_list:
        times_word_appear = 0

        if len(word) <= len(matrix_2d) or len(word) <= len(matrix_2d[0]):
            # if the word is too big it won't run the searching algorithm
            for i in range(len(matrix_2d)):
                for j in range(len(matrix_2d[i])):
                    if matrix_2d[i][j] == word[0]:
                        times_word_appear += search_for_word(word,
                                                             matrix_2d,
                                                             (i, j),
                                                             directions)

        if times_word_appear != 0:
            output_dict[word] = times_word_appear


if __name__ == "__main__":
    if len(sys.argv) == NUMBER_OF_ARGUMENTS + 1:

        words_list = load_words(sys.argv[1])
        if words_list is None:
            sys.exit(MSG_WORD_LIST_FILE_NOT_FOUND)

        matrix_2d = load_matrix(sys.argv[2])
        if matrix_2d is None:
            sys.exit(MSG_MATRIX_FILE_FILE_NOT_FOUND)

        output_file_location = sys.argv[3]

        directions = load_directions(sys.argv[4])
        if directions is None:
            sys.exit(MSG_DIRECTIONS_INVALID)

        output_dict = {}

        if directions != "" and matrix_2d != []:
            search_2D_matrix(matrix_2d, words_list, directions, output_dict)

        write_output_dict_to_file(output_dict, output_file_location)
    else:
        sys.exit(MSG_INVALID_NUMBER_OF_PARAMETERS)
