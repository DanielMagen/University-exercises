#############################################################
# FILE : ai.py (file 2 out of 7)
# WRITER 1 : Daniel Magen ,login user -
# WRITER 2 : Omer Liberman,, login user -
# EXERCISE : EX 12
# DESCRIPTION: In this file we implemented the class AI
#############################################################


import random


class AI:
    """
    This function defines the AI user we were asked to implement.
    """

    NO_LEGAL_MOVES = "No possible AI moves"

    def __init__(self):
        pass

    def find_legal_move(self, game, func, timeout=None):
        """
        The function uses the method find free slots on board
        which is a method of board.
        Then it randomizes a column in the game which has free slot.
        """
        free_slots_on_board = game.board.find_free_slots()

        if len(free_slots_on_board) == 0:
            raise Exception(AI.NO_LEGAL_MOVES)

        chosen_column = random.choice(free_slots_on_board)
        return chosen_column
