#############################################################
# FILE : asteroid_main.py
# WRITER 1 : Daniel Magen ,login user -
# WRITER 2 : Omer Liberman,, login user -
# EXERCISE : EX 9
# DESCRIPTION: In this file we implemented the class GameRunner
# and the function main which runs the game
#############################################################

from screen import Screen
import sys
import math
import random
from torpedo import Torpedo
from asteroid import Asteroid
from ship import Ship
from vector import Vector


class GameRunner:
    DEFAULT_ASTEROIDS_NUM = 5
    ROTATE_LEFT = 7
    ROTATE_RIGHT = -7
    SCORE_ACCORDING_TO_ASTEROID_SIZE = {3: 20, 2: 50, 1: 100}
    MAX_TORPEDO_LIFE_CYCLES = 200
    MAX_NUM_OF_SIMULTANEOUS_TORPDEOS = 15
    START_SCORE_AT = 0
    MIN_ASTEROID_SPEED = 1
    MAX_ASTEROID_SPEED = 3
    START_SIZE_OF_ASTEROID = 3
    NUMBER_OF_ASTEROIDS_AFTER_SPLIT = 2
    FULL_ROTATION_IN_RADIANS = math.pi * 2
    MESSAGE_SHIP_LOST_LIFE = "Your Ship Has Crushed"
    MESSAGE_SHIP_LOST_LIFE_TITLE = "Your Ship Lost Life"
    MESSAGE_WON = "Congratulation"
    MESSAGE_WON_TITLE = "Win"
    MESSAGE_LOSE = "You lost"
    MESSAGE_LOSE_TITLE = "Lose"
    MESSAGE_QUIT = "You Choose To Quit"
    MESSAGE_QUIT_TITLE = "Quit"

    def __init__(self, asteroids_amnt):
        """
        :param asteroids_amnt: number of asteroids in the game
        This function initialize the game Asteroid
        """
        self._screen = Screen()
        self.screen_max_x = Screen.SCREEN_MAX_X
        self.screen_max_y = Screen.SCREEN_MAX_Y
        self.screen_min_x = Screen.SCREEN_MIN_X
        self.screen_min_y = Screen.SCREEN_MIN_Y

        self._max_coordinates_vector = \
            Vector(self.screen_max_x, self.screen_max_y)

        self._min_coordinates_vector = \
            Vector(self.screen_min_x, self.screen_min_y)

        self._delta_axis_vector = \
            self._max_coordinates_vector - self._min_coordinates_vector

        self._ship = self.create_new_ship()
        self._asteroid_list = self.create_asteroids(asteroids_amnt)
        self._torpedos_list = []

        self._score = GameRunner.START_SCORE_AT
        self.draw_score()

    def get_random_location_tuple(self):
        """
        This function randomize the locations of the game objects
        :return: random location on the board , presented as tuple (x,y)
        """
        random_x = random.randint(self.screen_min_x, self.screen_max_x)
        random_y = random.randint(self.screen_min_y, self.screen_max_y)

        return random_x, random_y

    def get_random_asteroid_speed(self):
        """
        randomize the speed of the asteroids
        """
        random_x = random.randint(GameRunner.MIN_ASTEROID_SPEED,
                                  GameRunner.MAX_ASTEROID_SPEED)

        random_y = random.randint(GameRunner.MIN_ASTEROID_SPEED,
                                  GameRunner.MAX_ASTEROID_SPEED)

        return random_x, random_y

    def run(self):
        self._do_loop()
        self._screen.start_screen()

    def _do_loop(self):
        # You don't need to change this method!
        self._game_loop()

        # Set the timer to go off again
        self._screen.update()
        self._screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        """
        This function runs the entire game.
        """
        self.move_objects()
        self.draw_objects()
        self.check_asteroid_collisions()
        self.check_and_remove_torpedos_life_cycle()
        self.check_input()

        if self.won():
            self._screen.show_message(GameRunner.MESSAGE_WON_TITLE,
                                      GameRunner.MESSAGE_WON)
            self.end_game()

        if self.lost():
            self._screen.show_message(GameRunner.MESSAGE_LOSE_TITLE,
                                      GameRunner.MESSAGE_LOSE)
            self.end_game()

        if self._screen.should_end():
            self._screen.show_message(GameRunner.MESSAGE_QUIT_TITLE,
                                      GameRunner.MESSAGE_QUIT)
            self.end_game()

    def check_input(self):
        """
        This function checks the validity of the inputs and executes
        functions according to what pressed.
        """
        if self._screen.is_space_pressed():
            self.create_new_torpedo()

        if self._screen.is_left_pressed():
            self._ship.rotate(math.radians(GameRunner.ROTATE_LEFT))

        if self._screen.is_right_pressed():
            self._ship.rotate(math.radians(GameRunner.ROTATE_RIGHT))

        if self._screen.is_up_pressed():
            self._ship.accelerate(self.calc_new_speed)

    def won(self):
        """
        This functions returns True if the asteroid list
        is empty (which is the condition to win the game)
        """
        return len(self._asteroid_list) == 0

    def lost(self):
        """
        This functions returns True if the ship's life is zero
        (which means the user lost)
        """
        return self._ship.get_life() == 0

    def end_game(self):
        """
        exiting from the game
        """
        self._screen.end_game()
        sys.exit()

    def create_new_ship(self):
        """
        Creates the ship in random location and present on the game screen
        """
        location_tuple = self.get_random_location_tuple()
        new_ship = Ship(location_tuple)
        self._screen.draw_ship(*location_tuple,
                               new_ship.get_direction_angle_in_degrees())
        return new_ship

    def create_asteroids(self,
                         num_of_asteroids_to_create,
                         location_vectors_list=None,
                         speed_vectors_list=None,
                         size_list=None):
        """
        :param num_of_asteroids_to_create: default number of 5 
        as given in the exercise
        :param location_vectors_list: list of the asteroids random locations
        :param speed_vectors_list: list of the asteroids random speeds
        :param size_list: list of the asteroids sizes 
        (the size is 3 at the beginning)

        The function creates 5 asteroids with the information in the lists

        :return: list of 5 asteroids
        """

        asteroids_added = []
        # starts an empty list which the new asteroids is going to be

        if location_vectors_list is None:
            # uses create_random_location_vectors_for_asteroids to 
            # create list of random locations for the new asteroids
            location_vectors_list = self.create_random_location_vectors_for_asteroids(
                num_of_asteroids_to_create)

        if speed_vectors_list is None:
            # uses create_random_speed_vectors_for_asteroids 
            # to create list of random speed locations for the new asteroids
            speed_vectors_list = self.create_random_speed_vectors_for_asteroids(
                num_of_asteroids_to_create)

        if size_list is None:
            # uses create_size_list_for_asteroids 
            # to create list of sizes for the new asteroids
            size_list = self.create_size_list_for_asteroids(
                num_of_asteroids_to_create)

        #  the for loop creates the asteroids with the data in lists which 
        # created in the 3 if's above append them to the 
        # list of asteroids and screen them

        for i in range(num_of_asteroids_to_create):
            new_asteroid = Asteroid(location_vectors_list[i],
                                    speed_vectors_list[i],
                                    size_list[i])
            asteroids_added.append(new_asteroid)
            self._screen.register_asteroid(new_asteroid,
                                           new_asteroid.get_size())

        self.draw_asteroids(asteroids_added)

        return asteroids_added

    def create_random_location_vectors_for_asteroids(self, num_of_asteroids_to_create):
        """
        :param num_of_asteroids_to_create: number of asteroids
        :return: list of random asteroids location vectors
        """
        location_vectors_list = []
        ship_location_vector = self._ship.get_location_vector()

        for _ in range(num_of_asteroids_to_create):
            location_tuple = self.get_random_location_tuple()
            location_vector = Vector(*location_tuple)

            while ship_location_vector == location_vector:
                location_tuple = self.get_random_location_tuple()
                location_vector = Vector(*location_tuple)

            location_vectors_list.append(location_vector)

        return location_vectors_list

    def create_random_speed_vectors_for_asteroids(self, num_of_asteroids_to_create):
        """
        :param num_of_asteroids_to_create: create_size_list_for_asteroids
        :return: list of random asteroids speed vectors
        """
        speed_vectors_list = []

        for _ in range(num_of_asteroids_to_create):
            speed_tuple = self.get_random_asteroid_speed()
            speed_vector = Vector(*speed_tuple)
            speed_vectors_list.append(speed_vector)

        return speed_vectors_list

    def create_size_list_for_asteroids(self, num_of_asteroids_to_create):
        """
        :param num_of_asteroids_to_create: create_size_list_for_asteroids
        :return: list of asteroids sizes (default size)
        """
        return [GameRunner.START_SIZE_OF_ASTEROID] * num_of_asteroids_to_create

    def draw_ship(self):
        """
        Uses the function draw_ship in Screen to present the ship on the screen
        """
        ship_location = self._ship.get_location_tuple()
        self._screen.draw_ship(ship_location[0],
                               ship_location[1],
                               self._ship.get_direction_angle_in_degrees())

    def draw_torpedos(self, torpedos_list):
        """
        Uses the function draw_torpedo in Screen 
        to present the torpedos on the screen
        """
        for torpedo in torpedos_list:
            self._screen.draw_torpedo(torpedo,
                                      *torpedo.get_location_tuple(),
                                      self._ship.get_direction_angle_in_degrees())

    def draw_asteroids(self, asteroids_list):
        """
        Uses the function draw_asteroid in Screen
        to present the asteroids on the screen
        """
        for asteroid in asteroids_list:
            self._screen.draw_asteroid(asteroid,
                                       *asteroid.get_location_tuple())

    def draw_score(self):
        """
        Uses the function set_score in Screen to present the current score in
        the game and updates it on the screen
        """
        self._screen.set_score(self._score)

    def draw_objects(self):
        """
        Summons all the functions that draws objects together
        """
        self.draw_ship()
        self.draw_asteroids(self._asteroid_list)
        self.draw_torpedos(self._torpedos_list)

    def calc_new_position(self, location_vector, speed_vector):
        """
        :param location_vector: vector that indicates the 
        location of the object on the axis's
        :param speed_vector: vector that indicates the 
        speed of the object on the axis's
        :return: the new location vector according to the given formula
        """
        return (speed_vector
                + location_vector
                - self._min_coordinates_vector) \
               % self._delta_axis_vector \
               + self._min_coordinates_vector

    def calc_new_speed(self, speed_vector, degree_in_radians):
        """
        :param speed_vector: vector that indicates 
        the speed of the object on the axis's
        :param degree_in_radians: the wanted direction for the object
        :return: the new speed vector of the object on each axis
        """
        accel_vector = Vector(math.cos(degree_in_radians),
                              math.sin(degree_in_radians))

        return speed_vector + accel_vector

    def calc_new_torpedo_speed(self, speed_vector, degree_in_radians):
        """
        :param speed_vector: vector that indicates 
        the speed of the object on the axis's
        :param degree_in_radians: the direction where the torpedo goes
        :return: the speed vector of the torpedo
        """
        multiply_argument_by = 2
        accel_vector = Vector(math.cos(degree_in_radians),
                              math.sin(degree_in_radians))

        return speed_vector + accel_vector * multiply_argument_by

    def calc_asteroids_speed_vectors_after_torpedo_collision(self,
                                                             torpedo,
                                                             asteroid):
        """
        :param torpedo: Torpedo object
        :param asteroid: Asteroid object which was hit by the torpedo
        :return: the speed of the 2 new asteroids
        """
        asteroid_speed_vector = asteroid.get_speed_vector()

        new_asteroid_speed_vector = (torpedo.get_speed_vector()
                                     + asteroid_speed_vector) / abs(asteroid_speed_vector)

        new_asteroid_speed_vectors_list = [new_asteroid_speed_vector]

        rotate_asteroid_by = \
            GameRunner.FULL_ROTATION_IN_RADIANS / GameRunner.NUMBER_OF_ASTEROIDS_AFTER_SPLIT

        for _ in range(GameRunner.NUMBER_OF_ASTEROIDS_AFTER_SPLIT - 1):
            asteroid_speed_vector = new_asteroid_speed_vectors_list[-1]
            rotated_speed_vector = \
                asteroid_speed_vector.rotate_2d_vector(rotate_asteroid_by)
            new_asteroid_speed_vectors_list.append(rotated_speed_vector)

        return new_asteroid_speed_vectors_list

    def move_objects(self):
        """
        Moves all the objects on the screen
        """
        self._ship.move_ship(self.calc_new_position)

        for asteroid in self._asteroid_list:
            asteroid.move_asteroid(self.calc_new_position)

        for torpedo in self._torpedos_list:
            torpedo.move_torpedo(self.calc_new_position)
            torpedo.update_life_cycle()

    def create_new_torpedo(self):
        """
        Creates new torpedo object
        """
        if len(self._torpedos_list) >= GameRunner.MAX_NUM_OF_SIMULTANEOUS_TORPDEOS:
            return

        ship_direction_angle = self._ship.get_direction_angle_in_radians()
        ship_speed_vec = self._ship.get_speed_vector()

        new_torpedo_speed_vector = self.calc_new_torpedo_speed(ship_speed_vec,
                                                               ship_direction_angle)
        new_torpedo = Torpedo(self._ship.get_location_vector(),
                              ship_direction_angle,
                              new_torpedo_speed_vector)

        self._torpedos_list.append(new_torpedo)
        self._screen.register_torpedo(new_torpedo)
        self.draw_torpedos([new_torpedo])

    def check_and_remove_torpedos_life_cycle(self):
        """
        Remove torpedo from the screen when it crosses his maximum life time
        """
        indices_of_torpedos_to_remove = set([])

        for i in range(len(self._torpedos_list)):
            if \
                    self._torpedos_list[i].get_life_cycle() > GameRunner.MAX_TORPEDO_LIFE_CYCLES:
                indices_of_torpedos_to_remove.add(i)

        self.asta_la_vista_torpedos(list(indices_of_torpedos_to_remove))

    def spaceship_collisions_with_asteroids_checker_and_handler(self):
        """
        Deals with the case that ship is collided with asteroid
        """
        indices_of_asteroid_to_remove = set([])

        for i in range(len(self._asteroid_list)):
            if self._asteroid_list[i].has_intersection(self._ship):
                self._screen.show_message(GameRunner.MESSAGE_SHIP_LOST_LIFE_TITLE,
                                          GameRunner.MESSAGE_SHIP_LOST_LIFE)
                self._screen.remove_life()
                self._ship.lose_life()
                indices_of_asteroid_to_remove.add(i)

        self.asta_la_vista_asteroids(list(indices_of_asteroid_to_remove))

    def torpedos_collisions_with_asteroids_checker_and_handler(self):
        """
        Deals with the case that torpedo is collided with asteroid
        """
        indices_of_asteroid_to_remove = set([])
        indices_of_torpedos_to_remove = set([])
        asteroids_to_add_to_our_asteroid_list = []

        for i in range(len(self._torpedos_list)):
            for j in range(len(self._asteroid_list)):

                if self._asteroid_list[j].has_intersection(self._torpedos_list[i]):

                    self.update_score(self._asteroid_list[j].get_size())
                    new_asteroids = self.split_asteroid(self._torpedos_list[i], j)

                    if new_asteroids is not None:
                        asteroids_to_add_to_our_asteroid_list += new_asteroids

                    indices_of_asteroid_to_remove.add(j)
                    indices_of_torpedos_to_remove.add(i)

        self._asteroid_list += asteroids_to_add_to_our_asteroid_list
        self.asta_la_vista_asteroids(list(indices_of_asteroid_to_remove))
        self.asta_la_vista_torpedos(list(indices_of_torpedos_to_remove))

    def update_score(self, size_of_asteroid):
        """
        :param size_of_asteroid:
        updates the score when hitting asteroid with torpedo
        """
        self._score += GameRunner.SCORE_ACCORDING_TO_ASTEROID_SIZE[size_of_asteroid]
        self._screen.set_score(self._score)

    def split_asteroid(self, torpedo, index_of_asteroid_to_split):
        """
        :param torpedo: Torpedo object that hits the asteroid
        :param index_of_asteroid_to_split: the index of the 
        asteroid that was hit in the asteroids list
        :return: 2 new smaller asteroids
        """
        asteroid = self._asteroid_list[index_of_asteroid_to_split]
        if asteroid.get_size() == Asteroid.MIN_SIZE:
            return []

        new_asteroids_speed_vectors = \
            self.calc_asteroids_speed_vectors_after_torpedo_collision(torpedo,
                                                                      asteroid)

        new_asteroids_added = self.create_asteroids(
            GameRunner.NUMBER_OF_ASTEROIDS_AFTER_SPLIT,
            [asteroid.get_location_vector()] * GameRunner.NUMBER_OF_ASTEROIDS_AFTER_SPLIT,
            new_asteroids_speed_vectors,
            [asteroid.get_size() - 1] * GameRunner.NUMBER_OF_ASTEROIDS_AFTER_SPLIT)

        return new_asteroids_added

    def check_asteroid_collisions(self):
        """
        Operates the cases of collisions with asteroids
        """
        self.spaceship_collisions_with_asteroids_checker_and_handler()
        self.torpedos_collisions_with_asteroids_checker_and_handler()

    def asta_la_vista_torpedos(self, indices_of_torpedos_to_remove_list):
        """
        remove torpedo from list of torpedos and screen
        """
        self.remove_indices_from_list(self._torpedos_list,
                                      indices_of_torpedos_to_remove_list,
                                      self.remove_torpedo_from_screen)

    def remove_torpedo_from_screen(self, torpedo):
        """
        remove torpedo from screen , using the unregister_torpedo from Screen
        """
        self._screen.unregister_torpedo(torpedo)

    def asta_la_vista_asteroids(self, indices_of_asteroids_to_remove_list):
        """
        remove asteroids from list of asteroids and screen
        """
        self.remove_indices_from_list(self._asteroid_list,
                                      indices_of_asteroids_to_remove_list,
                                      self.remove_asteroid_from_screen)

    def remove_asteroid_from_screen(self, asteroid):
        """
        remove asteroid from screen , using the unregister_asteroid from Screen
        """
        self._screen.unregister_asteroid(asteroid)

    @staticmethod
    def remove_indices_from_list(lst,
                                 indices,
                                 function_to_call_on_each_item_in_list_before_removal=None):
        """
        :param lst: list of objects
        :param indices: indices should be removed
        :param function_to_call_on_each_item_in_list_before_removal
        This function removes the given indices from list
        """
        indices = sorted(indices)
        for i in range(len(indices) - 1, -1, -1):
            if function_to_call_on_each_item_in_list_before_removal is not None:
                function_to_call_on_each_item_in_list_before_removal(lst[indices[i]])
            del lst[indices[i]]


#  Here lies the main function which runs the game Asteroid
def main(amnt):
    runner = GameRunner(amnt)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(GameRunner.DEFAULT_ASTEROIDS_NUM)
