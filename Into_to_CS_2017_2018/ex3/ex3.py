#!/usr/bin/env python3

def create_list():
    """
    let's the user enter an unlimited number of strings
    and returns those strings in a list containing them in the order
    they were entered
    """

    list_of_strings_user_entered = []

    while True:
        string_from_user = input()
        if string_from_user == "":
            break
        else:
            list_of_strings_user_entered.append(string_from_user)

    return list_of_strings_user_entered


def concat_list(str_list):
    """
    receives a list of string and returns a string which is 
    the concatenation of all of them in the order they are in the list
    """

    concatenated_string = ""

    for text in str_list:
        concatenated_string = concatenated_string + text

    return concatenated_string


def average(num_list):
    """
    receives a list of numbers and returns their average
    in case the list is empty it returns None
    """

    if len(num_list) == 0:
        return None

    sum_of_numbers = 0.0

    for num in num_list:
        sum_of_numbers += num

    return sum_of_numbers / len(num_list)


def cyclic(lst1, lst2):
    """
    gets 2 lists and returns True if one is the cyclic transformation
    of the other, and False otherwise
    """

    if len(lst1) != len(lst2):
        return False

    if len(lst1) == 0:
        return True

    length_of_lists = len(lst1)

    indices_to_start_checking_from = indices_of_item_in_list(lst1[0], lst2)
    # gets a list of indices in the second list in which the first item
    # of the first list is in

    for starting_place in indices_to_start_checking_from:
        condition_met = True

        for index_in_lst1 in range(length_of_lists):
            # checks that the lists are cyclic

            index_in_lst2 = (index_in_lst1 + starting_place) % length_of_lists

            if lst1[index_in_lst1] != lst2[index_in_lst2]:
                condition_met = False
                break

        if condition_met:
            return True

    return False


def indices_of_item_in_list(item, lst):
    """
    gets an object and a list
    returns a list containing all the indices of the list 
    in which the item is in
    if the item is not in the list the function returns an empty list 
    """

    indices_list = []

    for i in range(len(lst)):
        if lst[i] == item:
            indices_list.append(i)

    return indices_list


def histogram(n, num_list):
    """
    receives a number, n, and a list of numbers
    returns a list of size n in which each index, i, contains the 
    number of times i appears in the given list 
    """

    histogram_list = [0] * n

    for num in num_list:
        if num < n:
            histogram_list[num] += 1

    return histogram_list


def primes_list(n):
    """
    gets a number, n, and returns a list of all the primes 
    up to and including n
    """

    list_of_numbers = [x for x in range(n + 1)]
    final_prime_list = []

    for i in range(2, int(len(list_of_numbers) ** 0.5) + 1):
        # uses the sieve of eranthoses to calculate all the primes

        if list_of_numbers[i] != 0:
            for j in range(i ** 2, len(list_of_numbers), i):
                list_of_numbers[j] = 0

    for i in list_of_numbers:
        if i != 0:
            final_prime_list.append(i)

    final_prime_list.pop(0)  # pops 1 out of the prime list

    return final_prime_list


def prime_factors(n):
    """
    gets a natural number, n, and returns a list of primes such that in 
    ascending order such that multiplying all the numbers in the list 
    will give back the number n
    """

    primes = primes_list(int(n ** 0.5) + 1)
    prime_factors = []

    if n == 1:
        return prime_factors

    for i in range(len(primes)):
        if n < primes[i]:
            # we keep dividing n, as such checking it could become smaller
            # than some primes in the list
            break

        while n % primes[i] == 0:
            prime_factors.append(primes[i])
            n = n // primes[i]

    if n != 1:  # the number must be prime itself
        prime_factors.append(n)

    return prime_factors


def cartesian(lst1, lst2):
    """
    gets 2 list and returns the result of the cartesian product 
    lst1 X lst2
    """

    cartesian_prodcut_list = []

    for item1 in lst1:
        for item2 in lst2:
            cartesian_prodcut_list.append((item1, item2))

    return cartesian_prodcut_list


def pairs(n, num_list):
    """
    gets an integer number, n, and a list containing numbers
    returns all pairs of numbers that are in the given list 
    such that their sum is n
    """

    pairs_with_sum_n = []

    for i in range(len(num_list)):
        for j in range(i + 1, len(num_list)):
            if num_list[i] + num_list[j] == n:
                pairs_with_sum_n.append([num_list[i], num_list[j]])

    return pairs_with_sum_n
