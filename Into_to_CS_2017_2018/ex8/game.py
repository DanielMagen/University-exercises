#############################################################
# FILE : game.py
# WRITER : Daniel Magen
# EXERCISE : intro2cs ex8 2017-2018
# DESCRIPTION: this module contain a class in charge 
# of handling the game process called Game
#############################################################

############################################################
# Imports
############################################################
import game_helper as gh
from car import Car, Direction
from board import Board


############################################################
# Constants
############################################################


############################################################
# Class definition
############################################################


class Game:
    """
    A class representing a rush hour game.
    A game is composed of cars that are located on a square board and a user
    which tries to move them in a way that will allow the red car to get out
    through the exit
    """
    MESSAGE_CAR_NOT_ON_BOARD = "The isn't any {} cars on the board"
    MESSAGE_CANT_MOVE_CAR = "The car couldn't be moved to the requested position"
    MESSAGE_HELLO = "Welcome to rush Hour game"
    LENGTH_OF_RED_CAR = 2
    COLOR_OF_RED_CAR = 'R'

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        self.__board = board
        self.VALID_COLORS = board.get_colors_of_cars_on_board()

    def single_turn(self):
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. The logic defined by this function must be implemented
        but if you wish to do so in another function (or some other functions)
        it is ok.

        The function runs one round of the game :
            1. Print board to the screen
            2. Get user's input of: what color car to move, and what direction to
                move it.
            2.a. Check the the input is valid. If not, print an error message and
                return to step 2.
            2. Move car according to user's input. If movement failed (trying
                to move out of board etc.), return to step 2. 
            3. Report to the user the result of current round ()
        """
        print(self.__board)

        car_color_to_move = self.get_color_input()
        car = self.__board.get_car_by_color(car_color_to_move)

        while car == False:
            # while the given color has no corresponding car on the board
            print(Game.MESSAGE_CAR_NOT_ON_BOARD.format(car_color_to_move))
            car_color_to_move = self.get_color_input()
            car = self.__board.get_car_by_color(car_color_to_move)

        direction_to_move = gh.get_direction()

        was_able_to_move = self.__board.move(car, direction_to_move)

        if not was_able_to_move:
            print(Game.MESSAGE_CANT_MOVE_CAR)

        return was_able_to_move

    def get_color_input(self):
        """
        the function is based on the one given to us by the helper class
        we were told that the input was not to be handled by us
        yet this function was not available without copying it directly into
        my code
        since I do not understand the join line completely and since this piece
        of code is in my code, I changed it to a simpler code which is 
        more understandable to me
        
        it receives a color input from the user and returns it if its valid
        """
        available_colors = ""

        if len(self.VALID_COLORS) > 0:
            available_colors = str(self.VALID_COLORS[0])

            for i in range(1, len(self.VALID_COLORS)):
                available_colors += ',' + str(self.VALID_COLORS[i])

        color_input = input(gh.MESSAGE_GET_COLOR_INPUT + available_colors)

        while not color_input in self.VALID_COLORS:
            print(gh.ERROR_CAR_COLOR)
            color_input = input(gh.MESSAGE_GET_COLOR_INPUT + available_colors)

        return color_input

    def update_valid_colors(self):
        """
        updates the colors of the cars in the game
        """
        self.VALID_COLORS = self.__board.get_colors_of_cars_on_board()

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        print(Game.MESSAGE_HELLO)
        start, orientation, _ = \
            self.__board. \
                get_red_car_location_orientation_and_deviation(Game.LENGTH_OF_RED_CAR)

        red_car = Car(Game.COLOR_OF_RED_CAR,
                      Game.LENGTH_OF_RED_CAR,
                      start,
                      orientation)

        self.__board.add_car(red_car)

        print(self.__board)

        num_of_cars_to_add = gh.get_num_cars()  # assumes input is valid

        for _ in range(num_of_cars_to_add):
            car_data = gh.get_car_input(self.__board.get_size())
            new_car = Car(*car_data)
            self.__board.add_car(new_car)
            self.update_valid_colors()
            print(self.__board)

        while \
                self.__board.min_distance_between_car_exit(Game.COLOR_OF_RED_CAR) > 1:
            # while the red car has still not reached the exit
            self.single_turn()

        gh.report_game_over()


############################################################
# An example usage of the game
############################################################
if __name__ == "__main__":
    board = Board({}, [7, 5])  # if using a dictionry of cars. use '[]' if using a list
    game = Game(board)
    game.play()
