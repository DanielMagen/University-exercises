#############################################################
# FILE : four_in_a_row.py (file 4 out of 7)
# WRITER 1 : Daniel Magen ,login user -
# WRITER 2 : Omer Liberman,, login user -
# EXERCISE : EX 12
# DESCRIPTION: In this file we implemented main function
# which works with sys module.
#############################################################


import sys
import socket
from game import Game

DEFAULT_ARGUMENTS_LENGTH = [3, 4]
# the expected possible lengths of the arguments given
ILLEGAL_NUM_ARGS = "Illegal program arguments."
ILLEGAL_PORT_NUM = "Illegal program arguments."
ILLEGAL_PLAYER = "Illegal program arguments."
HUMAN = "human"
AI = "ai"


def main(args):
    """
    :param args: the arguments given by the user in the console
    """
    if len(args) not in DEFAULT_ARGUMENTS_LENGTH:
        # checks the given arguments are in the length expected
        print(ILLEGAL_NUM_ARGS)
        sys.exit()

    is_human = args[1]

    if is_human == HUMAN:
        is_human = True
    elif is_human == AI:
        is_human = False
    else:
        # the user entered an unknown string
        print(ILLEGAL_PLAYER)
        sys.exit()

    port = int(args[2])
    ip = None

    is_server = True
    if len(args) == DEFAULT_ARGUMENTS_LENGTH[1]:
        is_server = False
        ip = args[-1]

    if port not in range(1, 65536):
        # there is no such port
        print(ILLEGAL_PORT_NUM)
        sys.exit()

    if is_server:
        server = Game(is_human, is_server, port)
    else:
        client = Game(is_human, is_server, port, ip)


if __name__ == '__main__':
    main(sys.argv)
