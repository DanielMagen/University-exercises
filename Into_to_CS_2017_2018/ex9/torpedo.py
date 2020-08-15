#############################################################
# FILE : torpedo.py
# WRITER 1 : Daniel Magen ,login user -
# WRITER 2 : Omer Liberman,, login user -
# EXERCISE : EX 9
# DESCRIPTION: In this file we implemented the class torpedo
#############################################################

import random
from vector import Vector


class Torpedo:
    TORPEDO_RADIUS = 4
    STARTING_NUMBER_OF_LIFE_CYCLES = 1
    RAISE_LIFE_CYCLE_BY = 1

    def __init__(self, location_vector, direction_angle, speed_vector):
        self.location_vector = location_vector
        self.speed_vector = speed_vector
        self.direction_angle = direction_angle
        self.life_cycle = Torpedo.STARTING_NUMBER_OF_LIFE_CYCLES

    def get_radius(self):
        """
        :return: the integer 4 (the default radius of the torpedo)
        """
        return Torpedo.TORPEDO_RADIUS

    def get_life_cycle(self):
        """
        life getter
        """
        return self.life_cycle

    def update_life_cycle(self):
        """
        This function updates the life of the torpedo each
        round of the game
        """
        self.life_cycle += Torpedo.RAISE_LIFE_CYCLE_BY

    def move_torpedo(self, changing_location_function):
        """
        This function moves the torpedo, it uses the 
        function changing_location_vector
        which receives a location vector and a speed vector and
        calculates the new location
        :param changing_location_function:
        """
        self.location_vector = changing_location_function(self.location_vector,
                                                          self.speed_vector)

    def get_location_vector(self):
        """
        returns a copy of the location vector
        """
        return self.location_vector.get_copy()

    def get_location_tuple(self):
        """
        location getter
        """
        return self.location_vector.get_coordinates()

    def get_speed_vector(self):
        """
        speed getter
        """
        return self.speed_vector.get_copy()
