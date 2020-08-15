#############################################################
# FILE : crossword.py
# WRITER 1 : Daniel Magen
# WRITER 2 : yoav cohn,
# EXERCISE : intro2cs ex5 2017-2018
# DESCRIPTION: this module solves 3d crosswords and contains the bonus answer
#############################################################
import sys
import os.path

NUMBER_OF_ARGUMENTS = 4  # the number of arguments we are expecting to use

# those dictionaries contains the eight directions to search for in each
# configuration and their corresponding (delta x, delta y, delta z) values
# relative to the normal axis.
A_DIRECTIONS = {'d': (0, 1, 0),
                'u': (0, -1, 0),
                'r': (0, 0, 1),
                'l': (0, 0, -1),
                'y': (0, 1, 1),
                'x': (0, -1, -1),
                'w': (0, -1, 1),
                'z': (0, 1, -1)}

B_DIRECTIONS = {'d': (1, 0, 0),
                'u': (-1, 0, 0),
                'r': (0, 0, 1),
                'l': (0, 0, -1),
                'y': (1, 0, 1),
                'x': (-1, 0, -1),
                'w': (-1, 0, 1),
                'z': (1, 0, -1)}

C_DIRECTIONS = {'d': (0, 1, 0),
                'u': (0, -1, 0),
                'r': (1, 0, 0),
                'l': (-1, 0, 0),
                'y': (1, 1, 0),
                'x': (-1, -1, 0),
                'w': (1, -1, 0),
                'z': (-1, 1, 0)}

N_DIRECTIONS = {'diagonal1': (1, 1, 1),
                'diagonal1_opposite': (-1, -1, -1),
                'diagonal2': (-1, 1, 1),
                'diagonal2_opposite': (1, -1, -1),
                'diagonal3': (-1, -1, 1),
                'diagonal3_opposite': (1, 1, -1),
                'diagonal4': (1, -1, 1),
                'diagonal4_opposite': (-1, 1, -1)}

DIRECTIONS = {"a": A_DIRECTIONS,
              "b": B_DIRECTIONS,
              "c": C_DIRECTIONS,
              "n": N_DIRECTIONS}

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
    :param words_file: a file path for a file
    containing the words we should search for
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
    :param matrix_file: a file path for a file containing
    the matrix we should search in
    :return: if the file exists returns the matrix in a list of lists format
    if not it returns None
    """
    if not os.path.exists(matrix_file):
        return None

    with open(matrix_file, 'r') as words_from_list:
        matrix_3D = words_from_list.read().splitlines()

    for i in range(len(matrix_3D)):
        matrix_3D[i] = matrix_3D[i].lower().split(",")

    matrix_2d = []
    i = 0
    while i < len(matrix_3D):
        if matrix_3D[i] == ['***']:
            matrix_3D[i] = matrix_2d
            matrix_2d = []
            i += 1
        else:
            matrix_2d.append(matrix_3D[i])
            del matrix_3D[i]
    matrix_3D.append(matrix_2d)

    return matrix_3D


def load_directions(directions_input_string):
    """
    :param directions_input_string: a string containing letters
    indicating diretions to search the matrix with
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
    :param matrix: the 3d matrix we are searching in
    :param starting_location: a tuple containing 3 numbers representing the
    location in the matrix we should start searching in
    :param directions: a string containing the directions to search in
    :return: the number of times the word appears in the matrix
    when it starts from starting_location in all the directions given
    """

    number_of_times_found = 0

    for dirc_dict in directions:
        for dirc in DIRECTIONS[dirc_dict]:
            delta_x, delta_y, delta_z = DIRECTIONS[dirc_dict][dirc]

            # if the word won't fit in the given direction
            # we wont search for it there
            search_up_to_index = (
                starting_location[0] + (delta_x * (len(word) - 1)),
                starting_location[1] + (delta_y * (len(word) - 1)),
                starting_location[2] + (delta_z * (len(word) - 1)))
            # the first letter of the given word is already included
            # we need to search up to len(word)-1

            if search_up_to_index[0] < 0 or search_up_to_index[0] >= len(
                    matrix):
                continue
            if search_up_to_index[1] < 0 or search_up_to_index[1] >= len(
                    matrix[0]):
                continue
            if search_up_to_index[2] < 0 or search_up_to_index[2] >= len(
                    matrix[0][0]):
                continue

            row = starting_location[0] + delta_x
            col = starting_location[1] + delta_y
            depth = starting_location[2] + delta_z
            word_is_in_matrix = True

            for i in range(1, len(word)):
                if matrix[row][col][depth] != word[i]:
                    word_is_in_matrix = False
                    break
                row += delta_x
                col += delta_y
                depth += delta_z

            if word_is_in_matrix:
                number_of_times_found += 1

    return number_of_times_found


def search_3D_matrix(matrix_3d, words_list, directions, output_dict):
    """
    :param matrix_3d: the matrix we are searching in
    :param words_list: the words we are searching for
    :param directions: a string containing the directions to search in
    :param output_dict: a dictionary to write to
    the function writes to the output_dict the
    (words:number_of_times_found) pairs for each word
    it finds in the matrix at least once
    :return:None
    """
    for word in words_list:
        times_word_appear = 0

        if len(word) <= len(matrix_3d) or len(word) <= len(
                matrix_3d[0]) or len(word) <= len(matrix_3d[0][0]):
            # if the word is too big it won't run the searching algorithm
            for i in range(len(matrix_3d)):
                for j in range(len(matrix_3d[i])):
                    for k in range(len(matrix_3d[i][j])):
                        if matrix_3d[i][j][k] == word[0]:
                            times_word_appear += search_for_word(word,
                                                                 matrix_3d,
                                                                 (i, j, k),
                                                                 directions)

        if times_word_appear != 0:
            output_dict[word] = times_word_appear


if __name__ == "__main__":

    if len(sys.argv) == NUMBER_OF_ARGUMENTS + 1:

        words_list = load_words(sys.argv[1])
        if words_list is None:
            sys.exit(MSG_WORD_LIST_FILE_NOT_FOUND)

        matrix_3d = load_matrix(sys.argv[2])
        if matrix_3d is None:
            sys.exit(MSG_MATRIX_FILE_FILE_NOT_FOUND)

        output_file_location = sys.argv[3]

        directions = load_directions(sys.argv[4])
        if directions is None:
            sys.exit(MSG_DIRECTIONS_INVALID)

        output_dict = {}

        if directions != "" and matrix_3d != []:
            search_3D_matrix(matrix_3d, words_list, directions, output_dict)

        write_output_dict_to_file(output_dict, output_file_location)
    else:
        sys.exit(MSG_INVALID_NUMBER_OF_PARAMETERS)
