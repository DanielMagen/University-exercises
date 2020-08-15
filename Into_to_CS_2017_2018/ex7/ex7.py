#############################################################
# FILE : ex7.py
# WRITER : Daniel Magen
# EXERCISE : intro2cs ex7 2017-2018
# DESCRIPTION: this module contains a set of functions used to 
# solve different problems using recursion
#############################################################

def print_to_n(n):
    """
    this function receives an integer number
    and prints all integer numbers from 1 up to that number
    if the number is smaller than 1 the function does nothing
    """

    if n < 1:  # Does nothing to inputs smaller than 1
        return

    if n == 1:  # Base case
        print(n)

    else:  # Calls itself to print next numbers
        print_to_n(n - 1)
        print(n)


def print_reversed(n):
    """
    this function receives an integer number
    and prints all integer numbers from that number down to 1
    if the number is smaller than 1 the function does nothing
    """
    if n > 0:
        print(n)
        print_reversed(n - 1)


def is_prime(n):
    """
    this function receives an integer number
    and returns true if it is a prime and false otherwise
    """
    if n <= 1:
        return False
    return not has_divisor_smaller_than(n, n - 1)


def has_divisor_smaller_than(n, i):
    """
    this function receives an 2 integer numbers ,n and i
    and returns true if n has a divisor smaller than i
    if i is equal to or smaller than 1 it returns false
    """
    if i <= 1:  # Base case
        return False
    if n % i == 0:
        return True

    return has_divisor_smaller_than(n, i - 1)


def divisors(n):
    """
    this function receives an integer number ,n 
    and returns its divisors
    """
    if n == 0:
        return ['']
    return get_divisors_list(n, n)


def get_divisors_list(n, i):
    """
    this function receives an 2 integer numbers ,n and i
    and returns a list of numbers that aer euqal to or smaller than i
    that divide n
    """

    if n == 0 or i <= 0:  # Base case
        return []

    if n % i == 0:  # If divides appends to list and calls itself on smaller i
        return get_divisors_list(n, i - 1) + [i]

    return get_divisors_list(n, i - 1)


def exp_n_x(n, x):
    """
    this function receives an 2 integer numbers ,n and x
    and returns exp_n(x)
    """
    if n == 0:  # Base case
        return 1

    return get_x_raised_to_i_divided_by_i_fact(n, x) + exp_n_x(n - 1, x)


def get_x_raised_to_i_divided_by_i_fact(i, x):
    """
    this function receives an 2 integer numbers ,i and x
    and returns (x^i) / (i!)
    """
    if i == 0:  # Base case
        return 1

    return (x / i) * get_x_raised_to_i_divided_by_i_fact(i - 1, x)


def play_hanoi(hanoi, n, src, dest, temp):
    """
    this function receives
    hanoi - a complex object that is implemented in hanoi_game.py
    represents the graphical interface of the hanoi game
    
    n - an integer that is the number of discs that need to move
    
    src - a complex object that is implemented in hanoi_game.py
    represents a rod in the hanoi game that the discs are on
    
    dest - a complex object that is implemented in hanoi_game.py
    represents a rod in the hanoi game that the discs should move to
    
    temp - a complex object that is implemented in hanoi_game.py
    represents a rod in the hanoi game
    
    it calls hanoi.move in an order that would move all discs from src to dest
    """
    if n <= 0:  # Treats all numbers smaller than 1 as if was given 0
        return

    if n == 1:  # Base case
        hanoi.move(src, dest)
    else:
        play_hanoi(hanoi, n - 1, src, temp, dest)  # move n-1 discs to temp
        hanoi.move(src, dest)  # move largest disc to dest
        play_hanoi(hanoi, n - 1, temp, dest, src)  # move n-1 discs to dest


def print_binary_sequences(n):
    """
    this function receives an integer number ,n 
    and prints all possible sequences of 0 and 1 in length n
    """
    if n == 0:  # Base case
        return ''

    print_binary_sequences_with_prefix('0', n)
    print_binary_sequences_with_prefix('1', n)


def print_binary_sequences_with_prefix(prefix, n):
    """
    this function receives a string called prefix
    and an integer number ,n 
    it prints all possible sequences of 0 and 1 after the given prefix
    such that the length of the printed string is the smallest possible that 
    has a length of n or more
    """
    if len(prefix) == n:  # Base case
        print(prefix)
    else:
        print_binary_sequences_with_prefix(prefix + '0', n)
        print_binary_sequences_with_prefix(prefix + '1', n)


def print_sequences(char_list, n):
    """
    this function receives a list containing characters
    and an integer number ,n 
    and prints all possible sequences characters in the given list
    of length n
    """
    print_sequences_with_prefix('', char_list, 0, n)


def print_sequences_with_prefix(prefix, char_list, i, n):
    """
    this function receives 
    a string called prefix
    a list containing characters
    and 2 integer numbers ,i and n 
    
    it prints all possible sequences characters in the given list
    after the given prefix, such that the length of the printed string
    is the smallest possible that has a length of n or more
    """
    if i not in range(len(char_list)):  # if i is bigger than char_list stops
        return
    if len(prefix) >= n:  # Base case
        print(prefix)
    else:
        # Starts the function all over from 0 and with that character appended
        print_sequences_with_prefix(prefix + char_list[i], char_list, 0, n)
        # Calls the function for the next index
        print_sequences_with_prefix(prefix, char_list, i + 1, n)


def print_no_repetition_sequences(char_list, n):
    """
    this function receives a list containing characters
    and an integer numbers ,n 
    and prints all possible sequences of characters in the given list
    of length n, that have no repetition
    """
    EMPTY_STRING = ""
    EMPTY_LIST = []

    if n > len(char_list):  # Base case
        print(EMPTY_STRING)
    else:
        print_no_repetition_sequences_with_prefix(EMPTY_STRING,
                                                  char_list,
                                                  EMPTY_LIST,
                                                  0,
                                                  n)


def print_no_repetition_sequences_with_prefix(prefix,
                                              char_list,
                                              already_in_list,
                                              i,
                                              n):
    """
    this function receives 
    a string called prefix
    a list containing characters called char_list
    a list containing characters called already_in_list
    and 2 integer numbers ,i and n 
    
    it prints all possible non repeating sequences of characters in the
    given list after the given prefix, such that the length of the 
    printed string is the smallest possible that has a length of n or more,
    and such that no letter that is in the already_in_list list would appear
    after the prefix
    """
    if i not in range(len(char_list)):  # if i is bigger than char_list stops
        return
    if len(prefix) >= n:  # Base case
        print(prefix)
    else:
        if i not in already_in_list:
            # Starts function all over from 0 and with that character appended
            print_no_repetition_sequences_with_prefix(prefix + char_list[i],
                                                      char_list,
                                                      already_in_list + [i],
                                                      0,
                                                      n)
        # Calls the function for the next index
        print_no_repetition_sequences_with_prefix(prefix,
                                                  char_list,
                                                  already_in_list,
                                                  i + 1,
                                                  n)


def no_repetition_sequences_list(char_list, n):
    """
    this function receives a list containing characters
    and an integer numbers ,n 
    
    and returns a list of all possible sequences of characters 
    in the given list of length n, that have no repetition
    """
    EMPTY_STRING = ""
    EMPTY_LIST = []

    if n > len(char_list):  # Base case
        return []
    else:
        final_list = []
        append_no_repetition_sequences_with_prefix(final_list,
                                                   EMPTY_STRING,
                                                   char_list,
                                                   EMPTY_LIST,
                                                   0,
                                                   n)
        return final_list


def append_no_repetition_sequences_with_prefix(list_to_append,
                                               prefix,
                                               char_list,
                                               already_in_list,
                                               i,
                                               n):
    """
    this function receives 
    a list called list_to_append
    a string called prefix
    a list containing characters called char_list
    a list containing characters called already_in_list
    and 2 integer numbers ,i and n 
    
    it appends all possible non repeating sequences of characters in the
    given list after the given prefix, such that the length of the 
    printed string is the smallest possible that has a length of n or more,
    and such that no letter that is in the already_in_list list would appear
    after the prefix
    to list_to_append
    """
    if i not in range(len(char_list)):  # if i is bigger than char_list stops
        return

    if len(prefix) >= n:  # Base case
        list_to_append.append(prefix)
    else:
        if i not in already_in_list:
            # Starts function all over from 0 and with that character appended
            append_no_repetition_sequences_with_prefix(list_to_append,
                                                       prefix + char_list[i],
                                                       char_list,
                                                       already_in_list + [i],
                                                       0,
                                                       n)
        # Calls the function for the next index
        append_no_repetition_sequences_with_prefix(list_to_append,
                                                   prefix,
                                                   char_list,
                                                   already_in_list,
                                                   i + 1,
                                                   n)


print(divisors(0))
