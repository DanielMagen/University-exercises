import hangman_helper

CHAR_A = 97


def update_word_pattern(word, pattern, letter):
    """
    this function gets a word, a pattern and a letter
    returns a new pattern that is the given pattern with some '_' replaced
    by the given letter in the index they appear in the given word
    """

    new_pattern = ''

    # assumes the word and the pattern given have the same length
    for i, character in enumerate(word):
        if character == letter:
            new_pattern += letter
        else:
            new_pattern += pattern[i]

    return new_pattern


def run_single_game(words_list):
    """
    this function manages hangman_helper 
    and stores information relevant to the game, during the game
    
    it does not return a value
    """

    random_word = hangman_helper.get_random_word(words_list)
    wrong_guess_lst = []
    error_count = 0
    pattern = '_' * len(random_word)
    has_won = False
    msg = hangman_helper.DEFAULT_MSG

    hangman_helper.display_state(pattern, error_count, wrong_guess_lst, msg)

    while error_count < hangman_helper.MAX_ERRORS and not has_won:

        input_from_user = hangman_helper.get_input()
        # gets the input from the user

        if input_from_user[0] == hangman_helper.HINT:
            # the user is asking for a hint
            msg = hint_handler(words_list, pattern, wrong_guess_lst)

        elif input_from_user[0] == hangman_helper.LETTER:
            # the user has entered a character
            letter = input_from_user[1]
            msg, error_count, pattern = input_handler(letter,
                                                      random_word,
                                                      pattern,
                                                      error_count,
                                                      wrong_guess_lst)

        hangman_helper.display_state(pattern,
                                     error_count,
                                     wrong_guess_lst,
                                     msg)
        # updates the game display according to the given input

        if pattern == random_word:
            has_won = True

    win_handler(has_won, random_word, pattern, error_count, wrong_guess_lst)
    # once the loop has finished it calls win_handler 
    # to display the appropriate message to the user


def hint_handler(words_list, pattern, wrong_guess_lst):
    """
    if the user asks for a hint 
    this function generates a hint message using the hangman_helper module
    and returns it
    """

    filtered_words = filter_words_list(words_list,
                                       pattern,
                                       wrong_guess_lst)

    hint_letter = choose_letter(filtered_words, pattern)

    msg = hangman_helper.HINT_MSG + hint_letter

    return msg


def win_handler(has_won, random_word, pattern, error_count, wrong_guess_lst):
    """
    if the game ends, this function receives a boolean that states if the user
    has won or not, and displays a message to the user accordingly 
    using hangman_helper.display_state
    """

    if not has_won:
        msg = hangman_helper.LOSS_MSG + random_word
    else:
        msg = hangman_helper.WIN_MSG

    hangman_helper.display_state(pattern,
                                 error_count,
                                 wrong_guess_lst,
                                 msg,
                                 ask_play=True)


def input_handler(letter, random_word, pattern, error_count, wrong_guess_lst):
    """
    once the user enters an input this function is called
    it checks the validity of the input and returns a tuple 
    containing an updated (msg, error_count, pattern)
    
    it might append an item to wrong_guess_lst
    """

    if (len(letter) > 1) or (not letter.islower()):
        # non valid character
        msg = hangman_helper.NON_VALID_MSG

    elif (letter in wrong_guess_lst) or (letter in pattern):
        # character was entered before
        msg = hangman_helper.ALREADY_CHOSEN_MSG + letter

    else:
        # the character is valid
        msg = hangman_helper.DEFAULT_MSG

        new_pattern = update_word_pattern(random_word,
                                          pattern,
                                          letter)
        if new_pattern != pattern:
            pattern = new_pattern

        else:
            wrong_guess_lst.append(letter)
            error_count += 1

    return msg, error_count, pattern


def main():
    """
    this function does not receive an input
    as long as the user did not specify that he wishes to exit the game
    it loads all the words using hangman_helper and starts a new game
    """

    wants_to_play = True

    while wants_to_play:
        words_list = hangman_helper.load_words()

        run_single_game(words_list)

        keep_playing = hangman_helper.get_input()

        if keep_playing[0] == hangman_helper.PLAY_AGAIN:
            if keep_playing[1] == False:
                wants_to_play = False


def filter_words_list(words, pattern, wrong_guess_lst):
    """
    this function receives a list of words, a pattern and a guess list 
    it returns all the words in the words list that
    do not contain any letter that is in the guess list, 
    and that also matches the given pattern
    """

    words_that_match = []

    for word in words:
        word_matches = True

        if len(word) != len(pattern):
            continue

        for i, character in enumerate(word):
            if pattern[i] != '_':
                if pattern[i] != character or character in wrong_guess_lst:
                    word_matches = False
                    break

        if word_matches:
            words_that_match.append(word)

    return words_that_match


def letter_to_index(letter):
    """
    receives a lower case letter and converts it into a number between 0-25 
    """
    return ord(letter.lower()) - CHAR_A


def index_to_letter(index):
    """
    receives a number between 0-25  and converts it into a lower case letter
    between a-z
    """
    return chr(index + CHAR_A)


def choose_letter(words, pattern):
    """
    receives a list of words and a pattern
    returns the letter that is both 
    - most frequent in the given word list
    - does not appear in the given pattern
    """

    NUMBER_OF_LETTERS_IN_ALPHABET = 26
    letters_popularity = [[i, 0] for i in range(NUMBER_OF_LETTERS_IN_ALPHABET)]

    for word in words:
        for character in word:
            letters_popularity[letter_to_index(character)][1] += 1

    letters_popularity = sorted(letters_popularity,
                                key=lambda lst: lst[1],
                                reverse=True)

    for lst in letters_popularity:
        character = index_to_letter(lst[0])
        if not character in pattern:
            return character


if __name__ == "__main__":
    hangman_helper, hangman_helper.start_gui_and_call_main(main)
    hangman_helper.close_gui()
