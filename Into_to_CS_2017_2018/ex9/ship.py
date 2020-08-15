#############################################################
# FILE : ship.py
# WRITER 1 : Daniel Magen ,login user -
# WRITER 2 : Omer Liberman,, login user -
# EXERCISE : EX 9
# DESCRIPTION: In this file we implemented the class Ship
#############################################################

import random
import math
from vector import Vector


class Ship:
    """
    A class representing a ship in the game of Asteroids.
    The ship moves according to the user choice and can fire torpedo bullets.
    """
    SHIP_RADIUS = 1
    STARTING_NUMBER_OF_LIFES = 3
    STARTING_ANGLE_IN_RADIANS = 0
    SHIP_STARTING_SPEED = 0
    DEFAULT_LIFE_LOSS = 1

    def __init__(self, location_tuple):
        self.location_vector = Vector(*location_tuple)
        self.speed_vector = Vector(Ship.SHIP_STARTING_SPEED,
                                   Ship.SHIP_STARTING_SPEED)
        self.direction_angle = Ship.STARTING_ANGLE_IN_RADIANS
        self.life = Ship.STARTING_NUMBER_OF_LIFES

    def move_ship(self, changing_location_function):
        """
        This function moves the ship according to given location
        :param changing_location_function:         
        a functions which receives a location vector and a speed vector and
        calculates the new location
        """
        self.location_vector = changing_location_function(self.location_vector,
                                                          self.speed_vector)

    def rotate(self, degrees_in_radians):
        """
        This function changes rotates the head of the ship
        :param degrees_in_radians: the new direction where the ship should go
        """
        self.direction_angle = self.direction_angle + degrees_in_radians

    def accelerate(self, changing_speed_function):
        """
        This function updates the speed vector of the ship
        :param changing_speed_function: a function 
        which receives a speed vector and a direction angle
        calculates the new speed vector
        """
        self.speed_vector = changing_speed_function(self.speed_vector,
                                                    self.direction_angle)

    def get_radius(self):
        """
        radius getter
        """
        return Ship.SHIP_RADIUS

    def lose_life(self):
        """
        life reducer
        """
        self.life -= Ship.DEFAULT_LIFE_LOSS

    def get_life(self):
        """
        life getter
        """
        return self.life

    def get_location_vector(self):
        """
        returns copy of the location vector
        """
        return self.location_vector.get_copy()

    def get_speed_vector(self):
        """
        speed getter
        """
        return self.speed_vector.get_copy()

    def get_location_tuple(self):
        """
        returns the location vector
        """
        return self.location_vector.get_coordinates()

    def get_direction_angle_in_radians(self):
        """
        returns the direction angle of the ship in radians
        """
        return self.direction_angle

    def get_direction_angle_in_degrees(self):
        """
        returns the direction angle of the ship in degrees
        """
        return math.degrees(self.direction_angle)
