import math


def golden_ratio():
    """
    prints the numerical value of the golden ratio
    """
    print((1 + math.sqrt(5)) / 2)


def six_square():
    """
    prints the numerical value of 6^2
    """
    print(math.pow(6, 2))


def hypotenuse():
    """
    prints the length of the hypotenuse of a right triangle
    with sides that have the lengths 5,12   
    """
    side_c = math.sqrt(math.pow(12, 2) + math.pow(5, 2))
    print(side_c)


def pi():
    """
    prints the numerical value of pi
    """
    print(math.pi)


def e():
    """
    prints the numerical value of e
    """
    print(math.e)


def squares_area():
    """
    prints in ascending order the areas of squares with side length that 
    vary betweeen 1 and 10
    """
    print(1 * 1, 2 * 2, 3 * 3, 4 * 4, 5 * 5, 6 * 6, 7 * 7, 8 * 8, 9 * 9, 10 * 10)
