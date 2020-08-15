#############################################################
# FILE : asteroid.py
# WRITER 1 : Daniel Magen ,login user -
# WRITER 2 : Omer Liberman,, login user -
# EXERCISE : EX 9
# DESCRIPTION: In this file we implemented the class Asteroid
#############################################################

import random
from vector import Vector


class Asteroid:
    """
    A class representing an asteroid in the game of Asteroids.
    """
    MIN_SIZE = 1
    SIZE_COEFFICIENT = 10
    NORMALIZE_FACTOR = -5

    def __init__(self, location_vector, speed_vector, size):
        self.location_vector = location_vector
        self.speed_vector = speed_vector
        self.size = size
        self.radius = size * Asteroid.SIZE_COEFFICIENT + Asteroid.NORMALIZE_FACTOR

    def has_intersection(self, obj):
        """
        This function returns boolean value if any object
        is close to asteroid (if the object is very close it indicates
        a crash
        """
        distance_to_object = self.calculate_distance_with_object(obj)
        return distance_to_object <= self.radius

    def calculate_distance_with_object(self, obj):
        """
        Calculates the distance between the asteroid and the object given
        """
        obj_location_vector = obj.get_location_vector()
        return abs(self.location_vector - obj_location_vector)

    def move_asteroid(self, changing_location_function):
        """
        :param changing_location_function:         
        function changing_location_vector
        which receives a location vector and a speed vector and
        calculates the new location
        """
        self.location_vector = \
            changing_location_function(self.location_vector, self.speed_vector)

    def get_radius(self):
        """
        radius getter
        """
        return self.radius

    def get_size(self):
        """
        size getter
        """
        return self.size

    def get_min_size(self):
        """
        returns 1 (the minimum size of asteroid
        """
        return Asteroid.MIN_SIZE

    def get_location_vector(self):
        """
        returns a copy of asteroid location vector
        """
        return self.location_vector.get_copy()

    def get_location_tuple(self):
        """
        returns the location of the asteroid
        """
        return self.location_vector.get_coordinates()

    def get_speed_vector(self):
        """
        returns the speed vector of the asteroid
        """
        return self.speed_vector.get_copy()
