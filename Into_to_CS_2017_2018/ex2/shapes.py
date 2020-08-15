import math


def circle_area(radius):
    """
    this function receives the radius of a circle 
    and returns its area 
    """
    return math.pi * radius ** 2


def rectangle_area(side1, side2):
    """
    this function receives the length of 2 sides of a rectangle
    and returns its area 
    """
    return float(side1) * float(side2)


def trapezoid_area(first_base, second_base, distance):
    """
    this function receives the length of 2 bases of a trapezoid
    and the length between them
    and returns its area 
    """
    area = float(distance) * (float(first_base) + float(second_base))
    area = area / 2

    return area


def shape_area():
    """
    this function prompts the user to choose a shape
    according to the chosen shape, the function waits for the user
    to input the numbers required to calculate the shape area
    
    for circle - the number represents the length of it radius
    for rectangle - the numbers represents the length of it 2 sides
    for trapezoid - the numbers represents the length of it 2 bases 
    and the length between them
    
    finally, it returns the area of the chosen shape
    """
    result = input("Choose shape (1=circle, 2=rectangle, 3=trapezoid)")
    if result == "1":
        radius = input()

        return circle_area(float(radius))

    elif result == "2":
        side1 = input()
        side2 = input()

        return rectangle_area(side1, side2)

    elif result == "3":
        first_base = input()
        second_base = input()
        distance = input()

        return trapezoid_area(first_base, second_base, distance)

    return None
