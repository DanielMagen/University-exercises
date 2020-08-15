#############################################################
# FILE : Board.py (file 3 out of 7)
# WRITER 1 : Daniel Magen ,login user -
# WRITER 2 : Omer Liberman,, login user -
# EXERCISE : EX 12
# DESCRIPTION: In this file we implemented the class Game_Board
#############################################################

class Game_Board:
    """
    This class represents the board of the game, the moves of the players
     and define situations in the game as
    winning of one of the player or draw.
    """

    EMPTY_BLOCK = -1
    SEARCH_DIRECTIONS = [(1, 0), (0, 1), (1, -1), (-1, -1)]

    # all the possible search directions in the board

    def __init__(self,
                 width,
                 height,
                 player_one_code,
                 player_two_code,
                 draw_code,
                 win_not_found_code,
                 number_of_elements_in_winning_sequence):
        """
        :param width: the width of the board
        :param height: the height of the board
        :param player_one_code: the number which represents player one
        :param player_two_code: the number which represents player two
        :param draw_code: the number which represents draw situation
        :param win_not_found_code: the number which represents
        'winner yet found' in each round
        :param number_of_elements_in_winning_sequence:
        the number of adjacent elements needed for a win
        """
        self.board = [[Game_Board.EMPTY_BLOCK for _ in range(width)] for _ in
                      range(height)]
        self.width = width
        self.height = height
        self.player_one_code = player_one_code
        self.player_two_code = player_two_code
        self.draw_code = draw_code
        self.win_not_found_code = win_not_found_code

        self.win_sequence_len = number_of_elements_in_winning_sequence
        self.all_possible_sequences_in_game = \
            self.get_all_possible_sequences_in_game()

    def get_board(self):
        """
        board getter
        """
        return self.board

    def get_size_of_column(self, column):
        """
        :param column: number of column in the game
        :return: integer , represents the number of discs in the given column
        """
        count_num_of_discs = 0
        board_lists = self.board
        for row in range(self.height - 1, -1, -1):
            if board_lists[row][column] != Game_Board.EMPTY_BLOCK:
                count_num_of_discs += 1
        return count_num_of_discs

    def valid_move(self, column):
        """
        This function checks the validity of single move
        :param column: integer represents column in the game
        :return: boolean value whether the column reached the limit
        """
        if self.get_size_of_column(column) < self.height:
            return True
        else:
            return False

    def move_of_player(self, player, column):
        """
        With this function we make single move.
        The player chooses the column he wants to insert a disc to
        :param player: any player
        :param column: the column which the player wants to fill
        :return: True if move happened, False if not
        """
        game_board = self.board
        if self.valid_move(column):
            for row in range(self.height - 1, -1, -1):
                if game_board[row][column] == Game_Board.EMPTY_BLOCK:
                    game_board[row][column] = player
                    return True
                else:
                    continue
        else:
            return False

    def valid_player(self, player):
        """
        :param player: the player who wants to play
        :return: return true if the player who is playing now
        is the player who is suppose to play right now.
        """
        if self.board_status() == player:
            return True
        else:
            return False

    def board_status(self):
        """
        finds which player suppose to play right now.
        The main idea is that the number of discs of player one has to be
        equeal or greater by one than the number of discs of player two.
        """
        moves_of_one, moves_of_two = 0, 0
        game_board = self.board
        for row in range(self.height):
            for col in range(self.width):
                if game_board[row][col] == self.player_one_code:
                    moves_of_one += 1
                elif game_board[row][col] == self.player_two_code:
                    moves_of_two += 1
                else:
                    continue
        if moves_of_one == moves_of_two + 1:
            return self.player_two_code  # second player turn
        elif moves_of_two == moves_of_one:
            return self.player_one_code  # first player turn
        else:
            return 'PROBLEM'

    def find_free_slots(self):
        """
        This function goes along the columns of the board.
        If there is free slot in the column it adds the column number to a list
        The function returns a list of all the columns that has free slots.
        This function is used by the AI 'user'.
        """
        game_board = self.board
        list_of_free_slots = []
        for column in range(self.width):
            for row in range(self.height - 1, -1, -1):
                if game_board[row][column] == Game_Board.EMPTY_BLOCK:
                    list_of_free_slots.append(column)
                    break
                else:

                    continue
        return list_of_free_slots

    def get_all_possible_sequences_in_game(self):
        """
        The function finds all the possible sequences in the game of length
        4 (self.win_sequence_len).
        Then, it appends the sequence to a list of sequences.
        The function returns a list of all the sequences in length of 4
        in the game board.
        """
        all_possible_sequences_in_game = []

        for row in range(self.height):
            for col in range(self.width):
                for direction in Game_Board.SEARCH_DIRECTIONS:
                    # The function goes along each direction
                    # and creates sequences of four slots
                    new_sequence = []
                    for step in range(
                            self.win_sequence_len):
                        possible_valid_coordinate = (row + step * direction[0],
                                                     col + step * direction[1])

                        if self.out_of_board(possible_valid_coordinate):
                            # If the slots are out of board limits,
                            # it skips and creates another sequence
                            break
                        new_sequence.append(possible_valid_coordinate)

                    if len(new_sequence) == self.win_sequence_len:
                        # If the sequence is in the board's limits
                        # and in the right length, it
                        # appends it to the list of the legal sequences.
                        all_possible_sequences_in_game.append(new_sequence)

        return all_possible_sequences_in_game

    def out_of_board(self, coordinate):
        """
        The function checks if specific coordinate is the board's limits.
        It returns True if it is , returns False otherwise.
        """
        if coordinate[0] not in range(self.height):
            return True
        if coordinate[1] not in range(self.width):
            return True
        return False

    def check_if_there_is_win(self):
        """
        The function checks if any sequence of four slots
        which are not empty defines winning.
        If it is, the function returns the winner
        and the sequence of slots that 'won' the game.
        if not it returns False.
        """
        # The function goes along all the sequences in the game
        for sequence in self.all_possible_sequences_in_game:
            winning_sequence_was_found = True
            for i in range(1, len(sequence)):
                # Checks if anyone of the slots is empty.
                # If one was founded, it changes the flag to False.
                if self.board[sequence[i][0]][sequence[i][1]] == self.EMPTY_BLOCK:
                    winning_sequence_was_found = False
                    break
                # Checks if all slots has equal value.
                # If they don't, it changes the flag to False.
                if self.board[sequence[i][0]][sequence[i][1]] != \
                        self.board[sequence[i - 1][0]][sequence[i - 1][1]]:
                    winning_sequence_was_found = False
                    break
            # If the flag is still True
            # it means all slots aren't empty and equal the function returns
            # the winner and the sequence of slots that 'won' the game.
            if winning_sequence_was_found:
                return self.board[sequence[0][0]][sequence[0][1]], sequence

        return False

    def check_board_if_full(self):
        """
        The function checks if all slots on the board are full.
        The function returns True if the board is full
        and returns False otherwise.
        """
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] == Game_Board.EMPTY_BLOCK:
                    return False
        return True

    def __repr__(self):
        """
        :return: Return a string representation of the board.
        """
        string_form = ""
        for row in self.board:
            string_form += str(row) + '\n'

        return string_form
