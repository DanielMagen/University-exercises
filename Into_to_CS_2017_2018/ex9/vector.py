#############################################################
# FILE : vector.py
# WRITER 1 : Daniel Magen ,login user -
# WRITER 2 : Omer Liberman,, login user -
# EXERCISE : EX 9
# DESCRIPTION: In this file we implemented the class Vector
#############################################################

from __future__ import division
import math


class Vector:
    X_AXIS = 1
    ROUND_AFTER_ROTATE_BY = 3

    def __init__(self, *args):
        self.__coordinates = tuple(args)

    def get_coordinates(self):
        """
        returns the coordinates of the vector
        """
        return self.__coordinates

    def get_angle(self):
        """
        :return: the angle of the vector with the x axis in radians
        """
        return self.calculate_angle_with_nth_axis(Vector.X_AXIS)

    def get_copy(self):
        """
        returns a new Vector object with the same properties
        """
        return Vector(*self.__coordinates)

    def is_positive(self):
        """
        returns true if all the the Vector coordinates are positive
        false otherwise
        """
        for coor in self.__coordinates:
            if coor < 0:
                return False
        return True

    def _apply_action(self, second_arg, function):
        """
        apply the given function on the vector and second_arg in that order
        
        if the vector2 is not a Vector
        it returns a new Vector such that its coordinates are the result of
        function(self.__coordinates[i],second_arg)

        if the second_arg is a Vector
        it returns a new Vector object that has the same coordinates length
        as the smallest one from the 2, where all of its coordinates
        is the result of 
        function(self.__coordinates[i],second_arg.coordinates[i])
        """
        result = []

        if type(second_arg) == type(self):
            other_vcr_cooridinates = second_arg.get_coordinates()

            for i in range(min(len(self.__coordinates),
                               len(other_vcr_cooridinates))):
                result.append(function(self.__coordinates[i],
                                       other_vcr_cooridinates[i]))

        else:
            for i in range(len(self.__coordinates)):
                result.append(function(self.__coordinates[i], second_arg))

        return Vector(*result)

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
        mul_func = lambda a, b: a * b
        return self._apply_action(multiply_by, mul_func)

    def __truediv__(self, divide_by):
        """
        if the Vector is divided by an object that is not a Vector
        it returns a new Vector with all of its coordinates divided 
        by that object
        
        if the Vector is divided by another Vector
        it returns a new Vector object that has the same coordinates length
        as the smallest one from the 2, where all of its coordinates
        is the result of divided the corresponding coordinates in
        the vector by those in the second vector
        """
        div_func = lambda a, b: a / b
        return self._apply_action(divide_by, div_func)

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
        add_func = lambda a, b: a + b
        return self._apply_action(add_to, add_func)

    def __sub__(self, subtract_from_self):
        """
        if the Vector is lessened by an object that is not a Vector
        it returns a new Vector with all of its coordinates lessened 
        by that object
        
        if the Vector is lessened by another Vector
        it returns a new Vector object that has the same coordinates length
        as the smallest one from the 2, where all of its coordinates
        is the result of subtracting the corresponding coordinates in
        the vector from those in the second vector
        """
        sub_func = lambda a, b: a - b
        return self._apply_action(subtract_from_self, sub_func)

    def __mod__(self, mod_by):
        """
        if the Vector is modded by an object that is not a Vector
        it returns a new Vector with all of its coordinates modded
        by that object

        if the Vector is modded by another Vector
        it returns a new Vector object that has the same coordinates length
        as the smallest one from the 2, where all of its coordinates
        is the result of moding the corresponding coordinates in
        the vector using those in the second vector
        """
        mod_func = lambda a, b: a % b
        return self._apply_action(mod_by, mod_func)

    def __eq__(self, vector2):
        """
        returns true if the other object it is being compared to is another
        Vector with the exact same coordinates
        """
        if type(vector2) != type(self):
            return False

        other_vector_cooridinates = vector2.get_coordinates()
        if len(self.__coordinates) != len(other_vector_cooridinates):
            return False

        for i in range(len(self.__coordinates)):
            if self.__coordinates[i] != other_vector_cooridinates[i]:
                return False

        return True

    def __abs__(self):
        """
        :return:  returns the sum of all the coordinates squared
        """
        sum = 0
        for num in self.__coordinates:
            sum += num ** 2

        return math.sqrt(sum)

    def sum_of_coordinates(self):
        """
        :return: the sum of the vector coordinates
        """
        sum = 0
        for num in self.__coordinates:
            sum += num

        return sum

    def dot_product(self, vector2):
        """
        multiply two vectors and summarize the values of the result-vectors
        """
        return (self * vector2).sum_of_coordinates()

    def in_range(self, smallest, largest):
        """
        checks if all the coordinates in the vector 
        are equal or larger than "smallest"
        and smaller than largest
        """
        for coor in self.__coordinates:
            if coor not in range(smallest, largest):
                return False
        return True

    def calculate_angle_with_vector(self, vector2):
        """
        :param vector2: another Vector
        :return: the angle between this vector and vector2 in radians
        """
        dot_result = self.dot_product(vector2)
        absolute_value = abs(self) * abs(vector2)
        return math.acos(dot_result / absolute_value)

    def nth_axis(self, axis):
        """
        :param axis: the axis needed
        :return: the axis vector in the given dimension
        that has the same coordinate length as the vector
        for example if the vector is (2,5,6) and the given axis is
        2, it returns (0,1,0)

        if the given dimension is greater than the vector length
        it returns None
        """
        if axis > len(self.__coordinates):
            return None

        axis_coordinates = [0] * len(self.__coordinates)
        axis_coordinates[axis - 1] = 1

        return Vector(*axis_coordinates)

    def calculate_angle_with_nth_axis(self, axis):
        """
        :param vector2: another Vector
        :return: the angle between this vector and vector2 in radians
        """
        vector2 = self.nth_axis(axis)
        dot_result = self.dot_product(vector2)
        absolute_value = abs(self) * abs(vector2)
        return math.acos(dot_result / absolute_value)

    def rotate_2d_vector(self, angle_of_rotation):
        """
        :param angle_of_rotation: the angle to be rotated by, in radians
        :return:  if the vector dimension is bigger than 2 it returns
        None
        else
        it returns a new Vector with new values
        as given by rotating the vector around the origin by the degrees
        given in an anti clockwise fashion
        """
        if len(self.__coordinates) > 2:
            return None

        sin_ang = math.sin(angle_of_rotation)
        cos_ang = math.cos(angle_of_rotation)

        x_value = self.__coordinates[0]
        y_value = self.__coordinates[1]

        new_x_value = cos_ang * x_value - sin_ang * y_value
        new_y_value = cos_ang * y_value + sin_ang * x_value

        new_x_value = round(new_x_value, Vector.ROUND_AFTER_ROTATE_BY)
        new_y_value = round(new_y_value, Vector.ROUND_AFTER_ROTATE_BY)

        return Vector(new_x_value, new_y_value)
