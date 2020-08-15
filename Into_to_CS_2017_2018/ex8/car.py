#############################################################
# FILE : car.py
# WRITER : Daniel Magen
# EXERCISE : intro2cs ex8 2017-2018
# DESCRIPTION: this module contain 3 classes
# Vector - a class representing a vector
# Direction - a static class in charge of handling directions constants and 
# methods
# Car - a class representing a car on the board
#############################################################

############################################################
# Helper class
############################################################


class Vector:
    def __init__(self, cooridinate_tuple):
        self.__cooridinates = tuple(cooridinate_tuple)

    def get_coordinates(self):
        """
        returns the coordinates of the vector
        """
        return self.__cooridinates

    def get_copy(self):
        """
        returns a new Vector object with the same properties
        """
        return Vector(self.__cooridinates)

    def is_positive(self):
        """
        returns true if all the the Vector coordinates are positive
        false otherwise
        """
        for coor in self.__cooridinates:
            if coor < 0:
                return False
        return True

    def __mul__(self, multiply_by):
        """
        if the Vector is multiplied by an object that is not a Vector 
        it returns a new Vector with all of its coordinates 
        multiplied by that object
        
        if the Vector is multiplied by a another Vector 
        it returns a new Vector object that has the same coordinates length
        as the smallest one from the 2, where all of its coordinates
        is the result of multiplying the corresponding coordinates in the 
        2 Vectors
        """
        result = []

        if type(multiply_by) == type(self):
            other_vcr_cooridinates = multiply_by.get_coordinates()

            for i in range(min(len(self.__cooridinates),
                               len(other_vcr_cooridinates))):
                result.append(other_vcr_cooridinates[i] * self.__cooridinates[i])

        else:
            for i in range(len(self.__cooridinates)):
                result.append(self.__cooridinates[i] * multiply_by)

        return Vector(tuple(result))

    def __add__(self, add_to):
        """
        if the Vector is added to an object that is not a Vector 
        it returns a new Vector with all of its coordinates added to the object
        
        if the Vector is added to a another Vector 
        it returns a new Vector object that has the same coordinates length
        as the smallest one from the 2, where all of its coordinates
        is the result of adding the corresponding coordinates in the 
        2 Vectors
        """
        result = []

        if type(add_to) == type(self):
            other_vcr_cooridinates = add_to.get_coordinates()

            for i in range(min(len(self.__cooridinates),
                               len(other_vcr_cooridinates))):
                result.append(other_vcr_cooridinates[i] + self.__cooridinates[i])

        else:
            for i in range(len(self.__cooridinates)):
                result.append(self.__cooridinates[i] + add_to)

        return Vector(tuple(result))

    def __eq__(self, vector2):
        """
        returns true if the other object it is being compared to is another
        Vector with the exact same coordinates
        """
        if type(vector2) != type(self):
            return False

        other_vector_cooridinates = vector2.get_coordinates()
        if len(self.__cooridinates) != len(other_vector_cooridinates):
            return False

        for i in range(len(self.__cooridinates)):
            if self.__cooridinates[i] != other_vector_cooridinates[i]:
                return False

        return True

    def in_range(self, smallest, largest):
        """
        checks if all the coordinates in the vector 
        are equal or larger than "smallest"
        and smaller than largest
        """
        for coor in self.__cooridinates:
            if coor not in range(smallest, largest):
                return False
        return True

    def taxicab_distance(self, vector2):
        """
        goes over all the the numbers that are in the same index in the 
        given Vector coordinates and calculates the difference between them 
        returns the sum of the difference
        
        if one of the vectors has a coordinates list longer than the other
        the difference is set to be the abs of the numbers in the longer 
        coordinates list that has no corresponding number 
        in the other vector coordinates
        
        it the given object is not a Vector it returns false
        """
        if type(vector2) != type(self):
            return False

        other_vector_cooridinates = vector2.get_coordinates()
        diff = 0

        min_length = len(self.__cooridinates)
        max_length = len(other_vector_cooridinates)
        max_vector_cooridinates = other_vector_cooridinates

        if len(other_vector_cooridinates) < len(self.__cooridinates):
            min_length = len(other_vector_cooridinates)
            max_length = len(self.__cooridinates)
            max_vector_cooridinates = self.__cooridinates

        for i in range(min_length):
            diff += abs(other_vector_cooridinates[i] - self.__cooridinates[i])

        for i in range(min_length, max_length):
            diff += abs(max_vector_cooridinates[i])

        return diff


class Direction:
    """
    Class representing a direction in 2D world.
    You may not change the name of any of the constants (UP, DOWN, LEFT, RIGHT,
     NOT_MOVING, VERTICAL, HORIZONTAL, ALL_DIRECTIONS), but all other
     implementations are for you to carry out.
    """
    UP = 8
    DOWN = 2
    LEFT = 4
    RIGHT = 6

    NOT_MOVING = 5

    VERTICAL = 0
    HORIZONTAL = 1

    ALL_DIRECTIONS = (UP, DOWN, LEFT, RIGHT)

    VERTICAL_DIRECTIONS = (UP, DOWN)
    HORIZONTAL_DIRECTIONS = (LEFT, RIGHT)

    POSITIVE_DIRECTIONS = (DOWN, RIGHT)
    NEGATIVE_DIRECTIONS = (UP, LEFT)

    # the direction vectors for the possible car orientations
    VERTICAL_DIRECTION_VECTOR = Vector([1, 0])
    HORIZONTAL_DIRECTION_VECTOR = Vector([0, 1])

    NEGATIVE_VERTICAL_DIRECTION_VECTOR = VERTICAL_DIRECTION_VECTOR * -1
    NEGATIVE_HORIZONTAL_DIRECTION_VECTOR = HORIZONTAL_DIRECTION_VECTOR * -1

    @staticmethod
    def get_all_directions():
        """
        returns a tuple containing all the directions possible
        """
        return Direction.ALL_DIRECTIONS

    @staticmethod
    def get_not_moving_constant():
        """
        returns the constant set for not moving
        """
        return Direction.NOT_MOVING

    @staticmethod
    def get_vertical_constant():
        """
        returns the constant set for vertical motion
        """
        return Direction.VERTICAL

    @staticmethod
    def get_horizontal_constant():
        """
        returns the constant set for horizontal motion
        """
        return Direction.HORIZONTAL

    @staticmethod
    def get_vertical_direction_vector():
        """
        returns the constant Vector set for vertical motion
        """
        return Direction.VERTICAL_DIRECTION_VECTOR

    @staticmethod
    def get_horizontal_direction_vector():
        """
        returns the constant Vector set for horizontal motion
        """
        return Direction.HORIZONTAL_DIRECTION_VECTOR

    @staticmethod
    def get_opposite_orientation(orientation):
        """
        if given the constant set for horizontal motion
        it returns the constant set for vertical motion
        
        if given the constant set for vertical motion
        it returns the constant set for horizontal motion
        """
        if orientation == Direction.VERTICAL:
            return Direction.HORIZONTAL

        if orientation == Direction.HORIZONTAL:
            return Direction.VERTICAL

    @staticmethod
    def orientation_to_orientation_vector(orientation):
        """
        if given the constant set for horizontal motion
        it returns the constant Vector set for horizontal motion
        
        if given the constant set for vertical motion
        it returns the constant Vector set for vertical motion
        """
        if orientation == Direction.VERTICAL:
            return Direction.VERTICAL_DIRECTION_VECTOR

        if orientation == Direction.HORIZONTAL:
            return Direction.HORIZONTAL_DIRECTION_VECTOR

    @staticmethod
    def orientation_to_direction_list(orientation):
        """
        if given the constant set for horizontal motion
        it returns a tuple containing all the possible horizontal motions
        
        if given the constant set for vertical motion
        it returns a tuple containing all the possible vertical motions
        """
        if orientation == Direction.VERTICAL:
            return Direction.VERTICAL_DIRECTIONS

        elif orientation == Direction.HORIZONTAL:
            return Direction.HORIZONTAL_DIRECTIONS

    @staticmethod
    def get_orientation_vector_of_direction(direction):
        """
        is given a direction 
        if the direction corresponds to a direction in the possible directions
        constant, it returns a Vector that corresponds to that direction
        """
        if direction in Direction.POSITIVE_DIRECTIONS:

            if direction in Direction.VERTICAL_DIRECTIONS:
                return Direction.VERTICAL_DIRECTION_VECTOR
            else:
                return Direction.HORIZONTAL_DIRECTION_VECTOR

        if direction in Direction.VERTICAL_DIRECTIONS:
            return Direction.NEGATIVE_VERTICAL_DIRECTION_VECTOR
        else:
            return Direction.NEGATIVE_HORIZONTAL_DIRECTION_VECTOR

    @staticmethod
    def direction_and_orientation_match(drctn, orientation):
        """
        checks if the given direction is a valid direction 
        in the given orientation
        """
        return drctn in Direction.orientation_to_direction_list(orientation)


############################################################
# Class definition
############################################################


class Car:
    """
    A class representing a car in rush hour game.
    A car is 1-dimensional object that could be laid in either horizontal or
    vertical alignment. A car drives on its vertical\horizontal axis back and
    forth until reaching the board's boarders. A car can only drive to an empty
    slot (it can't override another car).
    """

    def __init__(self, color, length, location, orientation):
        """
        A constructor for a Car object
        :param color: A string representing the car's color
        :param length: An int in the range of (2,4) representing the car's length.
        :param location: A list representing the car's head (x, y) location
        :param orientation: An int representing the car's orientation
        """
        self.__color = color
        self.__length = length
        self.__location = Vector(location)
        self.__orientation = orientation

    def is_horizontal(self):
        """
        returns true if the car is horizontal and false if it's vertical
        """
        if self.__orientation == Direction.get_horizontal_constant():
            return True

        elif self.__orientation == Direction.get_vertical_constant():
            return False

    def get_orientation_vector(self, direction=None):
        """
        if this function receives no input it returns the orientation_vector
        corresponding to the car orientation
        
        if it does it should receive a valid direction from the Direction
        Class, it returns the orientation_vector corresponding to that 
        direction
        """
        if direction == None:
            if self.is_horizontal():
                return Direction.get_horizontal_direction_vector()

            return Direction.get_vertical_direction_vector()

        return Direction.get_orientation_vector_of_direction(direction)

    def get_location(self):
        """
        returns a copy of the Vector object containing the car location
        """
        return self.__location.get_copy()

    def get_end(self):
        """
        returns a Vector object containing the car end location
        """
        orientation_vector = self.get_orientation_vector()
        end = self.__location + (orientation_vector * (self.__length - 1))

        return end

    def get_length(self):
        """
        returns the car length
        """
        return self.__length

    def get_color(self):
        """
        returns the car color
        """
        return self.__color

    def update_location(self, location):
        """
        is given a tuple containing a new location
        updates the car location to a new Vector with the given coordinates
        """
        self.__location = Vector(location)

    def can_move_in_direction(self, direction):
        """
        checks if the car can move in the given direction
        if it can it returns True
        and False otherwise
        """
        if direction == Direction.get_not_moving_constant():
            return True

        return Direction.direction_and_orientation_match(
            direction, self.__orientation)
