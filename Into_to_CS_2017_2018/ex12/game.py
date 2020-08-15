#############################################################
# FILE : game.py (file 1 out of 7)
# WRITER 1 : Daniel Magen ,login user -
# WRITER 2 : Omer Liberman,, login user -
# EXERCISE : EX 12
# DESCRIPTION: In this file we implemented the class Game
#############################################################


import tkinter as tki
from GUI import FourInARowGui
import socket
from communicator import Communicator
from Board import Game_Board
from ai import AI


class Game:
    """
    This class represents the game 4 in a row we were asked to implement.
    """

    PLAYER_ONE = 0
    PLAYER_TWO = 1
    DRAW = 2
    NUMBER_TO_PLAYER = {PLAYER_ONE: "Server", PLAYER_TWO: "Client"}
    CONTINUE_GAME = 3
    ILLEGAL_MOVE = "Illegal move"
    PLAYER_ONE_WON_MSG = NUMBER_TO_PLAYER[PLAYER_ONE] + " has won the game"
    PLAYER_TWO_WON_MSG = NUMBER_TO_PLAYER[PLAYER_TWO] + " has won the game"
    DRAW_MSG = "There is a draw"
    DEFAULT_NUMBER_OF_ROWS = 6
    DEFAULT_NUMBER_OF_COLS = 7
    NUMBER_OF_ELEMENTS_IN_SEQUENCE = 4
    WIN_NOT_FOUND = -2
    DEFAULT_IP = socket.gethostbyname(socket.gethostname())
    AI_DEFAULT_VALUE = None

    def __init__(self,
                 is_human,
                 is_server,
                 port,
                 ip_of_server=DEFAULT_IP):
        """
        :param is_human: string. Describes if the player is human or ai.
        :param is_server: boolean value. If True, the user is the server
        and plays first, otherwise the player is the client and plays second.
        :param port: the port number the players uses for the game.
        goes between 1 to 65355.
        :param ip_of_server: the ip number of the server.
        the client insert this number.
        """
        # Creates the board game
        self.board = Game_Board(Game.DEFAULT_NUMBER_OF_COLS,
                                Game.DEFAULT_NUMBER_OF_ROWS,
                                Game.PLAYER_ONE,
                                Game.PLAYER_TWO,
                                Game.DRAW,
                                Game.WIN_NOT_FOUND,
                                Game.NUMBER_OF_ELEMENTS_IN_SEQUENCE)

        self.root = tki.Tk()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Creates the GUI method of the game
        self.gameGui = FourInARowGui(self.root,
                                     self.make_move,
                                     Game.DEFAULT_NUMBER_OF_ROWS,
                                     Game.DEFAULT_NUMBER_OF_COLS,
                                     screen_height,
                                     screen_width)

        # Defines which player begins.
        if is_server:
            self.root.title("Server")
            self.__communicator = Communicator(self.root, port)
        else:
            self.root.title("Client")
            self.__communicator = Communicator(self.root,
                                               port,
                                               ip_of_server)
            self.gameGui.lock_player()

        self.__communicator.bind_action_to_message(self.act_upon_message)
        self.__communicator.connect()

        # sets whose turn it is
        current_player = self.get_current_player()
        self.change_whose_turn_label(self.get_other_player(current_player))

        # Creates AI user if needed
        self.ai = Game.AI_DEFAULT_VALUE
        if not is_human:
            self.ai = AI()
            if is_server:
                self.make_ai_move()
            else:
                self.gameGui.lock_player()

        self.run_game()

    def run_game(self):
        """
        The function runs the game.
        """
        self.root.mainloop()

    def make_ai_move(self):
        """
        Makes an AI move if there is an ai player.
        :return:
        """
        col = self.ai.find_legal_move(self, self.make_ai_func())
        self.gameGui.simulate_press_by_ai(col)

    def act_upon_message(self, message):
        """
        :param message: a message given by the client or the server
        the message is expected to be the number of the column that was pressed
        :return:
        """
        current_player = self.get_current_player()
        self.change_whose_turn_label(current_player)

        self.gameGui.unlock_player()
        self.gameGui.simulate_press(int(message))

        if self.ai is not Game.AI_DEFAULT_VALUE:
            self.make_ai_move()

    def send_action_to_other_player(self, column):
        """
        :param column: the column the user has pressed
        locks the current player from pressing any other column
        and sends the column that was pressed on as a message to the
        other player
        """
        current_player = self.get_current_player()
        self.change_whose_turn_label(current_player)

        self.gameGui.lock_player()
        self.__communicator.send_message(str(column))

    def change_whose_turn_label(self, current_player):
        """
        :param current_player: the code of the current player
        changes the label such that it will say that the turn
        is that of the other player
        """
        whose_turn = \
            Game.NUMBER_TO_PLAYER[self.get_other_player(current_player)] + " Turn"
        self.gameGui.change_top_label(whose_turn)

    def get_other_player(self, current_player):
        """
        :param current_player: the player who is playing now
        :return: the other player
        """
        if current_player == Game.PLAYER_ONE:
            return Game.PLAYER_TWO
        if current_player == Game.PLAYER_TWO:
            return Game.PLAYER_ONE

    def make_move(self,
                  column,
                  me_has_pressing=True,
                  illegal_move_was_made=False):
        """
        This function implement single move in the game
        :param column: the column the player choose
        :param me_has_pressing: if the player pressed something
        :param illegal_move_was_made: a boolean, if its true an exception
        will be raised
        """
        if illegal_move_was_made:
            raise Exception(Game.ILLEGAL_MOVE)

        if me_has_pressing:
            self.send_action_to_other_player(column)

        current_player = self.get_current_player()

        if not self.board.valid_player(current_player):
            raise Exception(Game.ILLEGAL_MOVE)
        else:
            self.board.move_of_player(current_player, column)

            self.check_status()

    def check_status(self):
        """
        The function deals with cases of winning or draw in the game.
        Than it shuts the game down.
        """
        win_check = self.board.check_if_there_is_win()
        if win_check:
            # The winner player and the sequence of slots that won the game
            winner = win_check[0]
            win_sequence = win_check[1]
            win_sequence = Game.reverse_tuples_in_list(win_sequence)
            # Displaying the message to the players
            self.gameGui.game_over(self.final_stage_msg(winner), win_sequence)
            self.reset_ai()

        if self.board.check_board_if_full():
            # Displaying draw message to the players
            self.gameGui.game_over(self.final_stage_msg(Game.DRAW))
            self.reset_ai()

    def get_winner(self):
        """
        this function checks if there is a winner or a draw
        if there is a winner it returns the code of the player that won
        if there is a draw it returns the code for a draw
        if none of the above it returns None
        """
        win_check = self.board.check_if_there_is_win()
        if win_check:
            winner = win_check[0]
            return winner
        if self.board.check_board_if_full():
            return Game.DRAW

    def reset_ai(self):
        """
        Changes the ai to None
        """
        self.ai = Game.AI_DEFAULT_VALUE

    def final_stage_msg(self, winner_num):
        """
        printing message to the screen for win or draw
        """
        if winner_num == Game.PLAYER_ONE:
            return Game.PLAYER_ONE_WON_MSG

        if winner_num == Game.PLAYER_TWO:
            return Game.PLAYER_TWO_WON_MSG

        if winner_num == Game.DRAW:
            return Game.DRAW_MSG

    def get_player_at(self, row, col):
        """
        returns which player is on specific location
        """
        board = self.board.get_board()
        return board[row][col]

    def get_current_player(self):
        """
        returns whose turn is it now
        """
        return self.board.board_status()

    def make_ai_func(self):
        """
        Implement the moves of the AI.
        """

        def make_ai_move(col):
            self.gameGui.simulate_press(col)

        return make_ai_move

    @staticmethod
    def reverse_tuples_in_list(list_of_tuples):
        """
        :param list_of_tuples
        returns the same list with the same tuples but repositioned.
        """
        new_list = []
        for tpl in list_of_tuples:
            new_list.append(tuple(reversed(tpl)))
        return new_list
