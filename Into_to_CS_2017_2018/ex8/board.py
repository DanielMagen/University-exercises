#############################################################
# FILE : board.py
# WRITER : Daniel Magen
# EXERCISE : intro2cs ex8 2017-2018
# DESCRIPTION: this module contains a class representing the game board
# called Board
#############################################################


############################################################
# Imports
############################################################
import game_helper as gh
from car import Car, Direction, Vector


############################################################
# Constants
############################################################


############################################################
# Class definition
############################################################


class Board():
    """
    A class representing a rush hour board.
    """

    EMPTY_SLOT = '_'
    EXIT_SLOT = 'E'
    MESSAGE_CAR_WAS_ADDED = "The car was added successfully"
    MESSAGE_CAR_WAS_NOT_ADDED = "The car was not added to the board"
    MESSAGE_CAR_OUT_OF_BOUNDS = \
        "The car can not be added since its out of bounds"
    MESSAGE_CAR_WILL_OVERLAP = \
        "The car can not be added since it would hit something else on the board"
    MESSAGE_DIRECTION_NOT_VALID = "The direction given does not exist"
    MESSAGE_DIRECTION_IMPOSSIBLE = \
        "The car can not move in the given direction"
    MESSAGE_LOCATION_OCCUPIED = \
        "The car can not move in the given direction since it's already occupied"
    MESSAGE_RED_CAR_CANT_BE_ADDED = "The red car can't be added to the board"

    EXIT_BOARD_DEFAULT_LOCATION = [-1, -3]

    # we were told in the forum that the exit board should be picked by us
    # I wrote my program to fit any kind of exit_board but because of 
    # the forum instruction I set this exit as the deafult one that would
    # override any that is given to it

    def __init__(self, cars, exit_board, size=6):
        """
        Initialize a new Board object.
        :param cars: A list (@or dictionary) of cars. @can be empty
        :param exit_board: a tuple of coordinates of exit point in board
        :param size: Size of board (Default size is 6). 
        """
        self.__matrix = \
            [[Board.EMPTY_SLOT for _ in range(size + 2)] for _ in range(size + 2)]

        self.__exit_board = []
        for i in range(len(Board.EXIT_BOARD_DEFAULT_LOCATION)):
            self.__exit_board.append(Board.EXIT_BOARD_DEFAULT_LOCATION[i] \
                                     + len(self.__matrix))
        self.write_to_location(self.__exit_board, Board.EXIT_SLOT)

        self.write_indecies_onto_board()

        self.__cars = {}

        if type(cars) is dict:
            self.add_dict_of_cars(cars)
        elif type(cars) is list or type(cars) is tuple:
            self.add_list_of_cars(cars)

    def write_indecies_onto_board(self):
        """
        this method simply writes all the indecies to the edges of the board
        """
        for i in range(len(self.__matrix) - 1):
            location = (i, 0)
            if self.is_empty(location):
                self.write_to_location(location, str(i))

        for i in range(1, len(self.__matrix[0])):
            location = (len(self.__matrix) - 1, i)
            if self.is_empty(location):
                self.write_to_location(location, str(i - 1))

    def add_dict_of_cars(self, cars):
        """
        if given a dict adds the items in the given dict as cars to the board
        """
        for car in cars.items():
            self.add_car(car)

    def add_list_of_cars(self, cars):
        """
        if given a list adds the items in the given dict as cars to the board
        """
        for car in cars:
            self.add_car(car)

    def get_size(self):
        """
        returns the size of the matrix
        """
        return len(self.__matrix)

    def get_car_by_color(self, color):
        """
        gets a color
        if the board has a car with the given color it returns it
        otherwise it returns False
        """
        if color not in self.__cars:
            return False

        return self.__cars[color]

    def get_colors_of_cars_on_board(self):
        """
        returns a list of all the colors of all the cars on the board
        """
        return list(self.__cars.keys())

    def add_car(self, car):
        """
        Add a single car to the board.
        :param car: A car object
        :return: True if a car was successfully added, or False otherwise.
        """
        car_location_vector = car.get_location()
        car_length = car.get_length()

        orientation_vector = car.get_orientation_vector()

        if not self.range_of_locations_are_free(car_location_vector,
                                                orientation_vector,
                                                car_length):
            print(Board.MESSAGE_CAR_WAS_NOT_ADDED)
            return False

        car_color = car.get_color()
        if self.write_to_range_of_locations(car_location_vector,
                                            orientation_vector,
                                            car_length,
                                            car_color,
                                            check_in_bounds=False):
            self.__cars[car_color] = car
            print(Board.MESSAGE_CAR_WAS_ADDED)
            return True

        return False

    def write_to_range_of_locations(self,
                                    start_vector,
                                    orntion_vector,
                                    length,
                                    letter,
                                    check_in_bounds=True):
        """
        gets 
        a vector representing the starting location of some range
        a vector representing the orientation_vector that the range will follow
        a number representing the length of the range
        a letter to write to the board in the corresponding range
        optional check_in_bounds=True checks if the range is in the bounds 
        of the board
        
        if check_in_bounds=True and the range is out of bounds it returns False
        
        otherwise it writes the given letter to the board 
        in the corresponding range and returns True
        """
        if check_in_bounds:
            if not self.check_range_of_locations_are_in_bounds(start_vector,
                                                               orntion_vector,
                                                               length):
                return False

        new_start_vector = start_vector.get_copy()
        self.write_to_location(new_start_vector.get_coordinates(), letter)

        for _ in range(length - 1):
            new_start_vector += orntion_vector
            self.write_to_location(new_start_vector.get_coordinates(), letter)

        return True

    def write_to_location(self, location, letter):
        """
        gets
        a tuple representing the location in the board
        a letter to write to the board in the given location
        
        writes the given letter to the board
        """
        self.__matrix[location[0]][location[1]] = letter

    def range_of_locations_are_free(self,
                                    start_vector,
                                    orientation_vector,
                                    length):
        """
        gets
        a vector representing the starting location of some range
        a vector representing the orientation_vector that the range will follow
        a number representing the length of the range
        
        returns true if all the slots that are 
        in the corresponding range are empty
        if the range is not empty it returns false
        """
        if not self.check_range_of_locations_are_in_bounds(start_vector,
                                                           orientation_vector,
                                                           length):
            print(Board.MESSAGE_CAR_OUT_OF_BOUNDS)
            return False

        new_start_vector = start_vector.get_copy()

        if not self.is_empty(new_start_vector.get_coordinates()):
            print(Board.MESSAGE_CAR_WILL_OVERLAP)
            return False

        for _ in range(length - 1):
            new_start_vector += orientation_vector

            if not self.is_empty(new_start_vector.get_coordinates()):
                print(Board.MESSAGE_CAR_WILL_OVERLAP)
                return False

        return True

    def check_range_of_locations_are_in_bounds(self,
                                               start_vector,
                                               orientation_vector,
                                               length):
        """
        gets
        a vector representing the starting location of some range
        a vector representing the orientation_vector that the range will follow
        a number representing the length of the range
        
        
        returns true if all the slots that are 
        in the corresponding range are in bounds
        
        if the range is not in bounds it returns false
        """
        if not self.check_vector_in_bounds(start_vector):
            return False

        end = start_vector + (orientation_vector * length)

        if not self.check_vector_in_bounds(end):
            return False

        return True

    def check_vector_in_bounds(self, location_vector):
        """
        gets a vector 
        returns true if its coordinates is in the board bounds
        """
        return location_vector.in_range(0, len(self.__matrix))

    def check_tuple_in_bounds(self, location):
        """
        gets a tuple 
        returns true if the coordinates it corresponds to
        are in the board bounds
        """
        for coor in location:
            if coor not in range(0, len(self.__matrix)):
                return False

        return True

    def is_empty(self, location):
        """
        Check if a given location on the board is free.
        :param location: x and y coordinations of location to be check
        :return: True if location is free, False otherwise
        """
        if not self.check_tuple_in_bounds(location):
            return False

        if self.__matrix[location[0]][location[1]] == Board.EMPTY_SLOT:
            return True

        return False

    def check_of_move_legal(self, car, direction):
        """
        gets a car object and a direction
        returns True if the car can move in the given direction knowing its
        orientation and not taking into care the board bounds
        and False otherwise
        """

        if direction not in Direction.get_all_directions():
            print(Board.MESSAGE_DIRECTION_NOT_VALID)
            return False

        if not car.can_move_in_direction(direction):
            print(Board.MESSAGE_DIRECTION_IMPOSSIBLE)
            return False

        return True

    def move(self, car, direction):  ## check that car is in the board?
        """
        Move a car in the given direction.
        :param car: A Car object to be moved.
        :param direction: A Direction object representing desired direction
            to move car.
        :return: True if movement was possible and car was moved, False otherwise.
        """
        if not self.check_of_move_legal(car, direction):
            return False

        location_is_empty = False

        direction_vector = car.get_orientation_vector(direction)
        direction_is_positive = direction_vector.is_positive()

        old_start = car.get_location()
        old_end = car.get_end()

        new_start = old_start + direction_vector
        new_end = old_end + direction_vector

        if direction_is_positive:
            location_is_empty = self.is_empty(new_end.get_coordinates())

        else:
            location_is_empty = self.is_empty(new_start.get_coordinates())

        if not location_is_empty:
            print(Board.MESSAGE_LOCATION_OCCUPIED)
            return False

        car_color = car.get_color()

        car.update_location(new_start.get_coordinates())

        if direction_is_positive:
            self.delete_location(old_start.get_coordinates())
            self.write_to_location(new_end.get_coordinates(), car_color)
        else:
            self.delete_location(old_end.get_coordinates())
            self.write_to_location(new_start.get_coordinates(), car_color)

        return True

    def delete_location(self, location):
        """
        inserts an empty slot in the given location
        """
        self.write_to_location(location, Board.EMPTY_SLOT)

    def get_preferable_orientation_for_red_car(self):
        """
        returns the orientation that will give the red car the most space
        """
        horizontal_space = abs(len(self.__matrix[0]) - self.__exit_board[1])
        vertical_space = abs(len(self.__matrix) - self.__exit_board[0])

        horizontal_space = max(horizontal_space, self.__exit_board[1])
        vertical_space = max(vertical_space, self.__exit_board[0])
        # the space the red car will have in the in either orientation

        if horizontal_space >= vertical_space:
            return Direction.get_horizontal_constant()

        return Direction.get_vertical_constant()

    def get_red_car_location_orientation_and_deviation(self, length_of_car):
        """
        receives the requested size of the red car
        
        returns 
        a tuple representing the minimal starting location of the red car
        
        an orientation either vertical or horizontal as given by the 
        Direction class
        
        and a maximum deviation from the range in the positive direction along 
        the orientation returned
        
        if the given car size won't fit in the board it returns False
        """
        orientation_for_red_car = self.get_preferable_orientation_for_red_car()

        orientation_vector = \
            Direction.orientation_to_orientation_vector(orientation_for_red_car)

        opposite_orientation = \
            Direction.get_opposite_orientation(orientation_for_red_car)

        opposite_orientation_vector = \
            Direction.orientation_to_orientation_vector(opposite_orientation)

        exit_board_vector = Vector(self.__exit_board)

        minimal_starting_location_vector = \
            opposite_orientation_vector * exit_board_vector
        # will hold the starting location of the red car

        if minimal_starting_location_vector == exit_board_vector:
            # the starting location of the red car is on the exit slot
            # move it to the other side
            minimal_starting_location_vector += \
                orientation_vector * (len(self.__matrix) - 1)

        if not self.check_range_of_locations_are_in_bounds(
                minimal_starting_location_vector,
                orientation_vector,
                length_of_car):
            # if the red car won't fit in the board it returns False
            return False

        maximum_deviation = len(self.__matrix) - 1 - length_of_car

        # checking that the minimal_starting_location is not on an index of the
        # board
        minimal_starting_location_is_empty = \
            self.is_empty(minimal_starting_location_vector.get_coordinates())

        while not minimal_starting_location_is_empty:
            minimal_starting_location_vector += orientation_vector

            if not \
                    self.check_vector_in_bounds(minimal_starting_location_vector):
                break

            if \
                    self.is_empty(minimal_starting_location_vector.get_coordinates()):
                minimal_starting_location_is_empty = True

        if not minimal_starting_location_is_empty:
            # if the red car won't fit in the board it returns False
            print(Board.MESSAGE_RED_CAR_CANT_BE_ADDED)
            return False

        minimal_starting_location = \
            minimal_starting_location_vector.get_coordinates()
        # changes the vector into a simple coordinates tuple

        return (minimal_starting_location,
                orientation_for_red_car,
                maximum_deviation)

    def min_distance_between_car_exit(self, color):
        """
        returns the minimum distance that is needed to travel to get 
        from the exit of the board to the given car
        
        if there does not exist a car with the given color on the board
        it returns False
        """

        if color not in self.__cars:
            return False

        car = self.__cars[color]
        start = car.get_location()
        end = car.get_end()

        exit_board_vector = Vector(self.__exit_board)

        distance_from_start = start.taxicab_distance(exit_board_vector)
        distance_from_end = end.taxicab_distance(exit_board_vector)

        return min(distance_from_start, distance_from_end)

    def __repr__(self):
        """
        :return: Return a string representation of the board.
        """
        string_form = ""
        for row in self.__matrix:
            string_form += str(row) + '\n'

        return string_form
