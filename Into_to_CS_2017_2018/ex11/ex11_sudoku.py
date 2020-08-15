#############################################################
# FILE : ex11.py
# WRITER : Daniel Magen
# EXERCISE : intro2cs ex11 2017-2018
# DESCRIPTION: this module contains methods used to load and solve
# a sudoku puzzle
#############################################################
from ex11_backtrack import general_backtracking

EMPTY_CELL = 0
SUDOKU_SIZE = 9
ROW_INDEX = 0
COL_INDEX = 1
LEGAL_ASSIGNMENTS = range(1, 10)


def print_board(board, board_size=9):
    """ prints a sudoku board to the screen

    ---  board should be implemented as a dictinary 
         that points from a location to a number {(row,col):num}
    """
    for row in range(board_size):
        if (row % 3 == 0):
            print('-------------')
        toPrint = ''
        for col in range(board_size):
            if (col % 3 == 0):
                toPrint += '|'
            toPrint += str(board[(row, col)])
        toPrint += '|'
        print(toPrint)
    print('-------------')


def load_game(sudoku_file):
    """
    :param sudoku_file: a location for a sudoku file
    :return: a dict of tuples of coordinates as keys and numbers from 0-9
    as values
    """
    sudoku_list = []
    sudoku_dict = {}
    with open(sudoku_file, 'r') as sudoku:
        for line in sudoku.read().splitlines():
            sudoku_list += line.split(',')

    map(lambda s: int(s), sudoku_list)

    for i in range(len(sudoku_list)):
        location = (i // SUDOKU_SIZE, i % SUDOKU_SIZE)
        sudoku_dict[location] = int(sudoku_list[i])

    return sudoku_dict


def check_board(board, x, *args):
    """
    :param board: a dict of tuples of coordinates as keys and numbers from 0-9
    as values
    :param x: a tuple coordinate
    :param args: not used in my implementation
    :return: True if the placement in board[x] is legal
    False otherwise
    """
    if board[x] == EMPTY_CELL:
        return True
    to_check = get_same_row_col_and_square_coordinates(x)
    to_check = list(map(lambda i: board[i], to_check))
    to_check = remove_duplicates_in_list(to_check)
    return not board[x] in to_check


def get_same_row_col_and_square_coordinates(coordinate_tuple):
    """
    :param coordinate_tuple: a coordinate tuple
    :return: a list of all coordinate tuples that are in the same row or
    col or square
    as the given coordinate_tuple except the given coordinate_tuple itself
    """
    coordinates = get_same_axis_coordinates_list(coordinate_tuple, ROW_INDEX) \
                  + get_same_axis_coordinates_list(coordinate_tuple, COL_INDEX) \
                  + get_same_square_coordinates_list(coordinate_tuple)

    return remove_duplicates_in_list(coordinates)


def get_same_axis_coordinates_list(coordinate_tuple, index_to_change):
    """
    :param coordinate_tuple:  a coordinate tuple
    :param index_to_change: the index that should change
    :return: a list of all coordinate tuples that are the same in all places
    except the given index in the
    as the given coordinate_tuple except the given coordinate_tuple
    """
    coordinate_list = list(coordinate_tuple)
    same_axis_coordinates_list = []
    for i in range(0, SUDOKU_SIZE):
        if i != coordinate_tuple[index_to_change]:
            coordinate_list[index_to_change] = i
            same_axis_coordinates_list.append(tuple(coordinate_list))
    return same_axis_coordinates_list


def get_same_square_coordinates_list(coordinate_tuple):
    square_size = int(SUDOKU_SIZE ** 0.5)

    square_start_row = round_down_to_nearest_multiple(coordinate_tuple[ROW_INDEX],
                                                      square_size)
    square_start_col = round_down_to_nearest_multiple(coordinate_tuple[COL_INDEX],
                                                      square_size)

    same_square_coordinates_list = []
    for i in range(square_size):
        for j in range(square_size):
            new_coor = (square_start_row + i, square_start_col + j)
            if new_coor != coordinate_tuple:
                same_square_coordinates_list.append(new_coor)

    return same_square_coordinates_list


def round_down_to_nearest_multiple(number, mod_num):
    """
    :param number: the number to round down
    :param mod_num: the number rounded down to will be a multiple of
    that integer
    :return: the nearest smallest integer to number
    that is divisible by mod_num
    """
    return (number // mod_num) * mod_num


def remove_duplicates_in_list(list_of_items):
    """
    :param list_of_items: a list of items
    :return: a list of the unique items in the list
    """
    return list(set(list_of_items))


def get_empty_cells_in_sudoku(board):
    """
    :param board: a dict of tuples of coordinates as keys and numbers from 0-9
    as values
    :return: a list of coordinates of empty_cells in the board
    """
    empty_cells = []
    for coordinate in board:
        if board[coordinate] == EMPTY_CELL:
            empty_cells.append(coordinate)
    return empty_cells


def run_game(sudoku_file, print_mode=False):
    """
    :param sudoku_file: a location for a sudoku file
    :param print_mode: a boolean indicating to print the solution or not
    :return: True if a solution exists False otherwise
    """
    board = load_game(sudoku_file)
    empty_cells = get_empty_cells_in_sudoku(board)
    solution_exits = general_backtracking(empty_cells,
                                          board,
                                          0,
                                          LEGAL_ASSIGNMENTS,
                                          check_board)
    if print_mode:
        if solution_exits:
            print_board(board)

    return solution_exits
